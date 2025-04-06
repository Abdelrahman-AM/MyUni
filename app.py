from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import universities_data  # Import your data from database.py

# Initialize the FastAPI app
app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render the index.html template
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/universities", response_class=HTMLResponse)
async def universities(request: Request, city: str = Query(None)):
    if city:
        # Retrieve universities for the city from the database
        universities = universities_data.get(city, [])
        return templates.TemplateResponse(
            "universities.html", {"request": request, "city": city, "universities": universities}
        )
    else:
        # Return a 400 error if no city is provided
        return HTMLResponse("No city selected", status_code=400)