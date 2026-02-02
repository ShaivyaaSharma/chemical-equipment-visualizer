# 🧪 Chemical Equipment Parameter Visualizer

The **Chemical Equipment Parameter Visualizer** is a full-stack hybrid application (Web + Desktop) built to simplify the way chemical equipment data is analyzed and understood.

Instead of working with raw CSV files, logs, or large tables, this system converts equipment datasets into **clear visual dashboards, charts, summaries, and downloadable reports**. The goal is to make technical data more readable, meaningful, and actionable for users.

---

##  Why This Project Exists

Chemical equipment generates a lot of structured data, but reading it in raw form is inefficient and error-prone. This project focuses on:

- Making equipment parameters easy to **visualize**
- Supporting both **web and desktop** users
- Allowing quick **CSV uploads and analysis**
- Generating **professional PDF reports**
- Keeping the system scalable and easy to deploy

---

## Technologies & Frameworks

### Backend
- **Django & Django REST Framework**: Powers the robust API, handling authentication, data ingestion, and business logic.
- **Pandas & NumPy**: Used for high-performance CSV parsing and statistical analysis.
- **SQLite**: A lightweight, file-based database for easy setup and portability.
- **ReportLab**: For generating PDF reports programmatically.
- **Gunicorn & WhiteNoise**: Production-grade server and static file handling.

### Frontend Web
- **React.js**: A high-performance library for building dynamic user interfaces.
- **Chart.js**: Renders interactive, responsive charts.
- **Axios**: Handles secure API communication.
- **jspdf & html2canvas**: Client-side PDF creation.

### Frontend Desktop
- **PyQt5**: Native, OS-integrated graphical user interface.
- **Matplotlib**: Publication-quality static charts for desktop reports.
- **Requests**: Manages session-based authentication.

---

## File Structure

```text
chemical-equipment-visualizer/
├── backend/
│   ├── api/
│   │   ├── models.py        # Database schema
│   │   ├── views.py         # API logic & endpoints
│   │   ├── urls.py          # URL routing
│   │   └── serializer.py    # Data conversion
│   ├── backend/
│   │   └── settings.py      # Django configuration
│   ├── manage.py            # Django entry point
│   └── requirements.txt     # Python dependencies
│
├── frontend-web/
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── App.js           # Main application component
│   │   └── App.css          # Global styles
│   └── package.json         # Node dependencies & scripts
│
├── frontend-desktop/
│   ├── components/
│   │   ├── auth.py          # Login/Signup logic
│   │   ├── dashboard.py     # Visualizations & stats
│   │   ├── reports.py       # PDF generation logic
│   │   └── charts.py        # Matplotlib integrations
│   ├── main.py              # Desktop app entry point
│   └── requirements.txt     # Desktop-specific dependencies
│
├── README.md                # Project documentation
├── package.json             # Root configuration & scripts
└── remove_bg.py             # Utility script
```

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd chemical-equipment-visualizer
```

### 2. Install Root Dependencies
```bash
npm install
```

### 3. Setup Backend (Django)
```bash
cd backend
python3 -m venv venv
# Activate Virtual Env
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

pip install -r requirements.txt
python3 manage.py migrate
python3 create_superuser.py  # Creates admin user
deactivate
cd ..
```

### 4. Setup Frontend Web (React)
```bash
cd frontend-web
npm install
cd ..
```

### 5. Setup Frontend Desktop (PyQt5)
```bash
cd frontend-desktop
python3 -m venv venv
# Activate Virtual Env
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

pip install -r requirements.txt
deactivate
cd ..
```

---

## How to Run

### Option A: One-Command Start (Recommended)
Run Backend, Web App, and Desktop App simultaneously:
```bash
npm run dev:all
```
- **Web App**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Desktop App**: Launches automatically.

### Option B: Run Individually

**Backend**:
```bash
source backend/venv/bin/activate
python backend/manage.py runserver
```

**Web App**:
```bash
cd frontend-web
npm start
```

**Desktop App**:
```bash
source frontend-desktop/venv/bin/activate
python frontend-desktop/main.py
```

---

## Key Features

- **CSV Upload & Validation**: Automatically validates and processes chemical equipment datasets.
- **Interactive Dashboards**: Real-time charts and summaries via the Web UI.
- **PDF Report Generation**: Downloadable reports with visual insights.
- **Cross-Platform Access**: Unified backend for both web and desktop experiences.
- **Secure Authentication**: User-based data isolation for privacy and security.

---
*Verified & Maintained by the Chemical Equipment Visualizer Team.*