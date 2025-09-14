# Rich university data for UI and details
import json
from pathlib import Path
from urllib.parse import quote_plus


def _load_external_data():
    data_path = Path("data/universities.json")
    if data_path.exists():
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Basic validation
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return None


universities = _load_external_data() or [
    {
        "slug": "university-of-dubai",
        "name": "University of Dubai",
        "city": "Dubai",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/University_of_Dubai_logo.svg/512px-University_of_Dubai_logo.svg.png",
        "description": "A leading university in Dubai offering undergraduate and postgraduate programs across business, engineering, and IT.",
        "requirements": [
            "High school diploma (or equivalent)",
            "Official transcripts",
            "English proficiency (IELTS 6.0 / TOEFL iBT 70)",
            "Valid ID/Passport",
        ],
        "programs": ["Business", "Engineering", "IT"],
    },
    {
        "slug": "heriot-watt-university-dubai",
        "name": "Heriot-Watt University Dubai",
        "city": "Dubai",
        "image": "",
        "description": "Scottish university branch campus offering engineering, business, and design.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Engineering", "Business", "Design"],
    },
    {
        "slug": "middlesex-university-dubai",
        "name": "Middlesex University Dubai",
        "city": "Dubai",
        "image": "",
        "description": "UK university branch campus with broad UG/PG offerings.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Business", "Law", "IT", "Media"],
    },
    {
        "slug": "university-of-birmingham-dubai",
        "name": "University of Birmingham Dubai",
        "city": "Dubai",
        "image": "",
        "description": "Russell Group university branch campus in Dubai International Academic City.",
        "requirements": ["Strong academics", "English proficiency"],
        "programs": ["Business", "Education", "Computer Science", "Engineering"],
    },
    {
        "slug": "canadian-university-dubai",
        "name": "Canadian University Dubai",
        "city": "Dubai",
        "image": "",
        "description": "Private university offering Canadian-curriculum inspired programs.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Business", "Engineering", "Architecture", "Communication"],
    },
    {
        "slug": "bits-pilani-dubai",
        "name": "BITS Pilani Dubai Campus",
        "city": "Dubai",
        "image": "",
        "description": "Indian university branch campus focused on engineering and technology.",
        "requirements": ["Science stream", "Entrance criteria", "English proficiency"],
        "programs": ["Engineering", "Technology"],
    },
    {
        "slug": "mahe-dubai",
        "name": "Manipal Academy of Higher Education (Dubai)",
        "city": "Dubai",
        "image": "",
        "description": "MAHE Dubai offers programs in engineering, business, design, and media.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Engineering", "Business", "Design", "Media"],
    },
    {
        "slug": "amity-university-dubai",
        "name": "Amity University Dubai",
        "city": "Dubai",
        "image": "",
        "description": "Indian private university campus with a wide range of programs.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Business", "Engineering", "Hospitality", "Law"],
    },
    {
        "slug": "curtin-university-dubai",
        "name": "Curtin University Dubai",
        "city": "Dubai",
        "image": "",
        "description": "Australian university branch campus offering business and IT programs.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Business", "IT"],
    },
    {
        "slug": "murdoch-university-dubai",
        "name": "Murdoch University Dubai",
        "city": "Dubai",
        "image": "",
        "description": "Australian university branch campus known for media and business.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Media", "Business", "IT"],
    },
    {
        "slug": "sp-jain-dubai",
        "name": "SP Jain School of Global Management (Dubai)",
        "city": "Dubai",
        "image": "",
        "description": "Global management school offering business programs with multi-city model.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Business", "Management"],
    },
    {
        "slug": "rit-dubai",
        "name": "Rochester Institute of Technology (RIT) Dubai",
        "city": "Dubai",
        "image": "",
        "description": "US university branch campus focused on engineering and computing.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Engineering", "Computing", "Business"],
    },
    {
        "slug": "hult-dubai",
        "name": "Hult International Business School (Dubai)",
        "city": "Dubai",
        "image": "",
        "description": "Business school offering undergraduate and postgraduate programs.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Business", "Marketing", "Finance"],
    },
    {
        "slug": "uowd",
        "name": "University of Wollongong in Dubai (UOWD)",
        "city": "Dubai",
        "image": "",
        "description": "One of Dubai’s oldest private universities with broad programs.",
        "requirements": ["High school certificate", "English proficiency"],
        "programs": ["Business", "IT", "Engineering", "Media"],
    },
    {
        "slug": "american-university-in-dubai",
        "name": "American University in Dubai",
        "city": "Dubai",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/AUD_Logo.svg/512px-AUD_Logo.svg.png",
        "description": "An American-style institution offering diverse programs with strong industry links.",
        "requirements": [
            "High school certificate",
            "SAT/EmSAT (program dependent)",
            "English proficiency (IELTS/TOEFL)",
        ],
        "programs": ["Business", "Engineering", "Communication", "Architecture"],
    },
    {
        "slug": "zayed-university",
        "name": "Zayed University",
        "city": "Dubai",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Zayed_University_Logo.png/512px-Zayed_University_Logo.png",
        "description": "Federal university with campuses in Dubai and Abu Dhabi offering a range of programs.",
        "requirements": [
            "High school certificate",
            "English proficiency",
            "Program-specific assessments",
        ],
        "programs": ["Education", "Business", "IT", "Arts"],
    },
    {
        "slug": "khalifa-university",
        "name": "Khalifa University",
        "city": "Abu Dhabi",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Khalifa_University_logo.svg/512px-Khalifa_University_logo.svg.png",
        "description": "Top-ranked science and engineering university in Abu Dhabi.",
        "requirements": [
            "Strong STEM high school background",
            "Math/Science assessments",
            "English proficiency",
        ],
        "programs": ["Engineering", "Science", "Medicine"],
    },
    {
        "slug": "nyu-abu-dhabi",
        "name": "New York University Abu Dhabi",
        "city": "Abu Dhabi",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/New_York_University_Logo.svg/512px-New_York_University_Logo.svg.png",
        "description": "Selective liberal arts and research university with global curriculum.",
        "requirements": [
            "Competitive academic record",
            "Standardized tests (optional/varies)",
            "Essays and recommendations",
        ],
        "programs": ["Liberal Arts", "Science", "Engineering"],
    },
    {
        "slug": "american-university-of-sharjah",
        "name": "American University of Sharjah",
        "city": "Sharjah",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/AUS_logo.svg/512px-AUS_logo.svg.png",
        "description": "Accredited American-style university known for architecture, engineering, and business.",
        "requirements": [
            "High school certificate",
            "Math/Physics placement (program dependent)",
            "English proficiency",
        ],
        "programs": ["Architecture", "Engineering", "Business", "Arts"],
    },
    {
        "slug": "university-of-sharjah",
        "name": "University of Sharjah",
        "city": "Sharjah",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/University_of_Sharjah_logo.svg/512px-University_of_Sharjah_logo.svg.png",
        "description": "Comprehensive university offering programs across medicine, engineering, and humanities.",
        "requirements": [
            "High school certificate",
            "Program-specific criteria",
            "English/Arabic proficiency per program",
        ],
        "programs": ["Medicine", "Engineering", "Business", "Humanities"],
    },
    {
        "slug": "ajman-university",
        "name": "Ajman University",
        "city": "Ajman",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Ajman_University_logo.svg/512px-Ajman_University_logo.svg.png",
        "description": "Private university with programs in engineering, business, pharmacy, and more.",
        "requirements": [
            "High school certificate",
            "English proficiency",
        ],
        "programs": ["Engineering", "Business", "Pharmacy", "Law"],
    },
    {
        "slug": "gulf-medical-university",
        "name": "Gulf Medical University",
        "city": "Ajman",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Gulf_Medical_University_logo.png/512px-Gulf_Medical_University_logo.png",
        "description": "Medical-focused university offering health sciences programs.",
        "requirements": [
            "High school science stream",
            "Entrance exam/interview",
            "English proficiency",
        ],
        "programs": ["Medicine", "Health Sciences"],
    },
    {
        "slug": "aurak",
        "name": "American University of Ras Al Khaimah",
        "city": "Ras Al Khaimah",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/AURAK_logo.svg/512px-AURAK_logo.svg.png",
        "description": "Public university with American-style curriculum.",
        "requirements": [
            "High school certificate",
            "English proficiency",
        ],
        "programs": ["Engineering", "Business", "Design"],
    },
    {
        "slug": "rakmhsu",
        "name": "RAK Medical and Health Sciences University",
        "city": "Ras Al Khaimah",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/5/54/RAKMHSU_Logo.png/512px-RAKMHSU_Logo.png",
        "description": "Specialized medical university in Ras Al Khaimah.",
        "requirements": [
            "Science stream",
            "Entrance assessments",
            "English proficiency",
        ],
        "programs": ["Medicine", "Health Sciences"],
    },
    {
        "slug": "university-of-fujairah",
        "name": "University of Fujairah",
        "city": "Fujairah",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/University_of_Fujairah_logo.png/512px-University_of_Fujairah_logo.png",
        "description": "University serving the East Coast with various programs.",
        "requirements": [
            "High school certificate",
            "English proficiency",
        ],
        "programs": ["Business", "IT"],
    },
    {
        "slug": "emirates-canadian-university-college",
        "name": "Emirates Canadian University College",
        "city": "Umm Al Quwain",
        "image": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d2/Emirates_Canadian_University_College_logo.png/512px-Emirates_Canadian_University_College_logo.png",
        "description": "Private college offering business and law programs.",
        "requirements": [
            "High school certificate",
            "English proficiency",
        ],
        "programs": ["Business", "Law"],
    },
]

# Fill image URLs for entries missing an image using Clearbit logo by domain
_DOMAIN_BY_SLUG = {
    # Abu Dhabi / Al Ain
    "united-arab-emirates-university": "uaeu.ac.ae",
    "al-ain-university": "aau.ac.ae",
    "abu-dhabi-university": "adu.ac.ae",
    "sorbonne-university-abu-dhabi": "sorbonne.ae",
    "zayed-university-abu-dhabi": "zu.ac.ae",
    "khalifa-university": "ku.ac.ae",
    "nyu-abu-dhabi": "nyuad.nyu.edu",
    "emirates-college-of-technology": "ect.ac.ae",
    # Dubai
    "university-of-dubai": "ud.ac.ae",
    "american-university-in-dubai": "aud.edu",
    "zayed-university-dubai": "zu.ac.ae",
    "heriot-watt-university-dubai": "hw.ac.uk",
    "middlesex-university-dubai": "mdx.ac.ae",
    "university-of-birmingham-dubai": "birmingham.ac.uk",
    "canadian-university-dubai": "cud.ac.ae",
    "bits-pilani-dubai": "bits-pilani.ac.in",
    "mahe-dubai": "manipal.edu",
    "amity-university-dubai": "amityuniversity.ae",
    "curtin-university-dubai": "curtindubai.ac.ae",
    "murdoch-university-dubai": "murdochuniversitydubai.com",
    "sp-jain-dubai": "spjain.ae",
    "rit-dubai": "rit.edu",
    "hult-dubai": "hult.edu",
    "uowd": "uowdubai.ac.ae",
    "buid": "buid.ac.ae",
    "mbru": "mbru.ac.ae",
    "hbmsu": "hbmsu.ac.ae",
    "emirates-aviation-university": "eau.ac.ae",
    # Sharjah
    "american-university-of-sharjah": "aus.edu",
    "university-of-sharjah": "sharjah.ac.ae",
    "skyline-university-college": "skylineuniversity.ac.ae",
    "al-qasimia-university": "aqu.ac.ae",
    # Ajman
    "ajman-university": "ajman.ac.ae",
    "gulf-medical-university": "gmu.ac.ae",
    "cuca": "cuca.ae",
    # Ras Al Khaimah
    "aurak": "aurak.ac.ae",
    "rakmhsu": "rakmhsu.ac.ae",
    "bath-spa-university-rak": "bathspa.ac.ae",
    # Fujairah
    "university-of-fujairah": "uof.ac.ae",
    # Umm Al Quwain
    "emirates-canadian-university-college": "ecuc.ac.ae",
    # HCT
    "hct-abu-dhabi": "hct.ac.ae",
    "hct-dubai": "hct.ac.ae",
    "hct-sharjah": "hct.ac.ae",
}

for u in universities:
    # Attach a photo-style Unsplash URL for visual cards
    try:
        q = f"{u.get('name','')} {u.get('city','')}".strip()
        uq = quote_plus(q)
        u["photo_url"] = f"https://source.unsplash.com/featured/1200x800?university,campus,{uq}"
    except Exception:
        pass
    # If no image set, try a logo as a backup
    if not u.get("image"):
        slug = u.get("slug")
        domain = _DOMAIN_BY_SLUG.get(slug)
        if domain:
            u["image"] = f"https://logo.clearbit.com/{domain}"

def get_universities_by_city(city: str):
    return [u for u in universities if u["city"].lower() == (city or "").lower()]

def get_university_by_slug(slug: str):
    for u in universities:
        if u["slug"] == slug:
            return u
    return None

def get_programs_by_city(city: str):
    opts = set()
    for u in get_universities_by_city(city):
        for p in u.get("programs", []):
            opts.add(p)
    return sorted(opts)

def get_cities():
    return sorted({u.get("city") for u in universities if u.get("city")})
