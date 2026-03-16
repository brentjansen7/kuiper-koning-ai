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

st.set_page_config(page_title="Kuiper & Koning AI Tool", layout="wide")
st.title("Kuiper & Koning AI Tool")
st.write("Automatisch behandelverslagen genereren in SOAP-format")

st.sidebar.title("Menu")
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

st.divider()
st.caption("Tip: Controleer alles zelf voordat je het in Fysioroadmap zet!")
