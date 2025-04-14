country_to_language = {
    "BR": "portuguese",
    "PT": "portuguese",
    "US": "english",
    "GB": "english",
    "CA": "english",
    "AU": "english",
    "UK": "english",
    "DE": "german",
    "ES": "spanish",
    "FR": "french"
}

_languages = {
    'portuguese': {
        'choose_location': "Deseja escolher um local diferente? (1 - Sim / 0 - Não)",
        'location_prompt': "Qual local deseja pesquisar?",
        'chosen_place': "Local escolhido:",
        'feedback_prompt': "Gostaria de nos contar como está o tempo na sua região?\n1 - Sim\n0 - Não\n",
        'weather_feedback': "Como está o tempo agora na sua região?",
        'weather_update': "=== Atualização do Tempo ===",
        'location': "Localização",
        'current_temp': "Temperatura Atual",
        'condition': "Condição",
        'humidity': "Umidade",
        'wind_speed': "Velocidade do Vento",
        'forecast': "=== Previsão ===",
        'tomorrow': "Amanhã",
        'week_ahead': "Próxima Semana",
        'long_term': "Longo Prazo",
        'climate_trends': "=== Tendências Climáticas ===",
        'trend': "Tendência",
        'confidence': "Confiança"
    },
    'english': {
        'choose_location': "Would you like to choose a different location? (1 - Yes / 0 - No)",
        'location_prompt': "What location would you like to look up?",
        'chosen_place': "Chosen place:",
        'feedback_prompt': "Would you tell us how the weather is in your location?\n1 - Yes\n0 - No\n",
        'weather_feedback': "How is the weather right now in your location?",
        'weather_update': "=== Weather Update ===",
        'location': "Location",
        'current_temp': "Current Temperature",
        'condition': "Condition",
        'humidity': "Humidity",
        'wind_speed': "Wind Speed",
        'forecast': "=== Forecast ===",
        'tomorrow': "Tomorrow",
        'week_ahead': "Week Ahead",
        'long_term': "Long Term",
        'climate_trends': "=== Climate Trends ===",
        'trend': "Trend",
        'confidence': "Confidence"
    },
    'german': {
        'choose_location': "Möchten Sie einen anderen Ort auswählen? (1 - Ja / 0 - Nein)",
        'location_prompt': "Welchen Ort möchten Sie nachschlagen?",
        'chosen_place': "Gewählter Ort:",
        'feedback_prompt': "Möchten Sie uns mitteilen, wie das Wetter an Ihrem Standort ist?\n1 - Ja\n0 - Nein\n",
        'weather_feedback': "Wie ist das Wetter gerade an Ihrem Standort?",
        'weather_update': "=== Wetteraktualisierung ===",
        'location': "Standort",
        'current_temp': "Aktuelle Temperatur",
        'condition': "Zustand",
        'humidity': "Luftfeuchtigkeit",
        'wind_speed': "Windgeschwindigkeit",
        'forecast': "=== Vorhersage ===",
        'tomorrow': "Morgen",
        'week_ahead': "Nächste Woche",
        'long_term': "Langfristig",
        'climate_trends': "=== Klimatrends ===",
        'trend': "Trend",
        'confidence': "Konfidenz"
    },
    'spanish': {
        'choose_location': "¿Le gustaría elegir un lugar diferente? (1 - Sí / 0 - No)",
        'location_prompt': "¿Qué lugar le gustaría buscar?",
        'chosen_place': "Lugar elegido:",
        'feedback_prompt': "¿Nos diría cómo está el clima en su ubicación?\n1 - Sí\n0 - No\n",
        'weather_feedback': "¿Cómo está el clima ahora en su ubicación?",
        'weather_update': "=== Actualización del Tiempo ===",
        'location': "Ubicación",
        'current_temp': "Temperatura Actual",
        'condition': "Condición",
        'humidity': "Humedad",
        'wind_speed': "Velocidad del Viento",
        'forecast': "=== Pronóstico ===",
        'tomorrow': "Mañana",
        'week_ahead': "Próxima Semana",
        'long_term': "Largo Plazo",
        'climate_trends': "=== Tendencias Climáticas ===",
        'trend': "Tendencia",
        'confidence': "Confianza"
    },
    'french': {
        'choose_location': "Souhaitez-vous choisir un autre endroit? (1 - Oui / 0 - Non)",
        'location_prompt': "Quel endroit souhaitez-vous rechercher?",
        'chosen_place': "Lieu choisi:",
        'feedback_prompt': "Voulez-vous nous dire comment est la météo à votre emplacement?\n1 - Oui\n0 - Non\n",
        'weather_feedback': "Quel temps fait-il en ce moment à votre emplacement?",
        'weather_update': "=== Mise à jour Météo ===",
        'location': "Emplacement",
        'current_temp': "Température Actuelle",
        'condition': "Condition",
        'humidity': "Humidité",
        'wind_speed': "Vitesse du Vent",
        'forecast': "=== Prévisions ===",
        'tomorrow': "Demain",
        'week_ahead': "Semaine à Venir",
        'long_term': "Long Terme",
        'climate_trends': "=== Tendances Climatiques ===",
        'trend': "Tendance",
        'confidence': "Confiance"
    }
}

class Language:
    _instance = None
    _language = None
    _dictionary = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Language, cls).__new__(cls)
            cls._instance._set_language()
        return cls._instance
    
    def _set_language(self):
        if self._language is None:
            country = input("Enter either 00(auto-detect) or type your country code (e.g., BR, US, FR): ").strip().upper()
            
            self._language = country_to_language.get(country, "english")  # Padrão para inglês se não encontrado
            self._dictionary = _languages[self._language]
    
    def get_language(self):
        return self._language
    
    def get_dictionary(self):
        return self._dictionary
