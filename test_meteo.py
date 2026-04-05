import requests

def debug_meteo(ville, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric"
    
    print(f"🌍 Envoi de la requête pour {ville}...")
    reponse = requests.get(url)
    
    print(f"📡 Code de statut HTTP : {reponse.status_code}")
    
    if reponse.status_code == 200:
        print("✅ La clé est ENFIN active !")
        print(reponse.json())
    elif reponse.status_code == 401:
        print("⏳ Erreur 401 : La clé existe mais n'est pas encore activée par les serveurs d'OpenWeatherMap.")
        print("Message exact du serveur :", reponse.json())
    else:
        print(f"❌ Autre erreur : {reponse.json()}")

# On lance le test
ma_cle_api = "f5e5abee17575b21a5bc57b3c48ce4d5"
debug_meteo("Settat", ma_cle_api)