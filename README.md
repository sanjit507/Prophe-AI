# Prophe-AI

A Django-based real estate analytics and recommendation platform with property price prediction, map visualization, and a recommender system.

<img width="1884" height="824" alt="Screenshot 2026-05-28 235314" src="https://github.com/user-attachments/assets/a22bcc2b-d4c8-4a0f-8ba1-6d449ba25f35" />

<img width="1649" height="774" alt="image" src="https://github.com/user-attachments/assets/c9d7f234-ecc2-4664-b17e-8debb5c040f1" />

<img width="1635" height="801" alt="image" src="https://github.com/user-attachments/assets/897fc035-80c4-4b9b-907b-d0d42e4ddfd9" />

<img width="1645" height="699" alt="image" src="https://github.com/user-attachments/assets/a7b4f4ef-a7c2-4fb9-8a33-a2868f707073" />


<img width="1812" height="739" alt="image" src="https://github.com/user-attachments/assets/69d79285-0edd-4abc-9ed3-0c43d7aebfbc" />

<img width="1917" height="828" alt="image" src="https://github.com/user-attachments/assets/59559ee4-cfff-4a1b-80a1-fdfc7f28ea40" />

<img width="1491" height="698" alt="image" src="https://github.com/user-attachments/assets/b147cc5e-22bf-4e28-9f8b-13205803bf8f" />


<img width="1452" height="683" alt="image" src="https://github.com/user-attachments/assets/5ac77ee4-64ec-4b31-97a7-b49ed8222780" />

<img width="1411" height="705" alt="image" src="https://github.com/user-attachments/assets/9a230e20-9128-425c-99f0-3d1e75014d57" />



## Highlights
- Property price prediction with a dedicated UI flow.
- Interactive analytics with map visualization.
- Apartment recommender system powered by a trained model and curated dataset.

## Tech Stack
- Backend: Python, Django
- Frontend: Django Templates, HTML, CSS
- Data/ML: Pandas, NumPy, scikit-learn (via notebooks and model artifacts)
- Persistence: SQLite (default dev database)
- Deployment: Procfile + runtime.txt + nixpacks.toml

## Project Structure
- Analytics/ - Analytics app with datasets and visualization notebook.
- predictions/ - Prediction app, model artifacts, and UI templates.
- recommender_system/ - Recommender app, model artifacts, and UI templates.
- prophe/ - Project settings, URLs, and base templates.
- static/ - CSS and static assets across apps.

## How It Works
1. Analytics app prepares and visualizes property data using datasets and a notebook.
2. Prediction app loads trained model artifacts and serves a prediction form + result page.
3. Recommender system app reads curated apartment data and suggests similar listings.
4. Users navigate through the Django templates rendered by each app.

## Local Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000/ in your browser.

## Apps and Routes
- Core site: `prophe/`
- Analytics: `Analytics/`
- Predictions: `predictions/`
- Recommender: `recommender_system/`

## Data and Models
- Analytics datasets: `Analytics/data/`
- Recommender datasets: `recommender_system/Model/`
- Prediction models: `predictions/model/`

## Deployment Notes
- Uses `Procfile`, `runtime.txt`, and `nixpacks.toml` for deployment configuration.
- Update environment settings in `prophe/settings.py` for production (e.g., DEBUG, ALLOWED_HOSTS, database).

## Future Enhancements
- Add REST API endpoints for predictions and recommendations.
- Improve model explainability and feature importance views.
- Add user accounts and saved recommendations.


