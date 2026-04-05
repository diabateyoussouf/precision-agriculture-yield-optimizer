import requests

def obtenir_meteo(ville, api_key):
    """
    Interroge l'API OpenWeatherMap pour récupérer la météo d'une ville.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric"
    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            donnees = reponse.json()
            return donnees['main']['temp'], donnees['main']['humidity']
    except Exception as e:
        print(f"Erreur de connexion API : {e}")
    return None, None