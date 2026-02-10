# CSV Visualizer

Upload and analyze equipment data from CSV files. Built as both a web app and a desktop client.

## What it does

This tool lets you upload CSV files with equipment data and automatically generates charts and statistics. You get both a web interface (React) and a desktop app (PyQt5) that connect to the same Django backend.

Main features:
- Upload CSV files and see instant analysis
- Auto-calculated averages for flowrate, pressure, temperature
- Modern Doughnut and Line charts
- Download PDF reports with all your data
- Keeps history of your last 5 uploads (auto-cleanup)
- Dark mode support in the web version
- Modern Desktop Client with dark theme

## Tech used

**Backend**: Django + DRF  
**Web**: React + Chart.js  
**Desktop**: PyQt5 + Matplotlib  
**Database**: SQLite  
**Misc**: Pandas for data processing, ReportLab for PDFs

## Setup

You'll need Python 3.9+ and Node.js 18+.

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # optional, for admin panel
python manage.py runserver
```

Server runs on `http://localhost:8000`
If you make a superuser, you can access it on `http://localhost:8000/admin`
### Web Client

```bash
cd web_client
npm install
npm start
```

Opens at `http://localhost:3000`

### Desktop Client

```bash
cd desktop_client
pip install PyQt5 matplotlib requests
python app.py
```

## API Reference

| Endpoint | What it does |
|----------|-------------|
| `POST /api/auth/register/` | Create new account |
| `POST /api/auth/token/` | Login and get token |
| `POST /api/upload/` | Upload CSV file |
| `GET /api/history/` | Get last 5 uploads |
| `GET /api/summary/?id=` | Get stats for a dataset |
| `GET /api/chart-data/?id=` | Get chart data + table rows |
| `GET /api/report/?id=` | Download PDF report |

## CSV Format

Your CSV should have these columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,25.3,45.2
Reactor-001,Reactor,0,15.8,180.5
```

There's a sample file included (`sample_equipment_data.csv`) you can use for testing.

## Project Structure

```
csv_visualizer/
├── backend/
│   ├── app_core/         # models, views, etc
│   ├── visualizer_api/   # settings
│   └── requirements.txt
├── web_client/
│   ├── src/
│   │   ├── components/
│   │   └── styles/
│   └── package.json
├── desktop_client/
│   ├── app.py
│   └── components/
└── sample_equipment_data.csv
```

## Notes

- The web app has dark mode (toggle in header)
- Desktop app is dark by default
- History only keeps last 5 datasets per cleanup
- PDF reports include all tables and stats
- Admin panel available at `/admin/` if you created a superuser

## Demo

You can watch a full product demo of both the web and desktop applications here:
[**📺 Watch Demo Video (Google Drive)**](https://drive.google.com/file/d/1mvGkjmYd6iVU71kGSUw0UoR45m-tCyiW/view?usp=sharing)

## Screenshots

### Web Application

![Login Page](./screenshots/login.png)

![Dashboard](./screenshots/dashboard.png)

![Charts](./screenshots/charts.png)

### Desktop Application

![Desktop Login](./screenshots/desktop_login.png)

![Desktop Dashboard](./screenshots/desktop_dashboard.png)

![Desktop Charts](./screenshots/desktop_charts.png)

## Contact

Built by Nrishan Jyoti Das  
Email: nrishan@proton.me

---

**Thank you for reviewing this submission!**
