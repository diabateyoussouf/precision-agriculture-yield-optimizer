import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import random

# On importe ta fonction depuis l'autre fichier
from meteo_api import obtenir_meteo 

# --- 1. Configuration de la page ---
st.set_page_config(page_title="Smart Farming DIABATEBA", page_icon="🌱", layout="wide")

# --- 2. Base de données agronomique ---
# Ces données servent à la fois pour les recommandations et pour la nouvelle fonction de recherche
BESOINS_CULTURES = {
    'rice': {'N': 90, 'P': 45, 'K': 40},
    'maize': {'N': 100, 'P': 40, 'K': 30},
    'chickpea': {'N': 40, 'P': 60, 'K': 80},
    'kidneybeans': {'N': 20, 'P': 60, 'K': 20},
    'pigeonpeas': {'N': 20, 'P': 60, 'K': 20},
    'mothbeans': {'N': 20, 'P': 40, 'K': 20},
    'mungbean': {'N': 20, 'P': 40, 'K': 20},
    'blackgram': {'N': 40, 'P': 60, 'K': 20},
    'lentil': {'N': 20, 'P': 60, 'K': 20},
    'pomegranate': {'N': 20, 'P': 10, 'K': 40},
    'banana': {'N': 100, 'P': 75, 'K': 50},
    'mango': {'N': 20, 'P': 20, 'K': 30},
    'grapes': {'N': 20, 'P': 120, 'K': 200},
    'watermelon': {'N': 100, 'P': 10, 'K': 50},
    'muskmelon': {'N': 100, 'P': 10, 'K': 50},
    'apple': {'N': 20, 'P': 125, 'K': 200},
    'orange': {'N': 20, 'P': 10, 'K': 10},
    'papaya': {'N': 50, 'P': 50, 'K': 50},
    'coconut': {'N': 20, 'P': 10, 'K': 30},
    'cotton': {'N': 120, 'P': 40, 'K': 20},
    'jute': {'N': 80, 'P': 40, 'K': 40},
    'coffee': {'N': 100, 'P': 20, 'K': 30}
}

EMOJI_CULTURES = {
    'rice': '🍚', 'maize': '🌽', 'chickpea': '🧆', 'kidneybeans': '🫘', 'pigeonpeas': '🫘',
    'mothbeans': '🫘', 'mungbean': '🫘', 'blackgram': '🫘', 'lentil': '🥣', 'pomegranate': '🍅',
    'banana': '🍌', 'mango': '🥭', 'grapes': '🍇', 'watermelon': '🍉', 'muskmelon': '🍈',
    'apple': '🍎', 'orange': '🍊', 'papaya': '🥭', 'coconut': '🥥', 'cotton': '☁️',
    'jute': '🌿', 'coffee': '☕'
}

# --- 3. Fonctions Utilitaires ---
@st.cache_resource
def load_model():
    model = joblib.load('rf_crop_model.pkl') 
    encoder = joblib.load('label_encoder.pkl')
    return model, encoder

def calculer_recommandation_engrais(nutriment, valeur_actuelle, valeur_ideale):
    difference = valeur_ideale - valeur_actuelle
    if difference > 5:
        return f"🔴 **Déficit :** Ajoutez **{difference}** unités."
    elif difference < -5:
        return f"🟡 **Excès :** **{abs(difference)}** unités en trop."
    else:
        return "🟢 **Optimal :** Bon niveau !"

model, encoder = load_model()

if 'temp_locale' not in st.session_state:
    st.session_state.temp_locale = 25.0
if 'hum_locale' not in st.session_state:
    st.session_state.hum_locale = 70.0

# --- 4. Interface Utilisateur (UI) ---

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌱 DIABATEBA Smart Farming</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>L'IA au service de votre rendement agricole</h3>", unsafe_allow_html=True)
st.divider()

# Onglets pour séparer la Prédiction et la Consultation
tab1, tab2 = st.tabs(["🔮 Diagnostic & Prédiction", "📚 Bibliothèque des Cultures"])

with tab1:
    col_gauche, col_droite = st.columns(2, gap="large")

    with col_gauche:
        st.header("🌤️ Climat")
        col_ville, col_btn = st.columns([3, 1])
        with col_ville:
            ville_input = st.text_input("📍 Ville", placeholder="Ex: Settat...")
        with col_btn:
            st.write("") 
            st.write("")
            if st.button("🔍"):
                if ville_input:
                    CLE_API = st.secrets["OPENWEATHER_API_KEY"]
                    t, h = obtenir_meteo(ville_input, CLE_API)
                    if t is not None:
                        st.session_state.temp_locale, st.session_state.hum_locale = float(t), float(h)
                        st.toast(f"Météo mise à jour !", icon="✅")

        temperature = st.number_input("Température (°C)", value=st.session_state.temp_locale)
        humidity = st.number_input("Humidité (%)", value=st.session_state.hum_locale)
        rainfall = st.slider("Pluie (mm)", 0.0, 300.0, 100.0)

    with col_droite:
        st.header("📊 Sol")
        c1, c2, c3 = st.columns(3)
        N = c1.number_input("Azote (N)", 0, 150, 50)
        P = c2.number_input("Phosphore (P)", 0, 150, 50)
        K = c3.number_input("Potassium (K)", 0, 250, 50)
        ph = st.slider("pH du sol", 0.0, 14.0, 6.5, 0.1)

    if st.button("🔮 Lancer le Diagnostic", use_container_width=True, type="primary"):
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(input_data)
        culture_recommandee = encoder.inverse_transform(prediction)[0]
        
        st.success(f"### 🎉 Culture recommandée : **{culture_recommandee.upper()}**")
        
        # Animation rapide d'emojis
        emoji = EMOJI_CULTURES.get(culture_recommandee, '🌱')
        st.markdown(f"<p style='font-size:50px; text-align:center;'>{emoji} {emoji} {emoji} {emoji} {emoji}</p>", unsafe_allow_html=True)

        if culture_recommandee in BESOINS_CULTURES:
            st.info("🧪 **Ajustements nécessaires pour votre sol :**")
            besoins = BESOINS_CULTURES[culture_recommandee]
            res1, res2, res3 = st.columns(3)
            res1.markdown(calculer_recommandation_engrais("N", N, besoins['N']))
            res2.markdown(calculer_recommandation_engrais("P", P, besoins['P']))
            res3.markdown(calculer_recommandation_engrais("K", K, besoins['K']))

# --- NOUVELLE SECTION : BIBLIOTHÈQUE ---
with tab2:
    st.header("📖 Consulter les besoins d'une plante")
    st.write("Sélectionnez une culture pour connaître ses besoins idéaux en nutriments (N-P-K) selon les standards agronomiques.")
    
    # Liste de toutes les cultures disponibles dans ton modèle
    liste_cultures = sorted(list(BESOINS_CULTURES.keys()))
    
    culture_choisie = st.selectbox("Quelle culture vous intéresse ?", options=["-- Choisir une plante --"] + liste_cultures)
    
    if culture_choisie != "-- Choisir une plante --":
        donnees = BESOINS_CULTURES[culture_choisie]
        emoj = EMOJI_CULTURES.get(culture_choisie, '🌱')
        
        st.markdown(f"### {emoj} Fiche Technique : {culture_choisie.upper()}")
        
        # Affichage sous forme de "Cartes" de données
        m1, m2, m3 = st.columns(3)
        m1.metric("Azote (N) idéal", f"{donnees['N']} u")
        m2.metric("Phosphore (P) idéal", f"{donnees['P']} u")
        m3.metric("Potassium (K) idéal", f"{donnees['K']} u")
        
        st.success(f"💡 Pour un rendement optimal de **{culture_choisie}**, le sol doit idéalement être maintenu proche de ces valeurs.")
    else:
        st.info("Utilisez le menu déroulant ci-dessus pour rechercher une plante.")