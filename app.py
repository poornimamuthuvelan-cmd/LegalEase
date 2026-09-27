import os
from datetime import date
from pathlib import Path

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="centered")

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")
st.caption("TNSkill Student Project • II BCA")

st.warning(
    "LegalEase creates draft documents for educational and informational purposes. "
    "Review every document carefully and consult a qualified legal professional before using it for an actual legal matter."
)

DOCUMENTS = {
    "Rental Agreement": "rental",
    "Affidavit / Declaration": "affidavit",
    "Permission Letter": "permission",
}

doc_type = st.selectbox("Choose a document type", list(DOCUMENTS.keys()))

if "draft" not in st.session_state:
    st.session_state.draft = ""

with st.form("document_form"):
    st.markdown("### Enter document details")
    name = st.text_input("Your / Applicant Name")
    address = st.text_area("Address", height=80)

    if doc_type == "Rental Agreement":
        other_name = st.text_input("Landlord Name")
        property_address = st.text_area("Rental Property Address", height=70)
        rent = st.text_input("Monthly Rent (₹)")
        deposit = st.text_input("Security Deposit (₹)")
        duration = st.text_input("Agreement Duration", placeholder="Example: 11 months")
        start_date = st.date_input("Start Date", value=date.today())
        extra = st.text_area("Additional Terms (optional)", height=80)
    elif doc_type == "Affidavit / Declaration":
        purpose = st.text_area("Purpose / Declaration Statement", height=120)
        place = st.text_input("Place")
        declaration_date = st.date_input("Declaration Date", value=date.today())
    else:
        authority = st.text_input("Permission To / Authority Name")
        purpose = st.text_area("Purpose of Permission", height=100)
        location = st.text_input("Location")
        start_date = st.date_input("Start Date", value=date.today())
        end_date = st.date_input("End Date", value=date.today())
        extra = st.text_area("Additional Notes (optional)", height=80)

    submitted = st.form_submit_button("✨ Generate Draft", use_container_width=True)


def template_draft():
    if doc_type == "Rental Agreement":
        return f"""RENTAL AGREEMENT — DRAFT

This draft agreement is prepared for educational purposes.

Landlord: {other_name}
Tenant: {name}
Tenant Address: {address}
Rental Property: {property_address}
Monthly Rent: ₹{rent}
Security Deposit: ₹{deposit}
Duration: {duration}
Start Date: {start_date}

Terms:
1. The tenant agrees to pay the stated rent according to the mutually agreed schedule.
2. The property shall be used for lawful purposes.
3. The parties should agree in writing on maintenance, notice, deposit return, utilities, and other applicable terms.
4. Any additional terms should be reviewed and agreed upon by both parties.

Additional Terms:
{extra}

Tenant Signature: ____________________
Landlord Signature: __________________
Date: _______________________________
"""
    if doc_type == "Affidavit / Declaration":
        return f"""AFFIDAVIT / DECLARATION — DRAFT

I, {name}, residing at {address}, make the following declaration for the stated purpose.

Purpose:
{purpose}

I declare that the information stated above is true to the best of my knowledge and belief, subject to verification and applicable law.

Place: {place}
Date: {declaration_date}

Declarant Signature: __________________
Name: {name}
"""
    return f"""PERMISSION LETTER — DRAFT

To: {authority}

From: {name}
Address: {address}

Subject: Request for Permission

I respectfully request permission for the following purpose:

{purpose}

Location: {location}
Period: {start_date} to {end_date}

Additional Notes:
{extra}

Kindly consider this request according to the applicable rules and requirements.

Applicant Signature: __________________
Name: {name}
Date: ________________________________
"""


def ai_draft(base_text):
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key or not GEMINI_AVAILABLE:
        return base_text
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "Rewrite the following draft into clear, neutral, professional legal-style language. "
            "Do not invent facts, laws, clauses, dates, fees, rights, or obligations. Preserve every supplied fact. "
            "Keep it clearly labelled as a DRAFT for educational use. Return only the document text.\n\n" + base_text
        )
        response = model.generate_content(prompt)
        return response.text if getattr(response, "text", None) else base_text
    except Exception:
        return base_text


if submitted:
    if not name.strip():
        st.error("Please enter your / applicant name.")
    else:
        with st.spinner("Preparing your draft..."):
            st.session_state.draft = ai_draft(template_draft())
        st.success("Draft generated. Please review and edit it before downloading.")

if st.session_state.draft:
    st.markdown("### Review and edit")
    st.session_state.draft = st.text_area(
        "Generated document",
        value=st.session_state.draft,
        height=520,
        label_visibility="collapsed",
    )

    def make_pdf(text, filename):
        out = Path("generated_documents") / filename
        out.parent.mkdir(exist_ok=True)
        doc = SimpleDocTemplate(
            str(out), pagesize=A4,
            rightMargin=18*mm, leftMargin=18*mm,
            topMargin=18*mm, bottomMargin=18*mm,
        )
        styles = getSampleStyleSheet()
        title = ParagraphStyle("Title", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=10)
        body = ParagraphStyle("Body", parent=styles["BodyText"], leading=15, spaceAfter=7)
        story = [Paragraph("LegalEase — Draft Document", title)]
        for para in text.split("\n"):
            safe = para.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe if safe.strip() else "&nbsp;", body))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Educational draft — professional legal review is recommended before real-world use.", body))
        doc.build(story)
        return out

    if st.button("📥 Prepare PDF", use_container_width=True):
        safe_name = "legal_ease_draft.pdf"
        pdf_path = make_pdf(st.session_state.draft, safe_name)
        st.session_state.pdf_bytes = pdf_path.read_bytes()
        st.success("PDF is ready.")

    if "pdf_bytes" in st.session_state:
        st.download_button(
            "⬇️ Download PDF",
            data=st.session_state.pdf_bytes,
            file_name="LegalEase_Draft.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

with st.sidebar:
    st.header("About LegalEase")
    st.write("LegalEase is a student project that demonstrates AI-assisted drafting of common document formats.")
    st.markdown("**Technologies**")
    st.write("Python • Streamlit • Google Gemini API • ReportLab")
    st.markdown("**AI mode**")
    if os.getenv("GOOGLE_API_KEY") and GEMINI_AVAILABLE:
        st.write("Gemini enabled")
    else:
        st.write("Template/demo mode (no API key required)")
