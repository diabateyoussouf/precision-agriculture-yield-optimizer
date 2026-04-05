# precision-agriculture-yield-optimizer
# 🌱 DIABATEBA Smart Farming - Optimiseur de Rendement Agricole

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://diabateyoussouf-precision-agriculture-yield-optimize-app-gx9ayf.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-orange.svg)]()

**DIABATEBA Smart Farming** est une application web intelligente conçue pour aider les agriculteurs à optimiser leurs rendements. Grâce à l'Intelligence Artificielle et aux données météorologiques en temps réel, l'application recommande la culture la plus adaptée à un terrain spécifique et génère un plan de fertilisation sur mesure (idéal pour des contextes agronomiques comme ceux de l'OCP).

👉 **[ESSAYER L'APPLICATION EN DIRECT ICI](https://diabateyoussouf-precision-agriculture-yield-optimize-app-gx9ayf.streamlit.app/)**

---

## ✨ Fonctionnalités Principales

* **🌤️ Météo en Temps Réel :** Intégration de l'API OpenWeatherMap pour récupérer automatiquement la température et l'humidité d'une ville donnée.
* **🔮 Prédiction IA :** Utilisation d'un modèle de Machine Learning (Random Forest) pour prédire la meilleure culture parmi 22 variétés en fonction de 7 paramètres (Azote, Phosphore, Potassium, pH, Température, Humidité, Pluviométrie).
* **🧪 Plan de Fertilisation :** Calcul automatique des déficits ou excès en nutriments (N-P-K) du sol de l'utilisateur par rapport aux besoins idéaux de la plante recommandée.
* **📚 Bibliothèque Agronomique :** Un onglet dédié pour consulter les fiches techniques et les besoins standards de chaque culture prise en charge par le modèle.

---

## 🛠️ Technologies Utilisées

* **Interface Web :** [Streamlit](https://streamlit.io/)
* **Machine Learning :** Scikit-Learn (RandomForestClassifier)
* **Manipulation de données :** Pandas, NumPy
* **API Externe :** OpenWeatherMap API (via `requests`)
* **Déploiement :** Streamlit Community Cloud

---

## 🚀 Installation en local

Si vous souhaitez exécuter ce projet sur votre propre machine, suivez ces étapes :

### 1. Cloner le dépôt
```bash
git clone [https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_DEPOT.git](https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_DEPOT.git)
cd VOTRE_DEPOT
