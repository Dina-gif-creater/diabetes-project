# 🩺 DiabetesGuard AI

## What Is This?

**DiabetesGuard AI** is a multi-page web application that predicts a personalised diabetes risk score (0–100) using a Random Forest machine learning model trained on real health data. Users register, fill in their health details, receive an AI-generated risk score with charts, personalised recommendations, and can download a professional PDF health report.

---

## Live Demo Flow

```
Login Page  →  Register  →  Health Details Form  →  Results & Charts  →  PDF Download
```

---

## Features

| Feature | Description |
|---|---|
| 🔐 Login / Register | Secure user accounts stored locally with SHA-256 hashed passwords |
| 📋 Health Profile Form | 16 health inputs across personal, body, lifestyle, and medical sections |
| 🤖 AI Risk Prediction | Random Forest Regressor predicts a 0–100 diabetes risk score |
| 📊 Risk Gauge Chart | Interactive Plotly gauge showing risk level with colour zones |
| 🔬 Feature Importance Chart | Horizontal bar chart showing what factors affected the score most |
| 🕸 Health Radar Chart | Spider/radar chart showing overall health profile |
| 💡 Personalised Tips | Dynamic recommendations based on individual inputs |
| 📄 PDF Report Download | Professional downloadable report with patient data, result, and tips |
| 🌙 Dark UI | Modern dark-themed interface with glassmorphism cards |

---

## Project Structure

```
diabetes-predictor/
│
├── app.py                 ← Main Streamlit application (all 5 pages)
├── train_model.py         ← Script to train and save the ML model
├── diabetes_data.csv      ← Dataset (your uploaded file)
├── model.pkl              ← Saved ML model (created by train_model.py)
├── features.pkl           ← Saved feature list (created by train_model.py)
├── users_db.json          ← User accounts (created automatically on first run)
├── requirements.txt       ← Python dependencies
└── README.md              ← This file
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Frontend / UI | Streamlit |
| Machine Learning | Scikit-learn (Random Forest Regressor) |
| Charts | Plotly |
| PDF Generation | ReportLab |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib |
| Auth Storage | JSON file + SHA-256 hashing |

---

## Dataset

The app uses a custom diabetes health dataset (`diabetes_data.csv`) with the following columns:

| Column | Description |
|---|---|
| `weight` | Body weight in kg |
| `height` | Height in cm |
| `blood_glucose` | Fasting blood glucose in mg/dL |
| `physical_activity` | Daily exercise in minutes |
| `diet` | Diet quality (1 = healthy, 0 = unhealthy) |
| `medication_adherence` | Medication taken regularly (1 = yes, 0 = no) |
| `stress_level` | Stress level (0 = low, 1 = medium, 2 = high) |
| `sleep_hours` | Average sleep hours per night |
| `hydration_level` | Adequate daily water intake (1 = yes, 0 = no) |
| `bmi` | Body Mass Index (auto-calculated) |
| `risk_score` | **Target variable** — diabetes risk score from 0 to 100 |

---

## Quick Start

### Step 1 — Clone or Download

```bash
git clone https://github.com/YOUR_USERNAME/diabetes-guard-ai.git
cd diabetes-guard-ai
```

Or just download the zip and unzip it.

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Train the ML Model

> Run this **once** before starting the app.

```bash
python train_model.py
```

Expected output:
```
Loading dataset...
Shape: (1000, 11)
MAE: 4.29  |  R2: 0.897
model.pkl and features.pkl saved successfully!
Now run: streamlit run app.py
```

### Step 4 — Run the App

```bash
streamlit run app.py
```

Your browser opens automatically at **http://localhost:8501**

---

## How to Use

1. **Open the app** — Go to `http://localhost:8501` in your browser
2. **Register** — Click "Create New Account", fill in username, email, password
3. **Sign In** — Log in with your credentials
4. **Fill Health Details** — Enter your name, age, weight, height, glucose, lifestyle info
5. **View Results** — See your risk score, gauge chart, factor chart, and radar chart
6. **Read Tips** — Get personalised health recommendations
7. **Download Report** — Click the green button to download your PDF health report

---

## Model Details

| Property | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Number of Trees | 100 |
| Input Features | 10 health parameters |
| Output | Risk Score (0 to 100) |
| Train / Test Split | 80% / 20% |
| R² Score | ~0.90 |
| Mean Absolute Error | ~4.3 points |

### Risk Score Interpretation

| Score Range | Risk Level | Meaning |
|---|---|---|
| 0 – 29 | 🟢 LOW RISK | Healthy habits, keep it up |
| 30 – 59 | 🟡 MODERATE RISK | Some risk factors present, take action |
| 60 – 100 | 🔴 HIGH RISK | Multiple risk factors, consult a doctor |

---

## Screenshots

### Login Page
- Clean dark UI with email/password login
- Feature highlights shown below

### Health Details Form
- 4 sections: Personal Info, Body Measurements, Lifestyle, Medical Background
- Real-time BMI calculation and glucose range indicator

### Results Page
- 5 metric cards (Risk Score, Safety Score, BMI, Glucose, Sleep)
- 3 interactive Plotly charts (Gauge, Bar, Radar)
- Personalised tip cards

### PDF Report
- Blue-themed professional PDF
- Patient info table, colour-coded result box, all recommendations

---

## Deployment

### Option 1 — Streamlit Cloud (Free, Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repo → set `app.py` as the main file
5. Click **Deploy**

Your live URL: `https://your-app-name.streamlit.app`

> **Note:** Add `model.pkl` and `features.pkl` to your GitHub repo before deploying,
> or add a startup script that trains the model automatically.

### Option 2 — Local

```bash
streamlit run app.py
```

---

## GitHub Setup (Step by Step)

```bash
# 1. Initialise git
git init

# 2. Add all files
git add .

# 3. First commit
git commit -m "Initial commit - DiabetesGuard AI"

# 4. Create main branch
git branch -M main

# 5. Add your GitHub repo as remote
git remote add origin https://github.com/YOUR_USERNAME/diabetes-guard-ai.git

# 6. Push
git push -u origin main
```

---

## Common Errors and Fixes

| Error | Fix |
|---|---|
| `model.pkl not found` | Run `python train_model.py` first |
| `ModuleNotFoundError: reportlab` | Run `pip install reportlab` |
| `ModuleNotFoundError: streamlit` | Run `pip install streamlit` |
| `ValueError: X has N features but expecting M` | Delete `model.pkl`, re-run `train_model.py` |
| App opens but shows blank page | Hard-refresh browser with `Ctrl + Shift + R` |
| Port already in use | Run `streamlit run app.py --server.port 8502` |

---

## Disclaimer

> This application is built for **educational and hackathon purposes only**.
> The risk scores generated are based on a machine learning model and are
> **not a substitute for professional medical advice, diagnosis, or treatment**.
> Always consult a qualified healthcare professional for medical concerns.

---

## Team

Built with ❤️ during a 24-hour healthcare hackathon.

| Role | Responsibility |
|---|---|
| ML Engineer | Dataset, model training, feature engineering |
| Frontend Dev | Streamlit UI, CSS styling, charts |
| Data Analyst | EDA, visualisations, recommendations logic |
| Presenter | PPT, demo script, README, GitHub |

---

## License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

## Acknowledgements

- Dataset: Custom diabetes health dataset
- ML Library: [Scikit-learn](https://scikit-learn.org)
- UI Framework: [Streamlit](https://streamlit.io)
- Charts: [Plotly](https://plotly.com)
- PDF: [ReportLab](https://www.reportlab.com)

---

*Made with Python and Streamlit | DiabetesGuard AI | Healthcare Hackathon 2024*
