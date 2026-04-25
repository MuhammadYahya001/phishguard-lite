import re
from urllib.parse import urlparse
import tldextract


SUSPICIOUS_KEYWORDS = [
    "verify your account", "urgent", "immediately", "suspended", "click below",
    "reset password", "confirm identity", "bank", "wallet", "login now", "otp",
    "ssn", "limited time", "act now", "update payment", "unusual activity",
    "account locked", "security alert", "dear customer"
]


def extract_urls(text: str):
    pattern = r"(https?://[^\s]+|www\.[^\s]+)"
    found = re.findall(pattern, text or "")
    urls = []
    for u in found:
        if u.startswith("www."):
            u = "http://" + u
        urls.append(u.strip(").,]}>\"'"))
    return list(dict.fromkeys(urls))


def url_heuristics(urls):
    findings = []
    shorteners = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "rb.gy", "cutt.ly"}

    for url in urls:
        parsed = urlparse(url)
        host = parsed.netloc.lower().split(":")[0]
        ext = tldextract.extract(url)
        domain = ".".join([p for p in [ext.domain, ext.suffix] if p]).lower()

        flags = []
        score = 0

        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
            flags.append("ip_in_url")
            score += 25

        if domain in shorteners:
            flags.append("shortened_url")
            score += 18

        path_query = f"{parsed.path} {parsed.query}".lower()
        if any(k in path_query for k in ["login", "verify", "update", "secure", "account", "password"]):
            flags.append("suspicious_url_path")
            score += 12

        if host.count(".") >= 3:
            flags.append("many_subdomains")
            score += 8

        findings.append({
            "url": url,
            "domain": domain or host,
            "flags": flags,
            "url_risk": min(score, 40)
        })
    return findings


def keyword_hits(subject: str, body: str):
    text = f"{subject}\n{body}".lower()
    return [k for k in SUSPICIOUS_KEYWORDS if k in text]


def has_credential_request(text: str):
    t = (text or "").lower()
    patterns = [
        "send your password", "confirm your password", "verify your password",
        "enter your password", "share your otp", "confirm otp", "send otp",
        "credit card", "card details", "cvv", "pin code", "bank account number"
    ]
    return any(p in t for p in patterns)


def has_urgency(text: str):
    t = (text or "").lower()
    urgency_terms = [
        "urgent", "immediately", "within 24 hours", "today", "now",
        "final warning", "act now", "suspended", "locked", "expires today"
    ]
    return any(u in t for u in urgency_terms)


def clamp_score(v):
    try:
        v = int(v)
    except Exception:
        v = 50
    return max(0, min(100, v))


def label_from_score(score: int):
    if score >= 70:
        return "Phishing"
    if score >= 40:
        return "Suspicious"
    return "Safe"


def analyze_email(subject: str, body: str):
    subject = subject or ""
    body = body or ""
    full_text = f"{subject}\n{body}"

    urls = extract_urls(body)
    u_findings = url_heuristics(urls)
    k_hits = keyword_hits(subject, body)

    reasons = []
    indicators = []
    score = 8  # baseline

    if k_hits:
        score += min(len(k_hits) * 6, 30)
        reasons.append(f"Suspicious keyword hits: {', '.join(k_hits[:6])}")
        indicators.append("keyword_signal")

    if u_findings:
        url_score_total = sum(u["url_risk"] for u in u_findings)
        score += min(url_score_total, 35)
        indicators.append("url_signal")

        for u in u_findings:
            for f in u["flags"]:
                if f not in indicators:
                    indicators.append(f)

    if has_credential_request(full_text):
        score += 28
        reasons.append("Email requests sensitive credentials/payment details.")
        indicators.append("credential_request")

    if has_urgency(full_text):
        score += 14
        reasons.append("Urgent/threatening language detected.")
        indicators.append("urgency")

    if re.search(r"\bdear customer\b|\bdear user\b", full_text.lower()):
        score += 8
        reasons.append("Generic greeting detected.")
        indicators.append("generic_greeting")

    score = clamp_score(score)
    label = label_from_score(score)

    if not reasons:
        reasons.append("No major phishing indicators detected.")

    return {
        "label": label,
        "risk_score": score,
        "reasons": reasons,
        "indicators": list(dict.fromkeys(indicators)),
        "urls": u_findings,
        "keyword_hits": k_hits,
        "raw_model_output": "Heuristic mode (no external API call)."
    }