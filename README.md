# ⌨️ KeyTrack Pro --- Keyboard & Mouse Activity Analytics (Django)

KeyTrack Pro is a web-based analytics platform that tracks and
visualizes keyboard and mouse interactions to provide insights about
productivity, behavior and ergonomics.

The system collects user interaction events, stores them, and displays
them through an interactive dashboard with heatmaps and statistics.

------------------------------------------------------------------------

## 🎯 Project Goal

Transform raw user interaction data into meaningful visual insights.

Examples: - Which keys are most used? - Where users click the most? -
Typing speed & patterns - Mouse movement behavior

------------------------------------------------------------------------

## 🏗 Architecture

Tracking Agent → Django Backend → Database → Interactive Dashboard

-   Data Collection: Python event listeners
-   Backend: Django
-   Database: SQLite
-   Visualization: Chart.js + Heatmap.js

------------------------------------------------------------------------

## 🧠 Features

### Keyboard Analytics

-   Keyboard heatmap
-   Usage by day of week
-   Typing speed analysis
-   Key combination statistics

### Mouse Analytics

-   Click heatmap
-   Movement heatmap
-   Click frequency by button

### Dashboard

-   Date filters
-   Interactive charts
-   Aggregated statistics

------------------------------------------------------------------------

## 🛠 Technologies

Backend: - Python - Django

Frontend: - HTML - CSS - JavaScript - Chart.js - Heatmap.js

Database: - SQLite

------------------------------------------------------------------------

## 📁 Project Modules

-   Event Tracking Service
-   Data Storage Models
-   Analytics Engine
-   Visualization Dashboard

------------------------------------------------------------------------

## 🚀 How to Run

1.  Install dependencies pip install -r requirements.txt

2.  Run migrations python manage.py migrate

3.  Start server python manage.py runserver

4.  Open browser http://127.0.0.1:8000

------------------------------------------------------------------------

## 📊 Use Cases

-   Productivity analysis
-   UX research
-   Ergonomic studies
-   Behavior analytics

------------------------------------------------------------------------

## 🔮 Future Improvements

-   Real-time tracking
-   User profiles
-   Data export (CSV/PDF)
-   Advanced analytics

------------------------------------------------------------------------

## 👨‍💻 Authors

Ismail Boulaich

