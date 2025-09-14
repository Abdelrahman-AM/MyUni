from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import get_universities_by_city, get_university_by_slug, get_programs_by_city, get_cities
from database import universities as ALL_UNIS
import os
from pathlib import Path
import threading
try:
    import requests
    from requests.exceptions import RequestException
except Exception:  # Fallback so the app still runs without requests
    requests = None
    class RequestException(Exception):
        pass
from concurrent.futures import ThreadPoolExecutor, as_completed
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
import time
from collections import defaultdict, deque
# Pydantic email validation: fall back to plain str if email-validator not installed
try:
    import email_validator  # noqa: F401
    from pydantic import BaseModel, EmailStr, Field
except Exception:
    from pydantic import BaseModel, Field
    EmailStr = str  # type: ignore
from typing import List, Optional
import secrets, json

# Initialize the FastAPI app
app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Basic security middleware ---

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # Security headers (basic starter set)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer-when-downgrade")
        # CSP allows our domain, Bootstrap CDN, and HTTPS images
        csp = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' data: https://cdn.jsdelivr.net; "
            "object-src 'none'; frame-ancestors 'none'"
        )
        # Only set if not already present
        response.headers.setdefault("Content-Security-Policy", csp)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window_seconds
        self.bucket = defaultdict(deque)  # ip -> deque of timestamps

    async def dispatch(self, request, call_next):
        ip = request.client.host if request.client else "anon"
        now = time.time()
        dq = self.bucket[ip]
        # Drop old entries
        cutoff = now - self.window
        while dq and dq[0] < cutoff:
            dq.popleft()
        if len(dq) >= self.limit:
            return PlainTextResponse("Too Many Requests", status_code=429)
        dq.append(now)
        response = await call_next(request)
        # Simple rate-limit headers
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, self.limit - len(dq)))
        return response


# Restrict Host header (configurable via ALLOWED_HOSTS env)
_hosts = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,::1").split(",") if h.strip()]
app.add_middleware(TrustedHostMiddleware, allowed_hosts=_hosts)

# Narrow CORS (for dev UI browsing only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Attach security headers and a simple in-memory rate limiter
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, limit=120, window_seconds=60)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render the index.html template
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/universities", response_class=HTMLResponse)
async def universities(request: Request, city: str = Query(None), q: str = Query(None), program: str = Query(None), page: int = Query(1, ge=1)):
    if not city:
        return HTMLResponse("No city selected", status_code=400)
    # Validate city against known list
    valid_cities = set(get_cities())
    if city not in valid_cities:
        raise HTTPException(status_code=404, detail="City not found")

    unis = get_universities_by_city(city)

    # Apply filters
    if program:
        unis = [u for u in unis if program in u.get("programs", [])]
    if q:
        q = q[:100]  # basic length limit
        needle = q.lower()
        unis = [
            u for u in unis
            if needle in u["name"].lower() or needle in u.get("description", "").lower()
        ]

    # Resolve image for each university (local cached if available, else remote)
    unis_view_all = []
    for u in unis:
        u2 = dict(u)
        # Prefer Unsplash photo for display; fallback to local-or-remote logo/default
        disp = u.get("photo_url") or _local_or_remote(u["slug"], u.get("image", "/static/images/default.svg"))
        u2["display_image"] = disp
        unis_view_all.append(u2)

    # Simple server-side pagination
    page_size = 12
    total_count = len(unis_view_all)
    total_pages = max(1, (total_count + page_size - 1) // page_size)
    page = min(page, total_pages)
    start = (page - 1) * page_size
    end = start + page_size
    unis_view = unis_view_all[start:end]

    program_options = get_programs_by_city(city)
    return templates.TemplateResponse(
        "universities.html",
        {
            "request": request,
            "city": city,
            "universities": unis_view,
            "q": q or "",
            "program": program or "",
            "program_options": program_options,
            "total_count": total_count,
            "page": page,
            "total_pages": total_pages,
            "page_size": page_size,
        },
    )

@app.get("/university/{slug}", response_class=HTMLResponse)
async def university_detail(request: Request, slug: str):
    uni = get_university_by_slug(slug)
    if not uni:
        raise HTTPException(status_code=404, detail="University not found")
    uni_view = dict(uni)
    uni_view["display_image"] = uni.get("photo_url") or _local_or_remote(uni["slug"], uni.get("image", "/static/images/default.svg"))
    return templates.TemplateResponse(
        "university_detail.html", {"request": request, "uni": uni_view}
    )


def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTS = ["jpg", "jpeg", "png", "webp", "svg"]


def _existing_local(dest_dir: Path, slug: str):
    for ext in ALLOWED_EXTS:
        p = dest_dir / f"{slug}.{ext}"
        if p.exists() and p.stat().st_size > 2048:
            return p
    return None


def _download_one(headers, dest_dir: Path, slug: str, url: str) -> bool:
    if requests is None:
        return False
    if not slug or not url:
        return False
    if _existing_local(dest_dir, slug):
        return True
    try:
        r = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        if r.status_code != 200 or not r.content:
            return False
        ctype = r.headers.get("content-type", "").lower()
        ext = "jpg"
        if "svg" in ctype:
            ext = "svg"
        elif "png" in ctype:
            ext = "png"
        elif "webp" in ctype:
            ext = "webp"
        elif "jpeg" in ctype:
            ext = "jpg"
        dest_file = dest_dir / f"{slug}.{ext}"
        with open(dest_file, "wb") as f:
            f.write(r.content)
        return True
    except RequestException:
        return False


def _download_first_available(headers, dest_dir: Path, slug: str, urls):
    for url in urls:
        if _download_one(headers, dest_dir, slug, url):
            return True
    return False


def _cache_images():
    if requests is None:
        return  # Skip caching if requests is unavailable
    dest_dir = Path("static/images")
    _ensure_dir(dest_dir)
    headers = {"User-Agent": "MyUni/1.0 (+cache)"}
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = []
        for u in ALL_UNIS:
            slug = u.get("slug")
            if not slug:
                continue
            sources = []
            img = u.get("image")
            if img:
                sources.append(img)
            # Last-resort fast placeholder to ensure something shows if remotes fail
            sources.append(f"https://picsum.photos/seed/{slug}/1200/800")
            futures.append(ex.submit(_download_first_available, headers, dest_dir, slug, sources))
        for _ in as_completed(futures):
            pass


@app.on_event("startup")
async def prefetch_images_on_startup():
    # Run in background thread to avoid blocking startup
    threading.Thread(target=_cache_images, daemon=True).start()


def _local_or_remote(slug: str, remote_url: str) -> str:
    dest_dir = Path("static/images")
    p = _existing_local(dest_dir, slug)
    if p:
        return f"/static/images/{p.name}"
    # Use configured remote URL if provided, else neutral default
    return remote_url or "/static/images/default.svg"


# --------- Basic data submission API (favorites list) ---------

class SavePayload(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    city: Optional[str] = Field(default=None, max_length=80)
    favorites: List[str] = Field(default_factory=list)
    note: Optional[str] = Field(default=None, max_length=500)


def _safe_write_jsonl(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        import json, time
        obj = dict(obj)
        obj["ts"] = int(time.time())
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


@app.post("/api/save")
async def save_favorites(payload: SavePayload, request: Request):
    # Basic validation for city in known list, silently drop unknowns
    cities = set(get_cities())
    city = payload.city if payload.city in cities else None

    # Only accept known slugs
    known_slugs = {u.get("slug") for u in ALL_UNIS}
    favorites = [s for s in payload.favorites if s in known_slugs][:100]

    # Persist to a JSONL file
    record = {
        "name": payload.name.strip(),
        "email": str(payload.email),
        "city": city,
        "favorites": favorites,
        "note": (payload.note or "").strip(),
        "ip": request.client.host if request.client else None,
    }
    _safe_write_jsonl(Path("data/submissions.jsonl"), record)
    return {"ok": True, "saved": len(favorites)}


# ---------------- Accounts and sessions ----------------

USERS_PATH = Path("data/users.json")
SESSIONS_PATH = Path("data/sessions.json")

def _load_json(path: Path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default

def _save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f)
    tmp.replace(path)

try:
    import bcrypt
    def _hash_pw(pw: str) -> str:
        return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    def _check_pw(pw: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(pw.encode(), hashed.encode())
        except Exception:
            return False
except Exception:
    import hashlib
    def _hash_pw(pw: str) -> str:
        salt = secrets.token_hex(8)
        h = hashlib.sha256((salt+pw).encode()).hexdigest()
        return f"sha256${salt}${h}"
    def _check_pw(pw: str, hashed: str) -> bool:
        try:
            algo, salt, h = hashed.split("$")
            return hashlib.sha256((salt+pw).encode()).hexdigest() == h
        except Exception:
            return False

def _get_users():
    return _load_json(USERS_PATH, [])

def _save_users(users):
    _save_json(USERS_PATH, users)

def _get_sessions():
    return _load_json(SESSIONS_PATH, {})

def _save_sessions(s):
    _save_json(SESSIONS_PATH, s)

def _find_user_by_email(email: str):
    email = (email or "").strip().lower()
    for u in _get_users():
        if u.get("email") == email:
            return u
    return None

def _create_user(name: str, email: str, password: str):
    email = (email or "").strip().lower()
    users = _get_users()
    if any(u.get("email") == email for u in users):
        return None
    uid = secrets.token_hex(8)
    user = {"id": uid, "name": name.strip(), "email": email, "password": _hash_pw(password), "favorites": []}
    users.append(user)
    _save_users(users)
    return user

def _auth_user(email: str, password: str):
    u = _find_user_by_email(email)
    if not u:
        return None
    return u if _check_pw(password, u.get("password")) else None

def _create_session(user_id: str):
    sessions = _get_sessions()
    sid = secrets.token_urlsafe(24)
    sessions[sid] = {"user_id": user_id, "ts": int(time.time())}
    _save_sessions(sessions)
    return sid

def _delete_session(sid: str):
    sessions = _get_sessions()
    if sid in sessions:
        sessions.pop(sid)
        _save_sessions(sessions)

def _current_user(request: Request):
    sid = request.cookies.get("myuni_session")
    if not sid:
        return None
    sessions = _get_sessions()
    sess = sessions.get(sid)
    if not sess:
        return None
    uid = sess.get("user_id")
    for u in _get_users():
        if u.get("id") == uid:
            return u
    return None

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "user": _current_user(request)})

@app.post("/signup")
async def signup(request: Request):
    form = await request.form()
    name = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip()
    password = form.get("password") or ""
    if not name or not email or not password:
        return PlainTextResponse("Missing fields", status_code=400)
    if _find_user_by_email(email):
        return PlainTextResponse("Email already registered", status_code=400)
    user = _create_user(name, email, password)
    if not user:
        return PlainTextResponse("Could not create user", status_code=400)
    sid = _create_session(user["id"])
    resp = RedirectResponse(url="/favorites", status_code=303)
    resp.set_cookie("myuni_session", sid, httponly=True, samesite="lax")
    return resp

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "user": _current_user(request)})

@app.post("/login")
async def login(request: Request):
    form = await request.form()
    email = (form.get("email") or "").strip()
    password = form.get("password") or ""
    user = _auth_user(email, password)
    if not user:
        return PlainTextResponse("Invalid credentials", status_code=401)
    sid = _create_session(user["id"])
    resp = RedirectResponse(url="/favorites", status_code=303)
    resp.set_cookie("myuni_session", sid, httponly=True, samesite="lax")
    return resp

@app.post("/logout")
async def logout(request: Request):
    sid = request.cookies.get("myuni_session")
    if sid:
        _delete_session(sid)
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("myuni_session")
    return resp

@app.get("/favorites", response_class=HTMLResponse)
async def favorites_page(request: Request):
    user = _current_user(request)
    context = {"request": request, "user": user}
    if user:
        slugs = set(user.get("favorites") or [])
        items = []
        for u in ALL_UNIS:
            if u.get("slug") in slugs:
                u2 = dict(u)
                u2["local_image"] = _local_or_remote(u["slug"], u.get("image", "/static/images/default.svg"))
                items.append(u2)
        context["items"] = items
    return templates.TemplateResponse("favorites.html", context)

class FavoritePayload(BaseModel):
    favorites: List[str] = Field(default_factory=list)

@app.get("/api/favorites")
async def api_get_favorites(request: Request):
    user = _current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Login required")
    return {"favorites": user.get("favorites", [])}

@app.post("/api/favorites")
async def api_set_favorites(payload: FavoritePayload, request: Request):
    user = _current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Login required")
    known = {u.get("slug") for u in ALL_UNIS}
    favs = [s for s in payload.favorites if s in known][:200]
    users = _get_users()
    for u in users:
        if u.get("id") == user.get("id"):
            u["favorites"] = favs
            break
    _save_users(users)
    return {"ok": True, "saved": len(favs)}
