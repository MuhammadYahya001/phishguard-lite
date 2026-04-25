import streamlit as st
from detector import analyze_email

st.set_page_config(page_title="PhishGuard Lite", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; max-width: 1050px;}
.card {border:1px solid #eaeaea; border-radius:14px; padding:1rem; background:#fff;}
.muted {color:#6b7280; font-size:0.92rem;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ PhishGuard Lite")
st.markdown("<div class='muted'>Free heuristic phishing detector (no API key required)</div>", unsafe_allow_html=True)
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
            for reason in r["reasons"]:
                st.write(f"- {reason}")

            st.markdown("**Indicators**")
            st.write(", ".join(r["indicators"]) if r["indicators"] else "None")

            st.markdown("**URL Analysis**")
            if r["urls"]:
                for u in r["urls"]:
                    flags = ", ".join(u["flags"]) if u["flags"] else "none"
                    st.write(f"- `{u['domain']}` → {flags}")
            else:
                st.write("No URLs found.")

            with st.expander("Engine Output (debug)"):
                st.code(r["raw_model_output"])
    else:
        st.info("Submit an email to see analysis.")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Educational use only — heuristic analysis, not a replacement for enterprise email security.")