import streamlit as st
from detector import analyze_email

st.set_page_config(page_title="PhishGuard Lite", page_icon="🛡️", layout="wide")

st.markdown(
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800'
    '&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)

st.markdown("""
<style>

/* ── Global ─────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem;
    max-width: 1140px;
}

/* Hide default Streamlit header decoration */
header[data-testid="stHeader"] { background: transparent; }

/* ── Keyframe animations ─────────────────────────────────────────────────── */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(99, 179, 237, 0); }
    50%       { box-shadow: 0 0 18px 4px rgba(99, 179, 237, 0.35); }
}
@keyframes badge-pop {
    0%   { transform: scale(0.7); opacity: 0; }
    70%  { transform: scale(1.08); }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}
@keyframes result-reveal {
    from { opacity: 0; transform: scale(0.95) translateY(10px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}

/* ── Hero banner ─────────────────────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0f172a 100%);
    background-size: 200% 200%;
    animation: gradientShift 8s ease infinite;
    border-radius: 20px;
    padding: 2.2rem 2.4rem 2rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(99,179,237,0.18);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05);
    animation: fadeInDown 0.6s ease both, gradientShift 8s ease infinite;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #63b3ed, #48bb78, #63b3ed, transparent);
    background-size: 200% 100%;
    animation: shimmer 2.5s linear infinite;
}
.hero::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #f0f9ff;
    margin: 0 0 0.3rem;
    letter-spacing: -0.03em;
    line-height: 1.15;
    text-shadow: 0 2px 20px rgba(99,179,237,0.4);
}
.hero-title span {
    background: linear-gradient(135deg, #63b3ed 0%, #48bb78 50%, #63b3ed 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
}
.hero-sub {
    color: #94a3b8;
    font-size: 0.95rem;
    margin: 0;
    line-height: 1.5;
}
.hero-sub a { color: #63b3ed; text-decoration: none; }
.hero-sub a:hover { text-decoration: underline; }
.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(72, 187, 120, 0.12);
    border: 1px solid rgba(72, 187, 120, 0.3);
    color: #48bb78;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 0.7rem;
    text-transform: uppercase;
}
.hero-pill::before {
    content: '';
    width: 7px; height: 7px;
    background: #48bb78;
    border-radius: 50%;
    box-shadow: 0 0 6px #48bb78;
    display: inline-block;
}

/* ── Cards ───────────────────────────────────────────────────────────────── */
.card {
    border: 1px solid rgba(99,179,237,0.14);
    border-radius: 18px;
    padding: 1.5rem 1.7rem;
    background: linear-gradient(145deg, #1e293b, #0f172a);
    box-shadow: 0 4px 24px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.04);
    animation: fadeInUp 0.5s ease both;
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
    position: relative;
    overflow: hidden;
}
.card:hover {
    border-color: rgba(99,179,237,0.28);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35), 0 0 0 1px rgba(99,179,237,0.12);
}
.card-right { animation-delay: 0.1s; }

.card-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 1rem;
}

/* ── Override Streamlit inputs for dark theme ────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(99,179,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.12) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* ── Analyze button ──────────────────────────────────────────────────────── */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.02em !important;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.55) !important;
}
[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Sample email button ─────────────────────────────────────────────────── */
[data-testid="stBaseButton-secondary"] > button,
button[kind="secondary"] {
    background: rgba(99,179,237,0.1) !important;
    color: #63b3ed !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    transition: background 0.2s, border-color 0.2s !important;
}
button[kind="secondary"]:hover {
    background: rgba(99,179,237,0.18) !important;
    border-color: rgba(99,179,237,0.4) !important;
}

/* ── Verdict banners ─────────────────────────────────────────────────────── */
.verdict {
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.9rem;
    animation: result-reveal 0.4s cubic-bezier(0.34, 1.2, 0.64, 1) both;
    position: relative;
    overflow: hidden;
}
.verdict::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 100%;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.03) 50%, transparent 100%);
    background-size: 200% 100%;
    animation: shimmer 2s linear infinite;
    pointer-events: none;
}
.verdict-phishing {
    background: rgba(220, 38, 38, 0.12);
    border: 1px solid rgba(220, 38, 38, 0.4);
    animation: result-reveal 0.4s cubic-bezier(0.34,1.56,0.64,1) both, pulse-glow 2s ease-in-out 0.4s infinite;
    --glow: rgba(220, 38, 38, 0.35);
}
.verdict-phishing { box-shadow: 0 0 18px rgba(220, 38, 38, 0.25); }
.verdict-suspicious {
    background: rgba(217, 119, 6, 0.12);
    border: 1px solid rgba(217, 119, 6, 0.4);
    box-shadow: 0 0 14px rgba(217, 119, 6, 0.2);
}
.verdict-safe {
    background: rgba(5, 150, 105, 0.12);
    border: 1px solid rgba(5, 150, 105, 0.4);
    box-shadow: 0 0 14px rgba(5, 150, 105, 0.2);
}
.verdict-icon { font-size: 1.6rem; margin-right: 0.5rem; }
.verdict-label {
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}
.verdict-phishing .verdict-label  { color: #fca5a5; }
.verdict-suspicious .verdict-label { color: #fcd34d; }
.verdict-safe .verdict-label       { color: #6ee7b7; }
.verdict-score {
    font-size: 0.82rem;
    font-weight: 500;
    opacity: 0.75;
    margin-top: 0.15rem;
    color: #cbd5e1;
}

/* ── Score bar ───────────────────────────────────────────────────────────── */
.score-bar-wrap {
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin: 0.6rem 0 0.25rem;
    position: relative;
}
.score-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}
.score-bar-fill::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 30px; height: 100%;
    background: rgba(255,255,255,0.3);
    border-radius: 999px;
    filter: blur(4px);
    animation: shimmer 1.5s linear infinite;
}
.score-bar-phishing { background: linear-gradient(90deg, #dc2626, #ef4444); }
.score-bar-suspicious { background: linear-gradient(90deg, #d97706, #f59e0b); }
.score-bar-safe { background: linear-gradient(90deg, #059669, #10b981); }
.score-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.15rem;
}

/* ── Section headings ────────────────────────────────────────────────────── */
.section-head {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin: 1.1rem 0 0.4rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.section-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}

/* ── Reason list ─────────────────────────────────────────────────────────── */
.reason-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.85rem;
    color: #cbd5e1;
    line-height: 1.45;
    animation: fadeInUp 0.3s ease both;
}
.reason-item:last-child { border-bottom: none; }
.reason-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #f59e0b;
    margin-top: 6px;
    flex-shrink: 0;
    box-shadow: 0 0 6px rgba(245, 158, 11, 0.5);
}

/* ── Badge chips ─────────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    background: rgba(99,179,237,0.1);
    color: #93c5fd;
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 999px;
    padding: 3px 11px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 3px 3px 0 0;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
    animation: badge-pop 0.3s ease both;
    transition: background 0.2s, border-color 0.2s;
}
.badge:hover {
    background: rgba(99,179,237,0.2);
    border-color: rgba(99,179,237,0.5);
}
.badge-danger {
    background: rgba(220, 38, 38, 0.12);
    color: #fca5a5;
    border-color: rgba(220, 38, 38, 0.3);
}
.badge-warn {
    background: rgba(217, 119, 6, 0.12);
    color: #fcd34d;
    border-color: rgba(217, 119, 6, 0.3);
}
.badge-safe {
    background: rgba(5, 150, 105, 0.12);
    color: #6ee7b7;
    border-color: rgba(5, 150, 105, 0.3);
}

/* ── URL row ─────────────────────────────────────────────────────────────── */
.url-row {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.5rem 0.8rem;
    margin: 0.35rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    font-size: 0.8rem;
    animation: fadeInUp 0.3s ease both;
}
.url-domain {
    font-family: 'JetBrains Mono', monospace;
    color: #93c5fd;
    font-size: 0.78rem;
    word-break: break-all;
}
.url-flags { flex-shrink: 0; }

/* ── Info placeholder ────────────────────────────────────────────────────── */
.placeholder-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2.5rem 1.5rem;
    text-align: center;
    gap: 0.7rem;
}
.placeholder-icon {
    font-size: 2.8rem;
    filter: drop-shadow(0 0 12px rgba(99,179,237,0.4));
    animation: pulse-glow 3s ease-in-out infinite;
}
.placeholder-text {
    color: #475569;
    font-size: 0.88rem;
    line-height: 1.5;
    max-width: 240px;
}

/* ── Spinner override ────────────────────────────────────────────────────── */
[data-testid="stSpinner"] { color: #63b3ed !important; }

/* ── Expander ────────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
}

/* ── Footer ──────────────────────────────────────────────────────────────── */
.footer {
    margin-top: 2.5rem;
    padding: 1.2rem 0 0.5rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    color: #475569;
    font-size: 0.8rem;
    text-align: center;
    line-height: 1.8;
    animation: fadeInUp 0.5s 0.3s ease both;
}
.footer a { color: #63b3ed; text-decoration: none; }
.footer a:hover { text-decoration: underline; }

/* ── Streamlit alert overrides ───────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 3px !important;
    font-size: 0.875rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-pill">🟢 Live · Heuristic Engine</div>
    <div class="hero-title">🛡️ Phish<span>Guard</span> Lite</div>
    <p class="hero-sub">
        AI-powered phishing email detector — no API key required &nbsp;·&nbsp;
        <a href="https://github.com/MuhammadYahya001/phishguard-lite" target="_blank">GitHub ↗</a>
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sample email helper ───────────────────────────────────────────────────────
SAMPLE_SUBJECT = "Urgent: Your account has been suspended — verify immediately"
SAMPLE_BODY = (
    "Dear Customer,\n\n"
    "Unusual activity was detected on your account. "
    "Click below to confirm your identity and reset your password within 24 hours "
    "or your account will be permanently locked.\n\n"
    "http://secure-login.verify-account.xyz/update\n\n"
    "Failure to comply will result in permanent account termination.\n\n"
    "— Security Team"
)

if "subject_val" not in st.session_state:
    st.session_state["subject_val"] = ""
if "body_val" not in st.session_state:
    st.session_state["body_val"] = ""

if st.button("📋 Load sample phishing email", help="Fills in a realistic phishing example"):
    st.session_state["subject_val"] = SAMPLE_SUBJECT
    st.session_state["body_val"] = SAMPLE_BODY

# ── Main columns ──────────────────────────────────────────────────────────────
c1, c2 = st.columns([1.3, 1], gap="large")

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>✉️ &nbsp;Email Input</div>", unsafe_allow_html=True)
    with st.form("analysis_form"):
        subject = st.text_input(
            "Email Subject",
            value=st.session_state["subject_val"],
            placeholder="e.g. Urgent: Verify your account now",
        )
        body = st.text_area(
            "Email Body",
            value=st.session_state["body_val"],
            height=280,
            placeholder="Paste the full email content here…",
        )
        submitted = st.form_submit_button("🔍 Analyze Email", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card card-right'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>📊 &nbsp;Analysis Result</div>", unsafe_allow_html=True)

    if submitted:
        if not subject.strip() and not body.strip():
            st.warning("⚠️ Please enter a subject or body before analyzing.")
        else:
            with st.spinner("Scanning email for threats…"):
                r = analyze_email(subject, body)

            label, score = r["label"], r["risk_score"]

            # ── Verdict banner ────────────────────────────────────────────
            if label == "Phishing":
                verdict_class = "verdict-phishing"
                icon = "🚨"
                bar_class = "score-bar-phishing"
            elif label == "Suspicious":
                verdict_class = "verdict-suspicious"
                icon = "⚠️"
                bar_class = "score-bar-suspicious"
            else:
                verdict_class = "verdict-safe"
                icon = "✅"
                bar_class = "score-bar-safe"

            st.markdown(f"""
            <div class="verdict {verdict_class}">
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <span class="verdict-icon">{icon}</span>
                    <div>
                        <div class="verdict-label">{label}</div>
                        <div class="verdict-score">Risk score: {score} / 100</div>
                    </div>
                </div>
                <div class="score-bar-wrap">
                    <div class="score-bar-fill {bar_class}" style="width:{score}%;"></div>
                </div>
                <div class="score-meta"><span>0</span><span>50</span><span>100</span></div>
            </div>
            """, unsafe_allow_html=True)

            # ── Reasons ───────────────────────────────────────────────────
            st.markdown("<div class='section-head'>🔎 &nbsp;Reasons</div>", unsafe_allow_html=True)
            reasons_html = "".join(
                f"<div class='reason-item'><div class='reason-dot'></div>{reason}</div>"
                for reason in r["reasons"]
            )
            st.markdown(reasons_html, unsafe_allow_html=True)

            # ── Indicators ────────────────────────────────────────────────
            st.markdown("<div class='section-head'>🏷️ &nbsp;Indicators</div>", unsafe_allow_html=True)
            if r["indicators"]:
                def _badge_cls(ind):
                    danger_terms = ("credential", "ip_in", "phish", "malware", "inject")
                    warn_terms   = ("urgent", "keyword", "shortened", "subdomain", "suspicious", "generic")
                    low = ind.lower()
                    if any(t in low for t in danger_terms): return "badge badge-danger"
                    if any(t in low for t in warn_terms):   return "badge badge-warn"
                    return "badge"
                badges = "".join(
                    f"<span class='{_badge_cls(ind)}'>{ind}</span>" for ind in r["indicators"]
                )
            else:
                badges = "<span class='badge badge-safe'>none</span>"
            st.markdown(f"<div style='margin-top:0.25rem'>{badges}</div>", unsafe_allow_html=True)

            # ── URL analysis ──────────────────────────────────────────────
            st.markdown("<div class='section-head'>🌐 &nbsp;URL Analysis</div>", unsafe_allow_html=True)
            if r["urls"]:
                url_rows = ""
                for u in r["urls"]:
                    flags_html = (
                        "".join(f"<span class='badge badge-danger'>{f}</span>" for f in u["flags"])
                        if u["flags"] else "<span class='badge badge-safe'>clean</span>"
                    )
                    url_rows += f"""
                    <div class='url-row'>
                        <span class='url-domain'>{u['domain']}</span>
                        <span class='url-flags'>{flags_html}</span>
                    </div>"""
                st.markdown(url_rows, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#475569;font-size:0.85rem;margin:0.3rem 0'>No URLs detected.</p>",
                            unsafe_allow_html=True)

            with st.expander("🔧 Engine debug output"):
                st.code(r["raw_model_output"])
    else:
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">📧</div>
            <div class="placeholder-text">
                Enter an email subject and body on the left, then click
                <strong style="color:#63b3ed">Analyze Email</strong> to scan for threats.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='footer'>"
    "⚠️ Educational use only — heuristic analysis, not a replacement for enterprise email security.<br>"
    "<a href='https://phishguard-lite.streamlit.app/' target='_blank'>phishguard-lite.streamlit.app</a> &nbsp;·&nbsp; "
    "<a href='https://github.com/MuhammadYahya001/phishguard-lite' target='_blank'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True,
)