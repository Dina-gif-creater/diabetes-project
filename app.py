# ================================================================
# DiabetesGuard AI  —  Complete Multi-Page App
# Pages:  Login -> Register -> Details -> Results -> PDF Report
# Run:    streamlit run app.py
# ================================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go   # <-- go = plotly only, no conflict
import joblib
import datetime
import io
import json
import os
import hashlib

# ── Must be FIRST streamlit call ──
st.set_page_config(
    page_title="DiabetesGuard AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================================================================
# CSS
# ================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background: #0d1117 !important;
    color: #e2e8f0 !important;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#0d1117 0%,#0d1b2e 60%,#0a1628 100%) !important;
}
[data-testid="stHeader"]          { background: transparent !important; }
[data-testid="stSidebar"],
section[data-testid="stSidebar"],
[data-testid="collapsedControl"]  { display: none !important; }
footer                            { display: none !important; }

/* ── Cards ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.4rem;
}

/* ── Titles ── */
.page-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.6em; font-weight: 800;
    background: linear-gradient(135deg,#60a5fa,#a78bfa,#34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center; margin-bottom: .3rem;
}
.page-sub {
    text-align: center; color: #94a3b8;
    font-size: 1em; margin-bottom: 1.8rem;
}

/* ── INPUT TEXT BLACK on white bg, white on dark bg ── */
/* Login / Register inputs (light card) */
input[type="text"],
input[type="password"],
input[type="email"],
input[type="number"] {
    color: #1a1a2e !important;
    background: #ffffff !important;
    border-radius: 9px !important;
    border: 1.5px solid #c7d2fe !important;
    font-size: .97em !important;
    padding: .55rem .9rem !important;
}
input[type="text"]:focus,
input[type="password"]:focus,
input[type="number"]:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
    outline: none !important;
}

/* Streamlit wraps inputs — target inner input */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #ffffff !important;
    color: #1a1a2e !important;
    border: 1.5px solid #c7d2fe !important;
    border-radius: 9px !important;
    font-size: .97em !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #ffffff !important;
    color: #1a1a2e !important;
    border: 1.5px solid #c7d2fe !important;
    border-radius: 9px !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg,#6366f1,#8b5cf6) !important;
}

/* ── Labels ── */
label,
.stSlider label,
.stSelectbox label,
.stNumberInput label,
.stTextInput label,
.stRadio label span,
.stCheckbox label span {
    color: #94a3b8 !important;
    font-size: .83em !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: .45px !important;
}
/* Radio option text */
.stRadio div[role="radiogroup"] label span:last-child {
    color: #cbd5e1 !important;
    font-size: .95em !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    padding: .75rem 1.8rem !important;
    font-size: .97em !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all .25s ease !important;
    letter-spacing: .3px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,.4) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg,#059669,#10b981) !important;
    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    padding: .85rem 1.8rem !important;
    font-size: 1.05em !important;
    font-weight: 700 !important;
    width: 100% !important;
    letter-spacing: .3px !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(16,185,129,.4) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 11px !important;
    padding: 3px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color: white !important;
}

/* ── Metric cards ── */
.mc {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 15px;
    padding: 1.3rem;
    text-align: center;
    margin-bottom: .5rem;
}
.mc h2 { font-size: 2.4em; font-weight: 800; margin: .25rem 0; }
.mc p  { color: #94a3b8; font-size: .82em; margin: 0; }
.mc-b  { border-top: 3px solid #60a5fa; }
.mc-p  { border-top: 3px solid #a78bfa; }
.mc-g  { border-top: 3px solid #34d399; }
.mc-r  { border-top: 3px solid #f87171; }
.mc-o  { border-top: 3px solid #fb923c; }

/* ── Risk banners ── */
.r-hi {
    background: rgba(239,68,68,.12);
    border: 1px solid rgba(239,68,68,.35);
    border-left: 5px solid #ef4444;
    border-radius: 11px;
    padding: 1.1rem 1.4rem;
    color: #fca5a5; font-weight: 600; font-size: 1.05em; margin: .5rem 0;
}
.r-md {
    background: rgba(245,158,11,.12);
    border: 1px solid rgba(245,158,11,.35);
    border-left: 5px solid #f59e0b;
    border-radius: 11px;
    padding: 1.1rem 1.4rem;
    color: #fcd34d; font-weight: 600; font-size: 1.05em; margin: .5rem 0;
}
.r-lo {
    background: rgba(52,211,153,.12);
    border: 1px solid rgba(52,211,153,.35);
    border-left: 5px solid #34d399;
    border-radius: 11px;
    padding: 1.1rem 1.4rem;
    color: #6ee7b7; font-weight: 600; font-size: 1.05em; margin: .5rem 0;
}

/* ── Tip boxes ── */
.tip {
    background: rgba(96,165,250,.06);
    border: 1px solid rgba(96,165,250,.18);
    border-left: 4px solid #60a5fa;
    border-radius: 10px;
    padding: .9rem 1.1rem; margin: .5rem 0;
}
.tip b    { color: #93c5fd; display: block; margin-bottom: .25rem; font-size: .95em; }
.tip span { color: #cbd5e1; font-size: .88em; line-height: 1.6; }

/* ── Alerts ── */
.stSuccess > div { background: rgba(52,211,153,.1) !important; border-color:#34d399 !important; color:#6ee7b7 !important; }
.stError   > div { background: rgba(239,68,68,.1)  !important; border-color:#ef4444 !important; color:#fca5a5 !important; }
.stInfo    > div { background: rgba(96,165,250,.1)  !important; border-color:#60a5fa !important; color:#93c5fd !important; }
.stWarning > div { background: rgba(245,158,11,.1)  !important; border-color:#f59e0b !important; color:#fcd34d !important; }

/* ── Step bar ── */
.sbar  { display:flex; justify-content:center; align-items:center; gap:0; margin-bottom:2rem; flex-wrap:wrap; }
.sitem { display:flex; flex-direction:column; align-items:center; gap:5px; }
.scirc {
    width:34px; height:34px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:.82em; font-weight:700;
}
.sa { background:linear-gradient(135deg,#6366f1,#8b5cf6); color:white; }
.sd { background:#34d399; color:white; }
.si { background:rgba(255,255,255,0.07); color:#64748b; border:1px solid rgba(255,255,255,0.09); }
.slbl  { font-size:.72em; color:#64748b; font-weight:500; }
.slbla { color:#a5b4fc !important; font-weight:700 !important; }
.slbld { color:#34d399 !important; }
.sconn  { width:36px; height:2px; background:rgba(255,255,255,.08); margin:0 4px; margin-bottom:18px; }
.sconnd { background:#34d399 !important; }

/* ── Nav ── */
.navwrap {
    display:flex; justify-content:space-between; align-items:center;
    padding:.9rem 1.8rem; margin-bottom:1.8rem;
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.06);
    border-radius:14px;
}
.navlogo {
    font-family:'Poppins',sans-serif; font-weight:800; font-size:1.2em;
    background:linear-gradient(135deg,#60a5fa,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
</style>
""", unsafe_allow_html=True)


# ================================================================
# USER DATABASE  (JSON file)
# ================================================================
DB = "users_db.json"

def _load():
    if os.path.exists(DB):
        with open(DB) as f:
            return json.load(f)
    return {}

def _save(u):
    with open(DB, "w") as f:
        json.dump(u, f, indent=2)

def _hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password, email):
    users = _load()
    if not username.strip():
        return False, "Username cannot be empty."
    if username in users:
        return False, "Username already taken. Please choose another."
    users[username] = {"password": _hash(password), "email": email}
    _save(users)
    return True, "Account created successfully!"

def login_user(username, password):
    users = _load()
    if username not in users:
        return False, "Username not found. Please register first."
    if users[username]["password"] != _hash(password):
        return False, "Incorrect password. Please try again."
    return True, "Login successful!"


# ================================================================
# SESSION STATE
# ================================================================
INIT = {
    "page":       "login",
    "logged_in":  False,
    "username":   "",
    "user_data":  {},
    "risk_score": None,
    "safe_score": None,
    "risk_label": "",
    "tips":       [],
}
for k, v in INIT.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ================================================================
# LOAD MODEL
# ================================================================
@st.cache_resource
def load_model():
    try:
        m = joblib.load("model.pkl")
        f = joblib.load("features.pkl")
        return m, f, True
    except Exception:
        return None, None, False

model, feature_names, model_ok = load_model()


# ================================================================
# HELPERS
# ================================================================
def navigate(page):
    """Change page — named 'navigate' to avoid clashing with plotly 'go'."""
    st.session_state.page = page
    st.rerun()

def step_bar(cur_page):
    steps = ["Login", "Details", "Analysis", "Report"]
    idx_map = {"login":0,"register":0,"details":1,"predict":2,"report":3}
    cur = idx_map.get(cur_page, 0)
    html = '<div class="sbar">'
    for i, lbl in enumerate(steps):
        if i < cur:
            cc, lc, icon = "sd", "slbl slbld", "&#10003;"
        elif i == cur:
            cc, lc, icon = "sa", "slbl slbla", str(i+1)
        else:
            cc, lc, icon = "si", "slbl",       str(i+1)
        html += (f'<div class="sitem">'
                 f'<div class="scirc {cc}">{icon}</div>'
                 f'<div class="{lc}">{lbl}</div>'
                 f'</div>')
        if i < len(steps)-1:
            dc = "sconnd" if i < cur else ""
            html += f'<div class="sconn {dc}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def nav_bar():
    c1, _, c3 = st.columns([3, 5, 2])
    with c1:
        st.markdown('<div class="navlogo">🩺 DiabetesGuard AI</div>', unsafe_allow_html=True)
    with c3:
        if st.button("Logout", key="nav_logout"):
            for k, v in INIT.items():
                st.session_state[k] = v
            st.rerun()


# ================================================================
# PAGE 1 — LOGIN
# ================================================================
def page_login():
    st.markdown('<div class="page-title">🩺 DiabetesGuard AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">AI-powered early diabetes risk prediction</div>', unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Sign In")
        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter your username", key="li_u")
        password = st.text_input("Password", type="password",
                                 placeholder="Enter your password", key="li_p")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Sign In", key="btn_signin"):
            if not username.strip() or not password:
                st.error("Please enter both username and password.")
            else:
                ok, msg = login_user(username.strip(), password)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.username  = username.strip()
                    navigate("details")
                else:
                    st.error(msg)

        st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:1.3rem 0'>",
                    unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#64748b;font-size:.88em;"
                    "margin-bottom:.7rem'>No account yet?</p>", unsafe_allow_html=True)

        if st.button("Create New Account", key="btn_go_reg"):
            navigate("register")

        st.markdown('</div>', unsafe_allow_html=True)

    # Feature highlights
    st.markdown("<br>", unsafe_allow_html=True)
    for col, icon, title, desc in zip(
        st.columns(4),
        ["🤖","📊","💡","📄"],
        ["AI Model","Risk Score","Smart Tips","PDF Report"],
        ["Random Forest ML","Personalised 0-100","Custom health advice","Download instantly"]
    ):
        with col:
            st.markdown(f"""
            <div class="mc mc-b">
                <div style="font-size:1.8em">{icon}</div>
                <div style="font-weight:700;color:#93c5fd;margin:.3rem 0">{title}</div>
                <p>{desc}</p>
            </div>""", unsafe_allow_html=True)


# ================================================================
# PAGE 2 — REGISTER
# ================================================================
def page_register():
    st.markdown('<div class="page-title">🩺 DiabetesGuard AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Create your free account</div>', unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Register")
        st.markdown("<br>", unsafe_allow_html=True)

        new_u  = st.text_input("Choose a Username", placeholder="e.g. john_doe",          key="reg_u")
        new_e  = st.text_input("Email Address",     placeholder="you@email.com",           key="reg_e")
        new_p  = st.text_input("Password",  type="password", placeholder="Min 6 characters", key="reg_p")
        new_p2 = st.text_input("Confirm Password", type="password",
                                placeholder="Repeat your password", key="reg_p2")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Create Account", key="btn_create"):
            if not new_u or not new_e or not new_p or not new_p2:
                st.error("Please fill in all fields.")
            elif len(new_p) < 6:
                st.error("Password must be at least 6 characters.")
            elif new_p != new_p2:
                st.error("Passwords do not match.")
            elif "@" not in new_e:
                st.error("Please enter a valid email address.")
            else:
                ok, msg = register_user(new_u.strip(), new_p, new_e.strip())
                if ok:
                    st.success(msg + " Please sign in now.")
                    import time; time.sleep(1.5)
                    navigate("login")
                else:
                    st.error(msg)

        st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:1.3rem 0'>",
                    unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#64748b;font-size:.88em;"
                    "margin-bottom:.7rem'>Already have an account?</p>", unsafe_allow_html=True)

        if st.button("Back to Sign In", key="btn_back_login"):
            navigate("login")

        st.markdown('</div>', unsafe_allow_html=True)


# ================================================================
# PAGE 3 — HEALTH DETAILS FORM
# ================================================================
def page_details():
    nav_bar()
    step_bar("details")

    st.markdown('<div class="page-title" style="font-size:2em">📋 Your Health Profile</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Fill in your details for the most accurate prediction</div>',
                unsafe_allow_html=True)

    d = st.session_state.user_data  # prefill on revisit

    with st.form("health_form"):

        # ── Personal ──
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Personal Information")
        c1, c2, c3 = st.columns(3)
        with c1:
            full_name = st.text_input("Full Name",
                                      value=d.get("full_name",""),
                                      placeholder="e.g. Priya Sharma")
        with c2:
            age = st.number_input("Age (years)", 10, 100, int(d.get("age", 30)))
        with c3:
            g_opts = ["Male","Female","Other"]
            gender = st.selectbox("Gender", g_opts,
                                   index=g_opts.index(d.get("gender","Male")))
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Body Measurements ──
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📏 Body Measurements")
        c1, c2 = st.columns(2)
        with c1:
            weight = st.number_input("Weight (kg)", 20.0, 250.0,
                                     float(d.get("weight", 70.0)), 0.1)
        with c2:
            height = st.number_input("Height (cm)", 100.0, 250.0,
                                     float(d.get("height", 170.0)), 0.1)

        bmi_val = round(weight / ((height / 100) ** 2), 1)
        bmi_lbl = ("Underweight" if bmi_val < 18.5 else
                   "Normal"      if bmi_val < 25   else
                   "Overweight"  if bmi_val < 30   else "Obese")

        cb1, cb2, _ = st.columns([1,1,2])
        with cb1:
            st.metric("Your BMI (auto-calculated)", f"{bmi_val}", bmi_lbl)
        with cb2:
            if   bmi_val < 18.5: st.info("Underweight")
            elif bmi_val < 25:   st.success("Normal BMI")
            elif bmi_val < 30:   st.warning("Overweight")
            else:                st.error("Obese")

        blood_glucose = st.slider(
            "Fasting Blood Glucose (mg/dL)", 50, 300,
            int(d.get("blood_glucose", 100)),
            help="Normal: 70-100  |  Pre-diabetes: 100-125  |  Diabetes: 126+"
        )
        cg, _, _ = st.columns(3)
        with cg:
            if   blood_glucose < 100: st.success("Normal glucose range")
            elif blood_glucose < 126: st.warning("Pre-diabetes range")
            else:                     st.error("High - consult a doctor")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Lifestyle ──
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🏃 Lifestyle and Daily Habits")
        c1, c2 = st.columns(2)
        with c1:
            physical_activity = st.slider(
                "Daily Exercise (minutes)", 0, 180,
                int(d.get("physical_activity", 30))
            )
            sleep_hours = st.slider(
                "Sleep Hours per Night", 2.0, 14.0,
                float(d.get("sleep_hours", 7.0)), 0.5
            )
            stress_level = st.select_slider(
                "Stress Level", options=[0,1,2],
                value=int(d.get("stress_level", 0)),
                format_func=lambda x: {0:"Low",1:"Medium",2:"High"}[x]
            )
        with c2:
            diet = st.radio(
                "Diet Quality", options=[1,0],
                index=0 if d.get("diet",1)==1 else 1,
                format_func=lambda x: ("Healthy (fruits, veggies, whole grains)"
                                       if x==1 else "Unhealthy (processed, sugary, fried)")
            )
            hydration = st.radio(
                "Daily Water Intake", options=[1,0],
                index=0 if d.get("hydration_level",1)==1 else 1,
                format_func=lambda x: ("Good (8+ glasses/day)"
                                       if x==1 else "Poor (less than 8 glasses)")
            )
            medication = st.radio(
                "Medication Adherence", options=[1,0],
                index=0 if d.get("medication_adherence",1)==1 else 1,
                format_func=lambda x: ("Regular (as prescribed)"
                                       if x==1 else "Irregular (often skip)")
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Medical History ──
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🏥 Medical Background")
        c1, c2 = st.columns(2)
        with c1:
            fh_opts = ["Yes","No","Not Sure"]
            family_history = st.radio(
                "Family History of Diabetes?", fh_opts,
                index=fh_opts.index(d.get("family_history","No"))
            )
        with c2:
            sm_opts = ["Non-smoker","Ex-smoker","Current Smoker"]
            smoking = st.radio(
                "Smoking Status", sm_opts,
                index=sm_opts.index(d.get("smoking","Non-smoker"))
            )
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Analyse My Diabetes Risk  →")

    if submitted:
        if not full_name.strip():
            st.error("Please enter your full name before continuing.")
        else:
            st.session_state.user_data = {
                "full_name":            full_name.strip(),
                "age":                  age,
                "gender":               gender,
                "weight":               weight,
                "height":               height,
                "bmi":                  bmi_val,
                "bmi_label":            bmi_lbl,
                "blood_glucose":        blood_glucose,
                "physical_activity":    physical_activity,
                "sleep_hours":          sleep_hours,
                "stress_level":         stress_level,
                "diet":                 diet,
                "hydration_level":      hydration,
                "medication_adherence": medication,
                "family_history":       family_history,
                "smoking":              smoking,
            }
            navigate("predict")


# ================================================================
# PAGE 4 — PREDICTION & RESULTS
# ================================================================
def page_predict():
    nav_bar()
    step_bar("predict")

    d    = st.session_state.user_data
    name = d.get("full_name", st.session_state.username)

    st.markdown(f'<div class="page-title" style="font-size:2em">Results for {name}</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Your personalised diabetes risk assessment</div>',
                unsafe_allow_html=True)

    if not model_ok:
        st.error("model.pkl not found!  Run `python train_model.py` first, then restart the app.")
        if st.button("Back to Details"):
            navigate("details")
        return

    # ── Run ML prediction ──
    feat_order = ['weight','height','blood_glucose','physical_activity',
                  'diet','medication_adherence','stress_level',
                  'sleep_hours','hydration_level','bmi']
    inp        = np.array([[d[k] for k in feat_order]])
    risk_score = round(float(np.clip(model.predict(inp)[0], 0, 100)), 1)
    safe_score = round(100 - risk_score, 1)
    risk_label = ("HIGH RISK"     if risk_score >= 60 else
                  "MODERATE RISK" if risk_score >= 30 else
                  "LOW RISK")

    # Save for PDF page
    st.session_state.risk_score = risk_score
    st.session_state.safe_score = safe_score
    st.session_state.risk_label = risk_label

    # ── Metric cards ──
    r_color = "#f87171" if risk_score>=60 else "#fbbf24" if risk_score>=30 else "#34d399"
    r_cls   = "mc-r"   if risk_score>=60 else "mc-o"    if risk_score>=30 else "mc-g"

    for col, lbl, val, sub, hex_c, cls in zip(
        st.columns(5),
        ["Risk Score","Safety Score","BMI","Blood Glucose","Sleep"],
        [str(risk_score), str(safe_score), str(d["bmi"]),
         str(d["blood_glucose"]), str(d["sleep_hours"])],
        ["out of 100","out of 100", d["bmi_label"], "mg/dL","hrs/night"],
        [r_color,"#34d399","#a78bfa","#60a5fa","#fb923c"],
        [r_cls,"mc-g","mc-p","mc-b","mc-o"]
    ):
        with col:
            st.markdown(f"""<div class="mc {cls}">
                <p>{lbl}</p>
                <h2 style="color:{hex_c}">{val}</h2>
                <p>{sub}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Risk banner ──
    if risk_score >= 60:
        st.markdown(
            f'<div class="r-hi">HIGH RISK — Score: {risk_score}/100.'
            f'  Please consult a doctor soon.</div>',
            unsafe_allow_html=True)
    elif risk_score >= 30:
        st.markdown(
            f'<div class="r-md">MODERATE RISK — Score: {risk_score}/100.'
            f'  Take preventive action now.</div>',
            unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="r-lo">LOW RISK — Score: {risk_score}/100.'
            f'  Keep up the healthy habits!</div>',
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──
    t1, t2, t3 = st.tabs(["Risk Gauge", "Key Factors", "Health Radar"])

    with t1:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={'x':[0,1], 'y':[0,1]},
            title={'text':"Diabetes Risk Score",
                   'font':{'size':18, 'color':'#94a3b8'}},
            number={'font':{'size':52, 'color':'#e2e8f0'}},
            gauge={
                'axis':{'range':[0,100],
                        'tickcolor':'#64748b',
                        'tickfont':{'color':'#94a3b8'}},
                'bar':{'color':'#8b5cf6', 'thickness':0.24},
                'bgcolor':'rgba(0,0,0,0)',
                'bordercolor':'rgba(0,0,0,0)',
                'steps':[
                    {'range':[0,30],  'color':'rgba(52,211,153,0.18)'},
                    {'range':[30,60], 'color':'rgba(251,191,36,0.18)'},
                    {'range':[60,100],'color':'rgba(239,68,68,0.18)'},
                ],
                'threshold':{
                    'line':{'color':'#f87171','width':3},
                    'thickness':0.75,
                    'value':risk_score
                }
            }
        ))
        gauge.update_layout(
            height=360,
            margin=dict(t=50,b=10,l=20,r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(gauge, use_container_width=True)

    with t2:
        imps   = model.feature_importances_
        labels = ['Weight','Height','Blood Glucose','Physical Activity',
                  'Diet','Medication','Stress Level','Sleep Hours','Hydration','BMI']
        sidx   = np.argsort(imps)
        bar_c  = ['#f87171' if imps[i]==max(imps) else '#8b5cf6' for i in sidx]

        bar_chart = go.Figure(go.Bar(
            x=imps[sidx],
            y=[labels[i] for i in sidx],
            orientation='h',
            marker_color=bar_c,
            text=[f"{v:.3f}" for v in imps[sidx]],
            textposition='outside',
            textfont={'color':'#94a3b8','size':10}
        ))
        bar_chart.update_layout(
            title=dict(text="What the AI focuses on most",
                       font={'color':'#94a3b8','size':13}),
            xaxis=dict(color='#64748b',
                       gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(color='#94a3b8'),
            height=400,
            margin=dict(t=45,b=15,l=15,r=55),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(bar_chart, use_container_width=True)

    with t3:
        cats  = ['Glucose','BMI','Activity','Sleep','Hydration','Medication']
        vals  = [
            min(d["blood_glucose"]/300*100, 100),
            min(d["bmi"]/40*100, 100),
            min(d["physical_activity"]/120*100, 100),
            min(d["sleep_hours"]/10*100, 100),
            d["hydration_level"]*100,
            d["medication_adherence"]*100,
        ]
        vc = vals + [vals[0]]
        cc = cats + [cats[0]]

        radar = go.Figure(go.Scatterpolar(
            r=vc, theta=cc,
            fill='toself',
            fillcolor='rgba(139,92,246,0.14)',
            line=dict(color='#8b5cf6', width=2),
            marker=dict(color='#a78bfa', size=6)
        ))
        radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,100],
                                color='#64748b',
                                gridcolor='rgba(255,255,255,0.05)'),
                angularaxis=dict(color='#94a3b8')
            ),
            height=370,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(radar, use_container_width=True)

    # ── Build tips ──
    tips = []
    if d["blood_glucose"] > 140:
        tips.append(("High Blood Glucose",
                     "Your glucose is above 140 mg/dL. Avoid sugary drinks, white rice, "
                     "and processed food. Get an HbA1c blood test done."))
    elif d["blood_glucose"] > 100:
        tips.append(("Pre-Diabetes Glucose",
                     "Your fasting glucose is in the pre-diabetes range (100-125 mg/dL). "
                     "Reduce refined carbs, increase fibre, and exercise daily."))
    if d["bmi"] >= 30:
        tips.append(("Obesity Risk Factor",
                     f"Your BMI is {d['bmi']} (Obese). Losing 5-7 percent of body weight "
                     "can reduce diabetes risk by up to 58 percent. Start with daily walks."))
    elif d["bmi"] >= 25:
        tips.append(("Overweight BMI",
                     f"Your BMI is {d['bmi']} (Overweight). Target below 25 through a "
                     "calorie-controlled diet and regular aerobic exercise."))
    if d["physical_activity"] < 30:
        tips.append(("Low Physical Activity",
                     "Less than 30 mins of exercise per day. A brisk 30-minute daily walk "
                     "increases insulin sensitivity and lowers blood sugar naturally."))
    if d["stress_level"] == 2:
        tips.append(("High Stress Level",
                     "Chronic stress raises blood sugar via cortisol. Practice 15 mins "
                     "of meditation, deep breathing, or yoga every day."))
    if d["sleep_hours"] < 6:
        tips.append(("Insufficient Sleep",
                     "Less than 6 hours of sleep increases insulin resistance. "
                     "Aim for 7-9 hours of quality sleep each night."))
    if d["hydration_level"] == 0:
        tips.append(("Poor Hydration",
                     "Dehydration concentrates glucose in blood. "
                     "Drink at least 8-10 glasses of water every day."))
    if d["diet"] == 0:
        tips.append(("Unhealthy Diet",
                     "Eat more vegetables, legumes, whole grains, and lean protein. "
                     "Cut sugar, refined carbs, and fried foods."))
    if d["medication_adherence"] == 0:
        tips.append(("Irregular Medication",
                     "Skipping prescribed medication worsens outcomes. "
                     "Set two daily phone reminders and use a weekly pill organiser."))
    if d.get("family_history") == "Yes":
        tips.append(("Family History of Diabetes",
                     "First-degree relatives with diabetes raise your genetic risk. "
                     "Get a diabetes screening every 6 months and stay active."))
    if d.get("smoking") == "Current Smoker":
        tips.append(("Smoking Risk",
                     "Smokers are 30-40 percent more likely to develop Type 2 diabetes. "
                     "Quitting smoking significantly reduces your risk."))
    tips.append(("Recommended Medical Tests",
                 "Ask your doctor for: Fasting Blood Sugar, HbA1c test, "
                 "full lipid profile, and blood pressure check annually."))

    st.session_state.tips = tips

    # ── Display tips ──
    st.markdown("### Personalised Recommendations")
    ct1, ct2 = st.columns(2)
    for i, (tt, tb) in enumerate(tips):
        with (ct1 if i%2==0 else ct2):
            st.markdown(f'<div class="tip"><b>{tt}</b><span>{tb}</span></div>',
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cb, cn = st.columns(2)
    with cb:
        if st.button("Edit My Details", key="back_det"):
            navigate("details")
    with cn:
        if st.button("Download PDF Report", key="go_rep"):
            navigate("report")


# ================================================================
# PDF BUILDER  (ReportLab — zero Unicode errors)
# ================================================================
def build_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib           import colors
    from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units     import cm
    from reportlab.platypus      import (SimpleDocTemplate, Paragraph, Spacer,
                                         Table, TableStyle, HRFlowable)

    d          = st.session_state.user_data
    risk_score = st.session_state.risk_score
    safe_score = st.session_state.safe_score
    risk_label = st.session_state.risk_label
    tips       = st.session_state.tips

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm,   bottomMargin=2*cm)
    base = getSampleStyleSheet()

    def PS(name, **kw):
        return ParagraphStyle(name, parent=base['Normal'], **kw)

    s_title = PS('T',  fontSize=22, textColor=colors.white,
                 alignment=1, fontName='Helvetica-Bold')
    s_sub   = PS('Su', fontSize=11,
                 textColor=colors.Color(.82,.91,1), alignment=1)
    s_date  = PS('Da', fontSize=9,
                 textColor=colors.HexColor('#888888'),
                 alignment=1, spaceBefore=6)
    s_sec   = PS('Se', fontSize=13,
                 textColor=colors.HexColor('#1a73e8'),
                 fontName='Helvetica-Bold',
                 spaceBefore=12, spaceAfter=5)
    s_tt    = PS('TT', fontSize=10,
                 textColor=colors.HexColor('#1a5fb4'),
                 fontName='Helvetica-Bold',
                 spaceBefore=5, spaceAfter=2)
    s_tb    = PS('TB', fontSize=9, leading=13,
                 leftIndent=8, spaceAfter=3)
    s_dis   = PS('Di', fontSize=8,
                 textColor=colors.HexColor('#aaaaaa'),
                 alignment=1, spaceBefore=8)

    def banner(text, style, bg_hex):
        tbl = Table([[Paragraph(text, style)]], colWidths=[17*cm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor(bg_hex)),
            ('TOPPADDING',    (0,0),(-1,-1), 11),
            ('BOTTOMPADDING', (0,0),(-1,-1), 9),
            ('LEFTPADDING',   (0,0),(-1,-1), 14),
            ('RIGHTPADDING',  (0,0),(-1,-1), 14),
        ]))
        return tbl

    story = []
    story.append(banner("DiabetesGuard AI - Health Report",
                        s_title, '#1a73e8'))
    story.append(banner("Personalized Diabetes Risk Assessment",
                        s_sub,   '#1557c0'))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Generated: " +
        datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p'),
        s_date))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor('#1a73e8')))
    story.append(Spacer(1, 8))

    # Patient info table
    story.append(Paragraph("Patient Information", s_sec))
    sm = {0:"Low", 1:"Medium", 2:"High"}
    rows = [
        ["Field", "Value"],
        ["Full Name",         str(d.get("full_name",""))],
        ["Age",               str(d.get("age","")) + " years"],
        ["Gender",            str(d.get("gender",""))],
        ["Weight",            str(d.get("weight","")) + " kg"],
        ["Height",            str(d.get("height","")) + " cm"],
        ["BMI",               str(d.get("bmi","")) + " (" + str(d.get("bmi_label","")) + ")"],
        ["Blood Glucose",     str(d.get("blood_glucose","")) + " mg/dL"],
        ["Physical Activity", str(d.get("physical_activity","")) + " mins/day"],
        ["Diet",              "Healthy" if d.get("diet")==1 else "Unhealthy"],
        ["Medication",        "Regular" if d.get("medication_adherence")==1 else "Irregular"],
        ["Stress Level",      sm.get(d.get("stress_level",0), "")],
        ["Sleep Hours",       str(d.get("sleep_hours","")) + " hrs/night"],
        ["Hydration",         "Adequate" if d.get("hydration_level")==1 else "Inadequate"],
        ["Family History",    str(d.get("family_history",""))],
        ["Smoking",           str(d.get("smoking",""))],
    ]
    pt = Table(rows, colWidths=[6*cm, 11*cm])
    pt.setStyle(TableStyle([
        ('BACKGROUND',     (0,0),(-1,0),  colors.HexColor('#1a73e8')),
        ('TEXTCOLOR',      (0,0),(-1,0),  colors.white),
        ('FONTNAME',       (0,0),(-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',       (0,0),(-1,0),  10),
        ('ROWBACKGROUNDS', (0,1),(-1,-1),
         [colors.HexColor('#f0f7ff'), colors.white]),
        ('FONTNAME',       (0,1),(0,-1),  'Helvetica-Bold'),
        ('FONTSIZE',       (0,1),(-1,-1), 9),
        ('GRID',           (0,0),(-1,-1), 0.4, colors.HexColor('#cccccc')),
        ('TOPPADDING',     (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',  (0,0),(-1,-1), 5),
        ('LEFTPADDING',    (0,0),(-1,-1), 8),
        ('RIGHTPADDING',   (0,0),(-1,-1), 8),
    ]))
    story.append(pt)
    story.append(Spacer(1, 10))

    # Result box
    story.append(Paragraph("Risk Assessment Result", s_sec))
    if risk_score >= 60:
        r_bg = colors.HexColor('#ffe5e5')
        r_tc = colors.HexColor('#cc0000')
    elif risk_score >= 30:
        r_bg = colors.HexColor('#fff8e1')
        r_tc = colors.HexColor('#b36b00')
    else:
        r_bg = colors.HexColor('#e5f9e5')
        r_tc = colors.HexColor('#006600')

    s_res = PS('Rs', fontSize=13, textColor=r_tc,
               fontName='Helvetica-Bold', alignment=1)
    res_line = (str(risk_label) +
                "  |  Risk Score: " + str(risk_score) +
                " / 100  |  Safety Score: " + str(safe_score) + " / 100")
    rt = Table([[Paragraph(res_line, s_res)]], colWidths=[17*cm])
    rt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), r_bg),
        ('TOPPADDING',    (0,0),(-1,-1), 12),
        ('BOTTOMPADDING', (0,0),(-1,-1), 12),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 10),
        ('BOX',           (0,0),(-1,-1), 1.5, r_tc),
    ]))
    story.append(rt)
    story.append(Spacer(1, 10))

    # Tips
    story.append(Paragraph("Health Recommendations", s_sec))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor('#1a73e8')))
    story.append(Spacer(1, 4))

    for i, (tt, tb) in enumerate(tips):
        tip_tbl = Table([
            [Paragraph(str(i+1) + ". " + str(tt), s_tt)],
            [Paragraph(str(tb), s_tb)],
        ], colWidths=[17*cm])
        tip_tbl.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor('#f0f9ff')),
            ('LINEBEFORE',    (0,0),(0,-1),  3, colors.HexColor('#1a73e8')),
            ('LEFTPADDING',   (0,0),(-1,-1), 10),
            ('RIGHTPADDING',  (0,0),(-1,-1), 10),
            ('TOPPADDING',    (0,0),(0,0),   5),
            ('BOTTOMPADDING', (0,-1),(-1,-1),6),
        ]))
        story.append(tip_tbl)
        story.append(Spacer(1, 5))

    # Disclaimer
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor('#cccccc')))
    story.append(Paragraph(
        "DISCLAIMER: This report is AI-generated for educational purposes only. "
        "It is NOT a medical diagnosis. Please consult a licensed healthcare "
        "professional for proper medical advice and treatment.", s_dis))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ================================================================
# PAGE 5 — REPORT DOWNLOAD
# ================================================================
def page_report():
    nav_bar()
    step_bar("report")

    d    = st.session_state.user_data
    name = d.get("full_name", st.session_state.username)

    st.markdown('<div class="page-title" style="font-size:2em">Your Health Report</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">Complete diabetes risk report for {name}</div>',
                unsafe_allow_html=True)

    risk_score = st.session_state.risk_score
    safe_score = st.session_state.safe_score
    risk_label = st.session_state.risk_label

    cl, cr = st.columns([1.1, 1])

    with cl:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Result Summary")
        if risk_score >= 60:
            st.markdown(
                f'<div class="r-hi">HIGH RISK — Score: {risk_score} / 100</div>',
                unsafe_allow_html=True)
        elif risk_score >= 30:
            st.markdown(
                f'<div class="r-md">MODERATE RISK — Score: {risk_score} / 100</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="r-lo">LOW RISK — Score: {risk_score} / 100</div>',
                unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Your PDF report includes:**")
        for item in [
            "Complete patient information table",
            "Colour-coded risk result box",
            "Risk score and safety score",
            "All personalised health recommendations",
            "Medical disclaimer",
        ]:
            st.markdown(f"- {item}")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Download Your PDF")
        st.markdown(
            "<p style='color:#94a3b8;font-size:.9em;margin-bottom:1.2rem'>"
            "Click the green button below to download your complete "
            "health report as a PDF file.</p>",
            unsafe_allow_html=True)
        try:
            pdf_data  = build_pdf()
            safe_name = name.replace(" ","_").replace("/","_")
            filename  = ("DiabetesGuard_" + safe_name +
                         "_" + str(datetime.date.today()) + ".pdf")
            st.download_button(
                label="Download PDF Health Report",
                data=pdf_data,
                file_name=filename,
                mime="application/pdf",
                key="dl_pdf"
            )
            st.success("Report ready! Click the green button above to download.")
        except Exception as err:
            st.error("PDF error: " + str(err))
            st.info("Fix:  pip install reportlab")
        st.markdown('</div>', unsafe_allow_html=True)

    # Tips preview
    st.markdown("### Your Health Recommendations")
    ct1, ct2 = st.columns(2)
    for i, (tt, tb) in enumerate(st.session_state.tips):
        with (ct1 if i%2==0 else ct2):
            st.markdown(f'<div class="tip"><b>{tt}</b><span>{tb}</span></div>',
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cb, cn = st.columns(2)
    with cb:
        if st.button("Back to Results", key="rpt_back"):
            navigate("predict")
    with cn:
        if st.button("Start New Assessment", key="rpt_new"):
            st.session_state.user_data  = {}
            st.session_state.risk_score = None
            st.session_state.tips       = []
            navigate("details")


# ================================================================
# ROUTER
# ================================================================
_page = st.session_state.page

# Guard unauthenticated access
if not st.session_state.logged_in and _page not in ("login","register"):
    st.session_state.page = "login"
    _page = "login"

if   _page == "login":    page_login()
elif _page == "register": page_register()
elif _page == "details":  page_details()
elif _page == "predict":  page_predict()
elif _page == "report":   page_report()
else:
    st.session_state.page = "login"
    st.rerun()