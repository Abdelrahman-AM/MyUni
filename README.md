# MyUni

A simple FastAPI site to browse universities in the UAE by city.

## Features

- City picker on the home page
- Dynamic list of universities per city
- Responsive UI via Bootstrap

## Getting Started

1. Create a virtual environment (optional but recommended):
   
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   ```

2. Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   
   ```bash
   uvicorn app:app --reload
   ```

4. Open the app in your browser:
   
   - Home: http://127.0.0.1:8000/
   - Example: http://127.0.0.1:8000/universities?city=Dubai

## Project Structure

- `app.py`: FastAPI app and routes
- `database.py`: In-memory data for universities
- `templates/`: Jinja2 templates (`index.html`, `universities.html`)
- `static/`: Static assets (CSS)

## Notes

- Data is static and stored in-memory for simplicity. Replace `database.py` with a real database as needed.
- Adjust `templates/index.html` dropdown to add or remove cities.
