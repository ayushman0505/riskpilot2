🚀 RiskPilot – AI-Powered Project Risk Management Dashboard
RiskPilot is a full-stack AI-driven project risk analysis platform that helps teams identify, visualize, and mitigate project risks using real project data, simulations, and an intelligent AI advisor.

Built with FastAPI + Streamlit + LLMs, RiskPilot turns raw CSV project data into actionable insights with a modern, dark-themed dashboard.

✨ Key Features
📊 Project Risk Analytics
Risk score calculation per project
Budget utilization analysis
Timeline delay estimation
Monte Carlo simulation for delivery risk (P85 estimates)
📈 Interactive Visualizations
Risk score charts
Budget utilization graphs
Timeline & Monte Carlo visual insights
Clean, dark, professional UI (executive-friendly)
🤖 AI Project Advisor (LLM-powered)
Ask questions about:
Project risks
Employees & resource allocation
Cost overruns
Schedule delays
Continuous chat memory
Context-aware answers using live project data
Streaming responses (typing-style output)
📁 CSV-Based Data Input
Upload three CSV files:

projects.csv
employees.csv
finances.csv
No database required — lightweight & portable.

🧠 AI Capabilities
The AI advisor understands:

Risk drivers and bottlenecks
Employee workload & skills
Cost vs schedule trade-offs
Executive-level summaries and recommendations
LLM runs locally via Ollama (LLaMA 3) or can be swapped with any compatible model.

🛠️ Tech Stack
Backend
FastAPI
Python 3.10
Monte Carlo simulation
LLM streaming API
Frontend
Streamlit
Plotly (interactive charts)
Custom dark UI (CSS)
Session-based chat memory
AI / ML
Ollama (LLaMA 3)
Prompt grounding using project context
