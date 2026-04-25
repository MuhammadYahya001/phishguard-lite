# PhishGuard Lite 🛡️

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-phishguard--lite-brightgreen?logo=streamlit)](https://phishguard-lite.streamlit.app/)

> **Heuristic phishing email detector — no API key required.**  
> Instantly classify emails as Safe, Suspicious, or Phishing and understand *why*.

**🌐 [Try the live app →](https://phishguard-lite.streamlit.app/)**

---

## Overview

PhishGuard Lite is a lightweight, browser-based tool that analyzes email content for phishing indicators using rule-based heuristics. It requires no external API and runs entirely in-browser via Streamlit.

It was built to demonstrate practical NLP-adjacent security tooling: keyword analysis, URL heuristics, credential-request detection, and urgency pattern matching — all surfaced in a clean, interactive UI.

---

## Features

| Feature | Description |
|---|---|
| 🏷️ **Email Classification** | Labels every email as **Safe**, **Suspicious**, or **Phishing** |
| 📊 **Risk Score (0–100)** | Numeric risk score with a visual progress bar |
| 🔍 **Threat Reasons** | Human-readable explanation of detected indicators |
| 🌐 **URL Analysis** | Extracts all URLs and flags IP-based links, shorteners, and suspicious paths |
| ⚡ **No API Key Needed** | Fully heuristic — works offline, no external calls |

---

## How It Works

```
Email Input (Subject + Body)
        │
        ▼
  Keyword Analysis  ──►  Urgency Detection  ──►  Credential Checks
        │
        ▼
    URL Extraction ──►  URL Heuristics (IP, shortener, path keywords)
        │
        ▼
  Risk Score Aggregation  ──►  Label: Safe / Suspicious / Phishing
```

Scoring rules:
- **Safe**: risk score < 40  
- **Suspicious**: 40 ≤ score < 70  
- **Phishing**: score ≥ 70  

---

## Tech Stack

- **[Python 3.9+](https://www.python.org/)** — core logic
- **[Streamlit](https://streamlit.io/)** — interactive web UI
- **[tldextract](https://github.com/john-kurkowski/tldextract)** — accurate domain parsing
- **[re / urllib](https://docs.python.org/3/library/re.html)** — URL extraction and pattern matching

---

## Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/MuhammadYahya001/phishguard-lite.git
cd phishguard-lite
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Project Structure

```
phishguard-lite/
├── app.py              # Streamlit UI
├── detector.py         # Heuristic analysis engine
├── prompts.py          # Prompt templates (for optional LLM integration)
├── sample_emails.json  # Example phishing/safe emails for testing
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Sample Test Cases

Paste any of these into the app to see it in action:

**Phishing example (Subject):**
```
Urgent: Your account has been suspended — verify immediately
```

**Phishing example (Body):**
```
Dear Customer, unusual activity was detected on your account.
Click below to confirm your identity and reset your password within 24 hours
or your account will be permanently locked.
http://secure-login.verify-account.xyz/update
```

---

## Disclaimer

> ⚠️ PhishGuard Lite is for **educational and demonstration purposes only**.  
> It is not a replacement for enterprise email security solutions (e.g., Microsoft Defender, Proofpoint, or Google Workspace security).  
> Heuristic analysis may produce false positives and false negatives.

---

## License

This project is licensed under the [MIT License](LICENSE).
