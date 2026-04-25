"""
prompts.py — prompt templates for optional LLM-backed analysis.

These are used when an OpenAI-compatible model is integrated; the default
mode uses heuristic analysis in detector.py without any API calls.
"""

SYSTEM_PROMPT = """
You are a cybersecurity email threat analyst.
Classify the email into one of:
- Safe
- Suspicious
- Phishing

Return ONLY strict JSON with keys:
label, risk_score, reasons, indicators

Rules:
- risk_score: integer 0-100
- reasons: list of short explanations
- indicators: list of tactic tags (e.g., urgency, credential_request, suspicious_link)
- If clear credential theft / urgent account threat => Phishing
- If mixed signals => Suspicious
- If benign communication => Safe
"""

USER_PROMPT_TEMPLATE = """
Analyze this email:

Subject: {subject}

Body:
{body}

Additional URL findings:
{url_findings}

Return only JSON.
"""