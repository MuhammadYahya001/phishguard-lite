import streamlit as st
from detector import analyze_email

st.set_page_config(page_title="PhishGuard Lite", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
/* Layout */
.block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px;}

/* Cards */
.card {
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    background: #ffffff;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

/* Muted text */
.muted {color: #6b7280; font-size: 0.9rem; margin-top: -0.3rem;}

/* Badge chips */
.badge {
    display: inline-block;
    background: #f1f5f9;
    color: #334155;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 0.78rem;
    margin: 2px 2px 0 0;
    font-family: monospace;
}

/* Score bar label */
.score-label {font-size: 0.82rem; color: #6b7280; margin-top: 0.1rem;}

/* Footer */
.footer {
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
    color: #9ca3af;
    font-size: 0.82rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("## 🛡️ PhishGuard Lite")
st.markdown(
    "<p class='muted'>Heuristic phishing email detector — no API key required · "
    "<a href='https://github.com/MuhammadYahya001/phishguard-lite' target='_blank'>GitHub</a></p>",
    unsafe_allow_html=True,
)
st.write("")

# ── Sample email helper ──────────────────────────────────────────────────────
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

# ── Main columns ─────────────────────────────────────────────────────────────
c1, c2 = st.columns([1.3, 1], gap="large")

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
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
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### Analysis Result")

    if submitted:
        if not subject.strip() and not body.strip():
            st.warning("⚠️ Please enter a subject or body before analyzing.")
        else:
            with st.spinner("Running heuristic analysis…"):
                r = analyze_email(subject, body)

            label, score = r["label"], r["risk_score"]

            # Verdict banner
            if label == "Phishing":
                st.error(f"🚨 **{label}** — Risk score: **{score} / 100**")
            elif label == "Suspicious":
                st.warning(f"⚠️ **{label}** — Risk score: **{score} / 100**")
            else:
                st.success(f"✅ **{label}** — Risk score: **{score} / 100**")

            st.progress(score / 100)
            st.markdown(f"<p class='score-label'>Score: {score}/100</p>", unsafe_allow_html=True)

            # Reasons
            st.markdown("**Reasons**")
            for reason in r["reasons"]:
                st.markdown(f"- {reason}")

            # Indicators as badges
            st.markdown("**Indicators**")
            if r["indicators"]:
                badges = "".join(
                    f"<span class='badge'>{ind}</span>" for ind in r["indicators"]
                )
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.markdown("<span class='badge'>none</span>", unsafe_allow_html=True)

            # URL analysis
            st.markdown("**URL Analysis**")
            if r["urls"]:
                for u in r["urls"]:
                    flags = ", ".join(u["flags"]) if u["flags"] else "clean"
                    st.markdown(f"- `{u['domain']}` → {flags}")
            else:
                st.write("No URLs detected.")

            with st.expander("🔧 Engine debug output"):
                st.code(r["raw_model_output"])
    else:
        st.info("📧 Enter an email above and click **Analyze Email** to see results.")

    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='footer'>"
    "⚠️ Educational use only — heuristic analysis, not a replacement for enterprise email security.<br>"
    "<a href='https://phishguard-lite.streamlit.app/' target='_blank'>phishguard-lite.streamlit.app</a> · "
    "<a href='https://github.com/MuhammadYahya001/phishguard-lite' target='_blank'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True,
)