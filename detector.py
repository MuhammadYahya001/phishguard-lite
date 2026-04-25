import json
import re
from urllib.parse import urlparse

import tldextract
from openai import OpenAI
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


SUSPICIOUS_KEYWORDS = [
    "verify your account", "urgent", "immediately", "suspended", "click below",
    "reset password", "confirm identity", "bank", "wallet", "login now", "otp", "ssn"
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
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
            flags.append("ip_in_url")
        if domain in shorteners:
            flags.append("shortened_url")

        path_query = f"{parsed.path} {parsed.query}".lower()
        if any(k in path_query for k in ["login", "verify", "update", "secure", "account"]):
            flags.append("suspicious_url_path")

        findings.append({"url": url, "domain": domain or host, "flags": flags})
    return findings


def keyword_hits(subject: str, body: str):
    text = f"{subject}\n{body}".lower()
    return [k for k in SUSPICIOUS_KEYWORDS if k in text]


def url_findings_text(findings):
    if not findings:
        return "No URLs found."
    return "\n".join(
        f"- {f['url']} | domain={f['domain']} | flags={','.join(f['flags']) if f['flags'] else 'none'}"
        for f in findings
    )


def safe_json_parse(raw: str):
    try:
        return json.loads(raw)
    except Exception:
        pass
    s, e = raw.find("{"), raw.rfind("}")
    if s != -1 and e != -1 and e > s:
        try:
            return json.loads(raw[s:e+1])
        except Exception:
            return None
    return None


def clamp_score(v):
    try:
        v = int(v)
    except Exception:
        v = 50
    return max(0, min(100, v))


def call_llm(subject: str, body: str, findings_text: str):
    client = OpenAI()
    prompt = USER_PROMPT_TEMPLATE.format(
        subject=subject.strip(),
        body=body.strip(),
        url_findings=findings_text.strip()
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content.strip()


def analyze_email(subject: str, body: str):
    urls = extract_urls(body)
    u_findings = url_heuristics(urls)
    k_hits = keyword_hits(subject, body)

    raw = call_llm(subject, body, url_findings_text(u_findings))
    parsed = safe_json_parse(raw)

    if not parsed:
        score = 20 + len(k_hits) * 8
        for uf in u_findings:
            if "ip_in_url" in uf["flags"]:
                score += 20
            if "shortened_url" in uf["flags"]:
                score += 15
            if "suspicious_url_path" in uf["flags"]:
                score += 10
        score = clamp_score(score)

        label = "Safe"
        if score >= 70:
            label = "Phishing"
        elif score >= 40:
            label = "Suspicious"

        return {
            "label": label,
            "risk_score": score,
            "reasons": [
                "Fallback heuristic used (model output was not valid JSON).",
                f"Keyword hits: {', '.join(k_hits) if k_hits else 'none'}",
            ],
            "indicators": list(set(
                (["keyword_signal"] if k_hits else []) +
                [flag for uf in u_findings for flag in uf["flags"]]
            )),
            "urls": u_findings,
            "keyword_hits": k_hits,
            "raw_model_output": raw,
        }

    label = parsed.get("label", "Suspicious")
    if label not in {"Safe", "Suspicious", "Phishing"}:
        label = "Suspicious"

    reasons = parsed.get("reasons", [])
    indicators = parsed.get("indicators", [])
    if not isinstance(reasons, list):
        reasons = [str(reasons)]
    if not isinstance(indicators, list):
        indicators = [str(indicators)]

    return {
        "label": label,
        "risk_score": clamp_score(parsed.get("risk_score", 50)),
        "reasons": reasons,
        "indicators": indicators,
        "urls": u_findings,
        "keyword_hits": k_hits,
        "raw_model_output": raw,
    }