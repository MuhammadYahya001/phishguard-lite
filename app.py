import os
import streamlit as st
from detector import analyze_email

st.set_page_config(page_title="PhishGuard Lite", page_icon="🛡️", layout="wide")

# OpenRouter key check (instead of OPENAI_API_KEY)
if not os.getenv("OPENROUTER_API_KEY"):
    st.error("Missing OPENROUTER_API_KEY in secrets/.env")
    st.stop()

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; max-width: 1050px;}
.card {border:1px solid #eaeaea; border-radius:14px; padding:1rem; background:#fff;}
.muted {color:#6b7280; font-size:0.92rem;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ PhishGuard Lite")
st.markdown("<div class='muted'>AI-powered phishing email detector with URL + language analysis</div>", unsafe_allow_html=True)
st.write("")

c1, c2 = st.columns([1.25, 1], gap="large")

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    with st.form("f"):
        subject = st.text_input("Email Subject", placeholder="Urgent: Verify your account now")
        body = st.text_area("Email Body", height=260, placeholder="Paste email content...")
        submitted = st.form_submit_button("Analyze", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Result")

    if submitted:
        if not subject.strip() and not body.strip():
            st.warning("Please enter subject or body.")
        else:
            with st.spinner("Analyzing..."):
                r = analyze_email(subject, body)

            label, score = r["label"], r["risk_score"]

            if label == "Phishing":
                st.error(f"**{label}** — Risk: **{score}/100**")
            elif label == "Suspicious":
                st.warning(f"**{label}** — Risk: **{score}/100**")
            else:
                st.success(f"**{label}** — Risk: **{score}/100**")

            st.progress(score)

            st.markdown("**Reasons**")
            for reason in r.get("reasons", []):
                st.write(f"- {reason}")

            st.markdown("**Indicators**")
            inds = r.get("indicators", [])
            st.write(", ".join(inds) if inds else "None")

            st.markdown("**URL Analysis**")
            urls = r.get("urls", [])
            if urls:
                for u in urls:
                    flags = ", ".join(u.get("flags", [])) if u.get("flags") else "none"
                    st.write(f"- `{u.get('domain', 'unknown')}` → {flags}")
            else:
                st.write("No URLs found.")

            with st.expander("Model Output (debug)"):
                st.code(r.get("raw_model_output", "N/A"))
    else:
        st.info("Submit an email to see analysis.")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Educational use only — not a replacement for enterprise email security.")