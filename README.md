[![Live Demo](https://img.shields.io/badge/🌐%20Live-Demo-green?style=for-the-badge)](https://trashtrack.pythonanywhere.com)

TrashTrack is an AI-powered **smart bin system** designed to efficiently manage waste using **machine learning** and IoT. The system detects waste types, monitors fill levels, and integrates with a web application for real-time tracking, waste collection, and company waste purchasing.


# 🚀 TrashTrack - Smart Waste Management System

TrashTrack is an AI-powered **smart bin system** designed to efficiently manage waste using **machine learning** and IoT. The system detects waste types, monitors fill levels, and integrates with a web application for real-time tracking, waste collection, and company waste purchasing.

## 🏗 Features
- 🗑 **Smart Bins**: ML-based waste detection and fill level monitoring.
- 📍 **Map Integration**: Displays bin locations with latitude & longitude.
- 🚛 **Waste Collection System**: Optimized vehicle routes based on bin status.
- ♻ **Dumping Area Management**: Waste categorization for recycling or disposal.
- 🏢 **Company Portal**: Businesses can purchase waste via a simulated payment system.
- 🔔 **Notification System**: Alerts for full bins.
- 🔧 **Admin Panel**: Manual data management.

## 📂 Project Structure
```
ML Model/
│── combined.ipynb
│── index.py
TrashTrack/
│── mainapp/          # Core Django app
│── static/           # Static files
│── templates/        # HTML templates
│── trashtrack/       # Django project settings
│── db.sqlite3        # Database file
│── manage.py         # Django management script
│── requirements.txt  # Python dependencies
README.md             # Project guide
```

## ⚙️ Setup Instructions

### 1️⃣ Create a Virtual Environment
```bash
python -m venv venv
```

### 2️⃣ Activate the Virtual Environment

- **On Windows:**
```bash
venv\Scripts\activate
```

- **On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
pip install django-jazzmin
```

### 4️⃣ Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Run the Development Server
```bash
python manage.py runserver
```

The app will be live at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🧠 ML Model Download

To run the smart waste classification system, download the pre-trained machine learning model from the link below:

📥 [Download ML Model](https://drive.google.com/file/d/14vusReS36Gr3K_pz9EXxIToher9N0tB3/view?usp=drive_link)

## Contributors
- [Saurabh Singh](https://github.com/Saurabh-Singh02) – Backend & ML Model
- [Rishabh Sharma](https://github.com/StudentRishabhSharma) – Frontend, Debugging & Documentation

## 👥 Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Saurabh-Singh02">
        <img src="https://github.com/Saurabh-Singh02.png" width="70px;" alt="Saurabh Singh"/>
        <br /><sub><b>Saurabh Singh</b></sub>
      </a>
      <br />Backend & ML Model Training
    </td>
    <td align="center">
      <a href="https://github.com/StudentRishabhSharma">
        <img src="https://github.com/StudentRishabhSharma.png" width="70px;" alt="Rishabh Sharma"/>
        <br /><sub><b>Rishabh Sharma</b></sub>
      </a>
      <br />Frontend, Debugging & Documentation
    </td>
  </tr>
</table>









