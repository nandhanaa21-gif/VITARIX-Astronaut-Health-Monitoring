
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import os
from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


app = Flask(__name__)
app.secret_key = "vitarix_demo_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "vitarix.db")


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


# ==================================================
# CREATE DATABASE
# ==================================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            heart_rate REAL,
            temperature REAL,
            blood_pressure TEXT,
            sleep REAL,
            submitted_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mental_health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT,
            stress_level INTEGER,
            sleep_quality TEXT,
            notes TEXT,
            submitted_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS astronaut_profile (
            id INTEGER PRIMARY KEY,
            astronaut_name TEXT,
            astronaut_id TEXT,
            age INTEGER,
            gender TEXT,
            mission_name TEXT,
            mission_duration TEXT,
            mission_status TEXT
        )
    """)

    # Handle older databases without timestamp columns
    for table in ("health_records", "mental_health_records"):

        columns = [
            row["name"]
            for row in cursor.execute(
                f"PRAGMA table_info({table})"
            ).fetchall()
        ]

        if "submitted_at" not in columns:
            cursor.execute(
                f"ALTER TABLE {table} ADD COLUMN submitted_at TEXT"
            )

    conn.commit()
    conn.close()


# ==================================================
# PHYSICAL HEALTH ANALYSIS
# ==================================================

def analyze_health(record):

    alerts = []

    if not record:
        return alerts

    heart_rate = float(record["heart_rate"])
    temperature = float(record["temperature"])
    sleep = float(record["sleep"])

    if heart_rate < 50 or heart_rate > 100:
        alerts.append(
            f"Heart rate reading ({heart_rate:g} BPM) is outside the demo reference range."
        )

    if temperature < 36 or temperature > 37.5:
        alerts.append(
            f"Temperature reading ({temperature:g} °C) is outside the demo reference range."
        )

    if sleep < 6:
        alerts.append(
            f"Sleep duration ({sleep:g} hours) is below the 6-hour demo threshold."
        )

    return alerts


# ==================================================
# MENTAL HEALTH ANALYSIS
# ==================================================

def analyze_mental_health(record):

    alerts = []

    if not record:
        return alerts

    if int(record["stress_level"]) >= 8:
        alerts.append(
            "High stress level reported. Consider a relaxation break."
        )

    if record["mood"] in ("Sad", "Anxious"):
        alerts.append(
            f"Mood check-in recorded as {record['mood'].lower()}. Consider emotional support."
        )

    if record["sleep_quality"] == "Poor":
        alerts.append(
            "Poor sleep quality reported."
        )

    return alerts


# ==================================================
# RULE-BASED RISK ASSESSMENT
# ==================================================

def calculate_risk(physical, mental):

    score = 0
    reasons = []

    if not physical and not mental:

        return {
            "level": "No Data",
            "score": 0,
            "reasons": [],
            "recommendation": "Submit a health check-in to view the demo risk assessment."
        }

    if physical:

        heart_rate = float(physical["heart_rate"])
        temperature = float(physical["temperature"])
        sleep = float(physical["sleep"])

        if heart_rate < 50 or heart_rate > 100:
            score += 2
            reasons.append("Heart rate outside demo reference range")

        if temperature < 36 or temperature > 37.5:
            score += 2
            reasons.append("Temperature outside demo reference range")

        if sleep < 6:
            score += 1
            reasons.append("Sleep duration below 6 hours")

    if mental:

        if int(mental["stress_level"]) >= 8:
            score += 2
            reasons.append("High stress level reported")

        if mental["mood"] in ("Sad", "Anxious"):
            score += 1
            reasons.append("Mood check-in needs attention")

        if mental["sleep_quality"] == "Poor":
            score += 1
            reasons.append("Poor sleep quality reported")

    if score == 0:

        level = "Low"

        recommendation = (
            "Continue regular health check-ins and maintain healthy routines."
        )

    elif score <= 2:

        level = "Moderate"

        recommendation = (
            "Review the reported readings and consider rest, hydration, "
            "and a follow-up check-in."
        )

    else:

        level = "High"

        recommendation = (
            "Several check-in indicators need attention. "
            "Seek review from the mission medical team."
        )

    return {
        "level": level,
        "score": score,
        "reasons": reasons,
        "recommendation": recommendation
    }


# ==================================================
# PERSONALIZED WELLNESS RECOMMENDATIONS
# ==================================================

def get_wellness_recommendations(physical, mental):

    recommendations = []

    if not physical and not mental:

        return [
            "Submit a physical and mental wellness check-in to receive suggestions."
        ]

    if physical:

        heart_rate = float(physical["heart_rate"])
        temperature = float(physical["temperature"])
        sleep = float(physical["sleep"])

        if heart_rate < 50 or heart_rate > 100:

            recommendations.append(
                "Heart rate: Review this reading with the mission medical team."
            )

        else:

            recommendations.append(
                "Heart health: Continue appropriate exercise and routine monitoring."
            )

        if temperature < 36 or temperature > 37.5:

            recommendations.append(
                "Temperature: Recheck the reading and report persistent unusual values."
            )

        if sleep < 6:

            recommendations.append(
                "Sleep: Try to maintain a consistent rest schedule and discuss "
                "ongoing sleep difficulties with the medical team."
            )

        else:

            recommendations.append(
                "Sleep: Maintain a consistent sleep and wake routine."
            )

    if mental:

        if int(mental["stress_level"]) >= 8:

            recommendations.append(
                "Stress: Consider a guided breathing exercise or a short relaxation break."
            )

        if mental["mood"] in ("Sad", "Anxious"):

            recommendations.append(
                "Mood: Consider speaking with a trusted crew member or mission support professional."
            )

        if mental["sleep_quality"] == "Poor":

            recommendations.append(
                "Sleep quality: Reduce distractions before rest and report persistent sleep problems."
            )

        if (
            int(mental["stress_level"]) < 8
            and mental["mood"] not in ("Sad", "Anxious")
            and mental["sleep_quality"] != "Poor"
        ):

            recommendations.append(
                "Mental wellness: Continue regular mood check-ins and healthy crew communication."
            )

    recommendations.append(
        "General wellness: Stay hydrated, follow mission routines, "
        "and report concerning symptoms to the medical team."
    )

    return recommendations


# ==================================================
# HOME / DASHBOARD
# ==================================================

@app.route("/")
def home():

    conn = get_connection()

    physical_rows = conn.execute("""
        SELECT * FROM health_records
        ORDER BY id DESC
    """).fetchall()

    mental_rows = conn.execute("""
        SELECT * FROM mental_health_records
        ORDER BY id DESC
    """).fetchall()

    profile = conn.execute("""
        SELECT * FROM astronaut_profile
        WHERE id = 1
    """).fetchone()

    conn.close()

    # IMPORTANT FIX:
    # Convert SQLite Row objects into normal dictionaries.
    # This allows Flask/Jinja to serialize chart data using tojson.

    records = [dict(row) for row in physical_rows]

    mental_records = [dict(row) for row in mental_rows]

    # Convert profile separately for consistent template handling.
    profile = dict(profile) if profile else None

    latest_physical = records[0] if records else None

    latest_mental = mental_records[0] if mental_records else None

    physical_alerts = analyze_health(latest_physical)

    mental_alerts = analyze_mental_health(latest_mental)

    risk = calculate_risk(
        latest_physical,
        latest_mental
    )

    recommendations = get_wellness_recommendations(
        latest_physical,
        latest_mental
    )

    return render_template(
        "index.html",
        records=records,
        mental_records=mental_records,
        profile=profile,
        risk=risk,
        physical_alerts=physical_alerts,
        mental_alerts=mental_alerts,
        recommendations=recommendations
    )


# ==================================================
# SAVE ASTRONAUT PROFILE
# ==================================================

@app.route("/save_profile", methods=["POST"])
def save_profile():

    name = request.form.get(
        "astronaut_name", ""
    ).strip()

    astronaut_id = request.form.get(
        "astronaut_id", ""
    ).strip()

    age_value = request.form.get(
        "age", ""
    ).strip()

    gender = request.form.get(
        "gender", "Prefer not to say"
    )

    mission_name = request.form.get(
        "mission_name", ""
    ).strip()

    duration = request.form.get(
        "mission_duration", ""
    ).strip()

    status = request.form.get(
        "mission_status", "Training"
    )

    if not name or not astronaut_id or not age_value or not mission_name:

        flash(
            "Please fill in all required profile details.",
            "error"
        )

        return redirect(url_for("home") + "#profile")

    try:

        age = int(age_value)

        if age < 1 or age > 120:
            raise ValueError

    except ValueError:

        flash(
            "Please enter a valid age.",
            "error"
        )

        return redirect(url_for("home") + "#profile")

    if gender not in (
        "Female",
        "Male",
        "Other",
        "Prefer not to say"
    ):

        gender = "Prefer not to say"

    if status not in (
        "Training",
        "In Progress",
        "Completed"
    ):

        status = "Training"

    conn = get_connection()

    conn.execute("""
        INSERT OR REPLACE INTO astronaut_profile
        (
            id,
            astronaut_name,
            astronaut_id,
            age,
            gender,
            mission_name,
            mission_duration,
            mission_status
        )
        VALUES (1, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        astronaut_id,
        age,
        gender,
        mission_name,
        duration,
        status
    ))

    conn.commit()
    conn.close()

    flash(
        "Astronaut profile saved successfully!",
        "success"
    )

    return redirect(url_for("home") + "#profile")


# ==================================================
# SUBMIT PHYSICAL AND MENTAL HEALTH
# ==================================================

@app.route("/submit_complete", methods=["POST"])
def submit_complete():

    try:

        heart_rate = float(request.form["heart_rate"])

        temperature = float(request.form["temperature"])

        blood_pressure = request.form["blood_pressure"].strip()

        sleep = float(request.form["sleep"])

        mood = request.form["mood"]

        stress_level = int(request.form["stress_level"])

        sleep_quality = request.form["sleep_quality"]

        notes = request.form.get(
            "notes", ""
        ).strip()

        # Validate values

        if not 20 <= heart_rate <= 250:
            raise ValueError(
                "Heart rate must be between 20 and 250."
            )

        if not 25 <= temperature <= 45:
            raise ValueError(
                "Temperature must be between 25 and 45 °C."
            )

        if not 0 <= sleep <= 24:
            raise ValueError(
                "Sleep duration must be between 0 and 24 hours."
            )

        if not 1 <= stress_level <= 10:
            raise ValueError(
                "Stress level must be between 1 and 10."
            )

        if mood not in (
            "Happy", "Neutral", "Sad", "Anxious"
        ):
            raise ValueError("Invalid mood selection.")

        if sleep_quality not in (
            "Good", "Average", "Poor"
        ):
            raise ValueError("Invalid sleep quality.")

        if not blood_pressure:
            raise ValueError("Please enter blood pressure.")

        timestamp = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        conn = get_connection()

        try:

            conn.execute("""
                INSERT INTO health_records
                (
                    heart_rate,
                    temperature,
                    blood_pressure,
                    sleep,
                    submitted_at
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                heart_rate,
                temperature,
                blood_pressure,
                sleep,
                timestamp
            ))

            conn.execute("""
                INSERT INTO mental_health_records
                (
                    mood,
                    stress_level,
                    sleep_quality,
                    notes,
                    submitted_at
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                mood,
                stress_level,
                sleep_quality,
                notes,
                timestamp
            ))

            conn.commit()

        except sqlite3.Error:
            conn.rollback()
            raise

        finally:
            conn.close()

        flash(
            "Physical and mental health records saved successfully!",
            "success"
        )

    except (ValueError, KeyError) as error:

        flash(
            f"Please check your entries: {error}",
            "error"
        )

    except sqlite3.Error:

        flash(
            "Database error. Please try again.",
            "error"
        )

    return redirect(url_for("home") + "#dashboard")


# ==================================================
# DOWNLOAD HEALTH REPORT PDF
# ==================================================

@app.route("/download_report")
def download_report():

    conn = get_connection()

    physical = conn.execute("""
        SELECT * FROM health_records
        ORDER BY id DESC LIMIT 1
    """).fetchone()

    mental = conn.execute("""
        SELECT * FROM mental_health_records
        ORDER BY id DESC LIMIT 1
    """).fetchone()

    profile = conn.execute("""
        SELECT * FROM astronaut_profile
        WHERE id = 1
    """).fetchone()

    conn.close()

    risk = calculate_risk(
        physical,
        mental
    )

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "VITARIX - Astronaut Health Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 16))

    def add_line(label, value):

        safe_value = escape(
            str(
                value if value not in (None, "")
                else "Not available"
            )
        )

        story.append(
            Paragraph(
                f"<b>{escape(label)}:</b> {safe_value}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 7))

    # Astronaut Profile

    story.append(
        Paragraph(
            "Astronaut Profile",
            styles["Heading2"]
        )
    )

    if profile:

        add_line("Name", profile["astronaut_name"])

        add_line("Astronaut ID", profile["astronaut_id"])

        add_line("Age", profile["age"])

        add_line("Gender", profile["gender"])

        add_line("Mission", profile["mission_name"])

        add_line("Mission Duration", profile["mission_duration"])

        add_line("Mission Status", profile["mission_status"])

    else:

        add_line(
            "Profile",
            "No astronaut profile saved"
        )

    story.append(Spacer(1, 10))

    # Physical Health

    story.append(
        Paragraph(
            "Physical Health",
            styles["Heading2"]
        )
    )

    if physical:

        add_line(
            "Heart Rate",
            f'{physical["heart_rate"]} BPM'
        )

        add_line(
            "Temperature",
            f'{physical["temperature"]} °C'
        )

        add_line(
            "Blood Pressure",
            physical["blood_pressure"]
        )

        add_line(
            "Sleep",
            f'{physical["sleep"]} hours'
        )

        add_line(
            "Submitted At",
            physical["submitted_at"]
        )

    else:

        add_line(
            "Physical Record",
            "No data available"
        )

    story.append(Spacer(1, 10))

    # Mental Wellness

    story.append(
        Paragraph(
            "Mental Wellness",
            styles["Heading2"]
        )
    )

    if mental:

        add_line("Mood", mental["mood"])

        add_line(
            "Stress Level",
            f'{mental["stress_level"]}/10'
        )

        add_line(
            "Sleep Quality",
            mental["sleep_quality"]
        )

        add_line("Notes", mental["notes"])

        add_line(
            "Submitted At",
            mental["submitted_at"]
        )

    else:

        add_line(
            "Mental Record",
            "No data available"
        )

    story.append(Spacer(1, 10))

    # Risk Assessment

    story.append(
        Paragraph(
            "Demo Risk Assessment",
            styles["Heading2"]
        )
    )

    add_line(
        "Risk Level",
        risk["level"]
    )

    add_line(
        "Score",
        risk["score"]
    )

    add_line(
        "Reasons",
        ", ".join(risk["reasons"]) or "No demo alerts"
    )

    add_line(
        "Recommendation",
        risk["recommendation"]
    )

    story.append(Spacer(1, 16))

    story.append(
        Paragraph(
            "Disclaimer: This report uses manually entered "
            "demonstration data and simple rule-based checks. "
            "It is not a medical diagnosis and does not represent "
            "live spacecraft sensor readings.",
            styles["Italic"]
        )
    )

    document.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="VITARIX_Health_Report.pdf",
        mimetype="application/pdf"
    )


# ==================================================
# INITIALIZE DATABASE
# ==================================================

# This runs when the application starts, including on Render.
create_database()


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)

