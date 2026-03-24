import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Laad .env bestand (lokaal)
load_dotenv()

# API key: eerst Streamlit Secrets (cloud), dan .env (lokaal)
api_key = st.secrets.get("GROQ_API_KEY", None) or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY niet gevonden! Controleer je .env bestand of Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="Kuiper & Koning AI Tool", layout="wide", page_icon="🏥")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Buttons */
.stButton > button {
    background: #0f766e !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 1px 3px rgba(15,118,110,0.3) !important;
}
.stButton > button:hover {
    background: #0d6961 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(15,118,110,0.35) !important;
}

/* Download button */
.stDownloadButton > button {
    background: white !important;
    color: #0f766e !important;
    border: 1.5px solid #0f766e !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
.stDownloadButton > button:hover {
    background: #f0fdfb !important;
}

/* Text areas & inputs */
.stTextArea textarea, .stTextInput input {
    border-radius: 8px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #0f766e !important;
    box-shadow: 0 0 0 3px rgba(15,118,110,0.12) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f172a !important;
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: #cbd5e1 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding: 1rem 0 2rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 2rem;">
    <span style="font-size: 0.75rem; font-weight: 600; color: #0f766e; letter-spacing: 0.1em; text-transform: uppercase;">Fysiotherapie · AI-assistent</span>
    <h1 style="margin: 0.35rem 0 0.25rem 0; font-size: 1.75rem; font-weight: 700; color: #0f172a; letter-spacing: -0.02em;">Kuiper & Koning</h1>
    <p style="margin: 0; color: #64748b; font-size: 0.95rem;">Genereer behandelverslagen, voortgangsrapporten en herinneringsberichten met AI.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="padding: 0.5rem 0 1.25rem 0; margin-bottom: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.1);">
    <div style="font-size: 1rem; font-weight: 700; color: white; margin-bottom: 0.2rem;">🏥 K&K AI Tool</div>
    <div style="font-size: 0.72rem; color: #94a3b8; letter-spacing: 0.05em;">FYSIOTHERAPIE HULPMIDDELEN</div>
</div>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "Kies een functie:",
    ["SOAP-verslag genereren", "Voortgang samenvatten", "Herinneringsberichten"]
)

if pagina == "SOAP-verslag genereren":
    st.header("Behandelverslag genereren (SOAP-format)")
    st.write("Vul je ruwe aantekeningen in, en AI genereert een professioneel verslag.")

    aantekeningen = st.text_area(
        "Vul hier je behandelaantekeningen in:",
        placeholder="Bijv: patiënt klaagt over rugpijn, bewegingsbeperking L4-L5, mobilisatie gedaan",
        height=150
    )

    if st.button("Verslag genereren"):
        if not aantekeningen.strip():
            st.error("Vul eerst je aantekeningen in!")
        else:
            with st.spinner("AI genereert je verslag..."):
                try:
                    prompt = f"""Je bent een fysiotherapeut. Maak een SOAP-verslag in het Nederlands.

Aantekeningen: {aantekeningen}

Schrijf:
- S (Subjectief): Wat de patiënt zei
- O (Objectief): Wat je hebt gemeten
- A (Analyse): Je diagnose
- P (Plan): Vervolgstappen"""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}]
                    )

                    verslag = response.choices[0].message.content
                    st.success("Verslag gegenereerd!")
                    st.text_area("SOAP-verslag:", value=verslag, height=300)
                    st.download_button(
                        label="Download als .txt",
                        data=verslag,
                        file_name="SOAP-verslag.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Fout: {str(e)}")

elif pagina == "Voortgang samenvatten":
    st.header("Patiëntvoortgang samenvatten")
    st.write("Plak meerdere sessies in en AI maakt een voortgangsrapport.")

    sessies = st.text_area(
        "Vul hier alle behandelsessies in:",
        placeholder="Sessie 1: patiënt met rugpijn...",
        height=200
    )

    if st.button("Samenvatting maken"):
        if not sessies.strip():
            st.error("Vul eerst je sessies in!")
        else:
            with st.spinner("AI analyzeert voortgang..."):
                try:
                    prompt = f"""Je bent een fysiotherapeut. Maak een voortgangssamenvatting (1-2 alinea's) in het Nederlands.

Sessies: {sessies}

Focus op verbeteringen, restklachten en aanbevelingen."""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        max_tokens=800,
                        messages=[{"role": "user", "content": prompt}]
                    )

                    samenvatting = response.choices[0].message.content
                    st.success("Samenvatting klaar!")
                    st.text_area("Voortgangsrapport:", value=samenvatting, height=200)
                    st.download_button(
                        label="Download als .txt",
                        data=samenvatting,
                        file_name="voortgangsrapport.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Fout: {str(e)}")

elif pagina == "Herinneringsberichten":
    st.header("Herinneringsberichten genereren")
    st.write("AI schrijft persoonlijke herinneringen voor patiënten.")

    col1, col2 = st.columns(2)
    with col1:
        naam = st.text_input("Naam patiënt:")
    with col2:
        afspraak = st.text_input("Volgende afspraak (bijv. dinsdag 14:30):")

    laatste_sessie = st.text_area(
        "Wat hebben jullie gedaan in de laatste sessie?:",
        placeholder="Bijv: oefeningen voor schouder"
    )

    if st.button("Bericht genereren"):
        if not (naam and afspraak and laatste_sessie):
            st.error("Vul alle velden in!")
        else:
            with st.spinner("AI schrijft herinneringsbericht..."):
                try:
                    prompt = f"""Schrijf een persoonlijk herinneringsbericht in het Nederlands voor een fysiotherapie-patiënt.

Naam: {naam}
Afspraak: {afspraak}
Vorige sessie: {laatste_sessie}

Maak het vriendelijk, kort (2-3 zinnen), en motiverend."""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        max_tokens=200,
                        messages=[{"role": "user", "content": prompt}]
                    )

                    bericht = response.choices[0].message.content
                    st.success("Bericht klaar!")
                    st.text_area("Herinneringsbericht:", value=bericht, height=150)
                    st.download_button(
                        label="Download als .txt",
                        data=bericht,
                        file_name="herinneringsbericht.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Fout: {str(e)}")

st.markdown("""
<div style="margin-top: 3rem; padding-top: 1.25rem; border-top: 1px solid #e2e8f0;">
    <p style="font-size: 0.8rem; color: #94a3b8; margin: 0;">
        ⚠️ <strong>Let op:</strong> Controleer alle AI-output zelf voordat je het in Fysioroadmap verwerkt.
    </p>
</div>
""", unsafe_allow_html=True)
