import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="RiskPilot",
    page_icon="🧠",
    layout="wide"
)

# ================= DARK THEME (READABLE) =================
st.markdown("""
<style>
.stApp { background-color: #0e1117; }
html, body, p, span, div, label, h1, h2, h3 { color: white !important; }

.card {
    background: #161b22;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #30363d;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: #8b949e !important;
    margin-top: 40px;
    font-size: 14px;
}

.stButton > button {
    background-color: #238636;
    color: white !important;
    border-radius: 8px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #2ea043;
}
</style>
""", unsafe_allow_html=True)

# ================= UTIL FUNCTIONS =================
def monte_carlo_days(base_days, risk, sims=1000):
    samples = np.random.normal(base_days, base_days * max(risk, 0.1), sims)
    return int(np.percentile(samples, 85))

def analyze_risk(projects, employees, finances):
    rows = []
    for _, p in projects.iterrows():
        pid = p["project_id"]
        emp = employees[employees["assigned_project"] == pid]
        fin = finances[finances["project_id"] == pid]
        if emp.empty or fin.empty:
            continue

        fin = fin.iloc[0]
        avg_eff = max(emp["efficiency"].mean(), 0.1)
        base_days = p["estimated_days"] / avg_eff
        budget_used = fin["spent"] / fin["budget"]

        risk = round(
            (1 - avg_eff) * 0.4 +
            p["complexity"] * 0.4 +
            budget_used * 0.2, 2
        )

        rows.append({
            "project": p["project_name"],
            "risk_score": risk,
            "estimated_days": int(base_days),
            "monte_carlo_days": monte_carlo_days(base_days, risk),
            "budget_utilization": round(budget_used * 100, 2)
        })

    return pd.DataFrame(rows)

def generate_summary(df):
    return f"""
• Average Risk Score: {round(df['risk_score'].mean(),2)}
• Budget Utilization: {round(df['budget_utilization'].mean(),1)}%
• Monte Carlo (P85): {int(df['monte_carlo_days'].max())} days

RECOMMENDATIONS:
• Add temporary resources to high-risk projects
• Parallelize critical tasks
• Tighten cost approvals
"""

def ask_ai(question, df):
    # Optional Ollama support (if running locally)
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"Project data:\n{df}\n\nQuestion:{question}",
                "stream": False
            },
            timeout=10
        )
        return r.json()["response"]
    except:
        return "AI unavailable in cloud. Run locally with Ollama for full AI support."

# ================= STATE =================
if "df" not in st.session_state:
    st.session_state.df = None
if "chat" not in st.session_state:
    st.session_state.chat = []

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'>🧠 RiskPilot</h1>", unsafe_allow_html=True)
st.markdown("<center>AI-powered Corporate Risk Management Dashboard</center><br>", unsafe_allow_html=True)

# ================= UPLOAD =================
st.subheader("📤 Upload CSV Files")
c1, c2, c3 = st.columns(3)
with c1:
    projects = st.file_uploader("projects.csv", type="csv")
with c2:
    employees = st.file_uploader("employees.csv", type="csv")
with c3:
    finances = st.file_uploader("finances.csv", type="csv")

if projects and employees and finances and st.button("Run Analysis"):
    p = pd.read_csv(projects)
    e = pd.read_csv(employees)
    f = pd.read_csv(finances)
    st.session_state.df = analyze_risk(p, e, f)

# ================= DASHBOARD =================
if st.session_state.df is not None:
    df = st.session_state.df
    avg_risk = round(df["risk_score"].mean(), 2)

    left, right = st.columns([2.5, 1])

    with left:
        st.subheader("📄 Executive Summary")
        st.markdown(f"<div class='card'>{generate_summary(df)}</div>", unsafe_allow_html=True)

    with right:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_risk,
            gauge={"axis":{"range":[0,1]}},
            title={"text":"Avg Risk"}
        ))
        fig.update_layout(template="plotly_dark", height=230)
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            px.scatter(
                df,
                x="estimated_days",
                y="risk_score",
                size="budget_utilization",
                color="risk_score",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            px.density_heatmap(
                df,
                x="budget_utilization",
                y="risk_score",
                template="plotly_dark"
            ),
            use_container_width=True
        )

    st.dataframe(df, use_container_width=True)

# ================= CHAT =================
st.subheader("🤖 AI Project Advisor")
q = st.text_input("Ask about risks, cost, or timelines")

if st.button("Ask AI") and q:
    ans = ask_ai(q, st.session_state.df)
    st.session_state.chat.append((q, ans))

for q, a in st.session_state.chat:
    st.markdown(f"<div class='card'><b>You:</b> {q}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><b>AI:</b> {a}</div>", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("<div class='footer'>Made with ❤️ by Ayushman</div>", unsafe_allow_html=True)
