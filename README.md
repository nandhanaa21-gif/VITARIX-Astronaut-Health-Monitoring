# VITARIX-Astronaut-Health-Monitoring
An astronaut health monitoring system for tracking physical health, mental wellness, health analytics and wellness alerts.
# 🚀 VITARIX – Astronaut Health Monitoring System

### Supporting Astronaut Health and Well-being During Space Missions

VITARIX is a web-based Astronaut Health Monitoring System designed to monitor and analyze the physical health and mental well-being of astronauts during space missions.

The system provides a centralized dashboard where astronaut health information can be recorded, monitored, and analyzed. It helps identify potential wellness concerns through rule-based health assessments, visual analytics, alerts, and personalized recommendations.

VITARIX aims to support astronaut well-being by making health information easier to understand and monitor.

---

## 🌌 Project Overview

Astronauts experience challenging conditions during space missions, including changes in sleep patterns, physical activity, stress levels, and overall well-being.

Monitoring these factors is important for maintaining astronaut health throughout a mission.

VITARIX provides a digital monitoring platform that brings physical health tracking, mental wellness check-ins, health analytics, and wellness alerts together in one dashboard.

The system uses manually submitted health information and rule-based analysis to generate monitoring insights.

---

## ✨ Key Features

### 👨‍🚀 1. Astronaut Profile Management
- Register astronaut information.
- Record astronaut ID, age, gender, and mission details.
- View astronaut mission status and profile information.

### ❤️ 2. Physical Health Monitoring
Monitor important physical health parameters, including:
- Heart rate
- Body temperature
- Blood pressure
- Sleep duration

### 🧠 3. Mental Wellness Monitoring
Record and monitor mental wellness information:
- Mood check-ins
- Stress levels
- Sleep quality
- Personal wellness notes

### 📊 4. Health Analytics Dashboard
- Visualize health trends using interactive charts.
- Monitor heart rate variations.
- Analyze temperature and sleep patterns.
- Track stress-level trends.
- View submitted health records.

### ⚠️ 5. Rule-Based Risk Assessment
VITARIX uses predefined health monitoring rules to identify potential wellness concerns.

The system considers:
- Heart rate readings
- Body temperature
- Sleep duration
- Stress levels
- Mood and sleep quality

Based on the submitted information, it generates a risk score, risk level, and relevant observations.

### 🔔 6. Wellness Alerts
- Identify unusual submitted health readings.
- Highlight physical and mental wellness concerns.
- Display alerts to help users recognize areas that may need attention.

### 💡 7. Personalized Wellness Recommendations
Provides recommendations based on submitted health information to encourage better sleep habits, stress management, and general well-being.

### 🫀 8. Interactive Body Model
An interactive body model allows users to explore selected body systems, including:
- Brain
- Heart
- Lungs
- Muscles

### 📄 9. PDF Health Report
Generate and download a health report containing relevant submitted health information and monitoring results.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Database management |
| HTML5 | Website structure |
| CSS3 | Website styling |
| JavaScript | Interactive functionality |
| Chart.js | Health data visualization |

---

## 🏗️ System Architecture

The VITARIX application follows a simple web application architecture.

**User Input → Flask Backend → SQLite Database → Health Analysis → Dashboard and Reports**

1. Users enter astronaut profile and health information through the website.
2. Flask processes the submitted information.
3. SQLite stores the health records.
4. Rule-based logic evaluates the submitted health information.
5. The dashboard displays monitoring results, alerts, charts, and recommendations.

---

## 📂 Project Structure

```text
VITARIX/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
└── database/
    └── vitarix.db
```

The database file is created locally by the application when required. It is not included in the public repository.

---
