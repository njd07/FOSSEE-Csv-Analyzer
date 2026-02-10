# CSV Visualizer — Chemical Equipment Parameter Visualizer

A hybrid web + desktop application for uploading chemical equipment CSV data, viewing summaries, visualizing charts, and generating PDF reports.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Django + Django REST Framework |
| Database | SQLite |
| CSV Handling | pandas |
| Web Frontend | React.js + Chart.js |
| Desktop Frontend | PyQt5 + Matplotlib |
| PDF Generation | ReportLab |
| Deployment | Railway (backend) |

## Project Structure

```
csv_visualizer/
├── backend/               # Django REST API
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── visualizer_api/    # Django project settings
│   └── app_core/          # Main app: models, views, utils
├── web_client/            # React frontend
│   ├── package.json
│   └── src/
│       ├── App.js
│       ├── components/    # UploadCard, SummaryPanel, etc.
│       └── styles/
├── desktop_client/        # PyQt5 desktop app
│   ├── app.py
│   └── components/
├── sample_equipment_data.csv
└── README.md
```

## Setup Instructions

### 1. Backend

```bash
cd backend

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (for authentication)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

### 2. Web Frontend

```bash
cd web_client

# Install Node dependencies
npm install

# Start the React dev server
npm start
```

The web app will open at `http://localhost:3000`. Log in with the superuser credentials you created.

### 3. Desktop Client

```bash
cd desktop_client

# Install Python dependencies (if not already in venv)
pip install PyQt5 matplotlib requests

# Run the desktop app
python app.py
```

A login dialog will appear — enter your Django superuser credentials and the app will connect to `http://localhost:8000/api/`.

## API Endpoints

All endpoints require authentication (Token or Basic). Obtain a token via:

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload/` | Upload a CSV file (multipart, field: `file`) |
| GET | `/api/history/` | List last 5 uploaded datasets |
| GET | `/api/summary/?id=<id>` | Get summary JSON for a dataset |
| GET | `/api/chart-data/?id=<id>` | Get chart-ready data (labels, counts, averages, rows) |
| GET | `/api/report/?id=<id>` | Download a PDF report |
| POST | `/api/auth/token/` | Get auth token |

### Example: Upload via curl

```bash
TOKEN="your-token-here"

curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Token $TOKEN" \
  -F "file=@sample_equipment_data.csv"
```

### Example: Get history

```bash
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/history/
```

### Example: Download PDF

```bash
curl -H "Authorization: Token $TOKEN" \
  http://localhost:8000/api/report/?id=1 \
  --output report.pdf
```

## Sample CSV Format

The CSV file should have these columns:

```
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
...
```

A sample file (`sample_equipment_data.csv`) is included in the project root.

## Features

- **Upload CSV** — Upload equipment data CSV files through web or desktop UI
- **Summary Stats** — View total count, parameter averages, and type distribution
- **Charts** — Bar chart for type distribution, radar chart for parameter averages
- **Data Table** — View all equipment rows in a responsive, scrollable table
- **Upload History** — Browse the last 5 uploads and reload any past dataset
- **PDF Reports** — Generate and download PDF reports with summary and tables
- **Dark Mode** — Toggle dark/light theme on web; desktop is dark-only
- **Authentication** — Token-based auth protects all API endpoints

## Railway Deployment (Backend)

1. Push the `backend/` folder to a GitHub repository.

2. Create a new project on [Railway](https://railway.app) and connect the repo.

3. Set these environment variables in Railway:
   ```
   DJANGO_SECRET_KEY=your-random-secret-key
   DEBUG=0
   ALLOWED_HOSTS=your-app.railway.app,localhost
   ```

4. Railway will detect the `Procfile` and run gunicorn automatically.

5. After deploy, run migrations via Railway CLI or console:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

6. Update `API_BASE` in `web_client/src/App.js` and `desktop_client/app.py` to point to your Railway URL.

## Demo Video Script (2–3 min)

1. **Intro (15s)**: Show the project structure in your editor. Briefly mention the tech stack.
2. **Backend (30s)**: Start the Django server. Show a curl command uploading the sample CSV and getting a summary response.
3. **Web UI (60s)**: Open the React app. Log in. Upload the sample CSV. Show the summary panel, data table, bar chart, and radar chart. Toggle dark mode. Click a history item to reload a past upload. Download a PDF report.
4. **Desktop App (45s)**: Launch the PyQt5 app. Log in via the auth dialog. Upload the CSV. Show the table and Matplotlib charts. Download a PDF.
5. **Wrap-up (15s)**: Mention Railway deployment and summarize the features.
