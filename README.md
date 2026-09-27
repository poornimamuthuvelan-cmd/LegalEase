# LegalEase: AI-Powered Legal Document Generator

**TNSkill Student Project**

LegalEase is a Python + Streamlit application that demonstrates AI-assisted generation of draft legal-style documents. It is designed as an educational project and does not provide legal advice.

## Features

- Rental Agreement draft generator
- Affidavit / Declaration draft generator
- Permission Letter draft generator
- AI-assisted rewriting with Google Gemini when an API key is configured
- Template/demo mode when no API key is available
- Editable generated text
- PDF export using ReportLab
- Clear educational/legal-review disclaimer

## Technologies

- Python
- Streamlit
- Google Gemini API (optional)
- ReportLab

## Run the project

```bash
pip install -r requirements.txt
streamlit run app.py
```

The application opens in your browser.

## Optional Gemini setup

Set the environment variable `GOOGLE_API_KEY` before starting Streamlit. Never upload an API key to GitHub.

If no API key is configured, LegalEase automatically runs in template/demo mode.

## Project workflow

**Choose document → Enter details → Generate draft → Review/edit → Prepare PDF → Download**

## Disclaimer

LegalEase generates drafts for educational and informational purposes. It is not a substitute for legal advice, legal representation, or professional review. Users should verify all facts and consult a qualified legal professional before using a document for an actual legal matter.

## Prepared by

**M. Poornima**  
**II BCA**  
**S.S.K.V College of Arts and Science for Women**  
**Date: 24.09.2026**
