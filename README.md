# phishguard-lite# PhishGuard Lite 🛡️

## Live Demo
[Open App](https://phishguard-lite.streamlit.app/)

AI-assisted phishing email detector using **Python + Streamlit + OpenAI**.

## Features
- Classifies emails: **Safe / Suspicious / Phishing**
- Risk score from **0–100**
- Explanation of reasons and indicators
- URL extraction + suspicious link heuristics

## Setup
```bash
python -m venv .venv
# activate venv
pip install -r requirements.txt
```

Create `.env`:
```env
OPENAI_API_KEY=your_api_key_here
```

Run:
```bash
streamlit run app.py
```

## Resume Bullet
Built an AI-assisted phishing triage tool that classifies emails, assigns risk scores, and explains threat indicators like urgency language, credential requests, and suspicious URLs.

## Disclaimer
For educational use only.