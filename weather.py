import random
import datetime
import json
import os
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class WeatherService:
    """
    Base class for all weather-related services implementing the Singleton pattern.
    Manages language and location settings across the system.
    """
    _instances: Dict[str, Any] = {}  # Store instances for each subclass
    
    def __new__(cls, language: str = "english", location: str = "Washington DC"):
        # Implement proper singleton pattern per subclass
        if cls not in cls._instances:
            instance = super().__new__(cls)
            instance._language = language
            instance._location = location
            instance._initialize(language, location)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    def _initialize(self, language: str, location: str) -> None:
        """Protected initialization method to be called only once"""
        self._language = language
        self._location = location
        self.service_name = self.__class__.__name__
    
    @staticmethod
    def get_translation(language: str, key: str) -> str:
        """
        Get translated text based on language and key.
        Moved from global scope to class method for better encapsulation.
        """
        translations = {
            "portuguese": {
                "data_collected": "Dados coletados para",
                "forecast_generated": "Previsão gerada",
                "weather_alert": "Alerta de Tempo",
                "no_alerts": "Sem alertas de tempo severo.",
                "data_stored": "Dados armazenados para",
                "climate_trend": "Análise da tendência climática"
            },
            "english": {
                "data_collected": "Data collected for",
                "forecast_generated": "Forecast generated",
                "weather_alert": "Weather Alert",
                "no_alerts": "No severe weather alerts.",
                "data_stored": "Data stored for",
                "climate_trend": "Climate trend analysis"
            }
        }
        return translations.get(language, translations["english"]).get(key, key)

# gera dados meteorologicos laeatorios 
class WeatherDataCollector(WeatherService):
    def collect_data(self, location: str) -> Dict[str, Any]:
        """Collect weather data for a specific location"""
        weather_data = {
            "temperature": round(random.uniform(-10, 40), 2),
            "humidity": random.randint(20, 90),
            "wind_speed": round(random.uniform(0, 20), 2),
            "condition": random.choice(["Sunny", "Rainy", "Cloudy", "Snowy", "Windy"])
        }
        #print(f"[{self.service_name}] {self.get_translation(self._language, 'data_collected')} {location}: {weather_data}")
        return weather_data

#cria pevisões baseadas nos dados 
class WeatherForecaster(WeatherService):
    def generate_forecast(self, current_weather: Dict[str, Any]) -> Dict[str, str]:
        """Geração direta da previsão (sem estratégia)"""
        return {
            "tomorrow": self._predict_next_day(current_weather),
            "week_ahead": self._predict_week_ahead(current_weather),
            "long_term": self._predict_long_term(current_weather)
        }
    
    def _predict_next_day(self, current_weather: Dict[str, Any]) -> str:
        return "Sunny" if current_weather["temperature"] > 20 else "Cloudy"
    
    def _predict_week_ahead(self, current_weather: Dict[str, Any]) -> str:
        return "Mostly Sunny"
    
    def _predict_long_term(self, current_weather: Dict[str, Any]) -> str:
        return "Warming Trend"

#verifica se deve emitir alertas 
class WeatherAlertSystem(WeatherService):
    def check_for_alerts(self, weather_data: Dict[str, Any]) -> str:
        """Check weather conditions and issue alerts if necessary"""
        if self._should_issue_alert(weather_data):
            alert_message = f"{self.get_translation(self._language, 'weather_alert')}: {weather_data['condition']}!"
            #print(f"[{self.service_name}] {alert_message}")
            return alert_message
        return self.get_translation(self._language, "no_alerts")
    
    def _should_issue_alert(self, weather_data: Dict[str, Any]) -> bool:
        """Determine if weather conditions warrant an alert"""
        return (weather_data["condition"] in ["Stormy", "Snowy"] or 
                weather_data["wind_speed"] > 15 or 
                weather_data["temperature"] > 35 or 
                weather_data["temperature"] < -5)

# salva e carrega histprico de tempo em .json
class HistoricalWeatherData(WeatherService):
    def _initialize(self, language: str, location: str) -> None:
        """Initialize historical data storage"""
        super()._initialize(language, location)
        self.filename = "weather_history.json"
        self.history = self._load_weather_data()

    def _load_weather_data(self) -> Dict[str, Any]:
        """Load historical weather data from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                #print(f"[{self.service_name}] Error loading history. Creating new file.")
                return {}
        return {}

    def store_weather_data(self, location: str, data: Dict[str, Any]) -> None:
        """Store weather data with timestamp"""
        date = datetime.datetime.now().isoformat()
        
        if location not in self.history:
            self.history[location] = {}
        
        self.history[location][date] = data
        
        self._save_to_file()
        #print(f"[{self.service_name}] {self.get_translation(self._language, 'data_stored')} {location} ({date})")

    def _save_to_file(self) -> None:
        """Save historical data to JSON file"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.history, file, ensure_ascii=False, indent=4)

    def get_weather_history(self, location: Optional[str] = None) -> Dict[str, Any]:
        """Get historical weather data for a location"""
        location = location or self._location
        return self.history.get(location, {})

#analisa tendencias climáticas com base nos dados históricos
class ClimateAnalytics(WeatherService):
    def analyze_trends(self, location: Optional[str] = None) -> Dict[str, Any]:
        """Analyze climate trends for a location"""
        history = HistoricalWeatherData().get_weather_history(location or self._location)
        
        trend_analysis = {
            "trend": random.choice(["Warming", "Cooling", "Stable"]),
            "confidence": random.uniform(0.7, 0.99),
            "analyzed_datapoints": len(history)
        }
        
        #print(f"[{self.service_name}] {self.get_translation(self._language, 'climate_trend')}: {trend_analysis}")
        return trend_analysis

#adiconado o metodo Abstract factory 
class WeatherForecastingSystem:
    def __init__(self, factory: "WeatherServiceFactory"):
        self.weather_collector = factory.create_collector()
        self.forecaster = factory.create_forecaster()
        self.alert_system = factory.create_alert_system()
        self.historical_data = factory.create_historical_data()
        self.analytics = factory.create_analytics()
        
        self.location = self.weather_collector._location
        self.language = self.weather_collector._language


    def get_weather_update(self) -> Dict[str, Any]:
        """Get comprehensive weather update for the current location"""
        weather_info = self.weather_collector.collect_data(self.location)
        forecast = self.forecaster.generate_forecast(weather_info)
        alert = self.alert_system.check_for_alerts(weather_info)
        self.historical_data.store_weather_data(self.location, weather_info)
        trends = self.analytics.analyze_trends(self.location)
        
        return {
            "location": self.location,
            "timestamp": datetime.datetime.now().isoformat(),
            "current_weather": weather_info,
            "forecast": forecast,
            "alerts": alert,
            "climate_trends": trends
        }

class WeatherServiceFactory:
    def create_collector(self): pass
    def create_forecaster(self): pass
    def create_alert_system(self): pass
    def create_historical_data(self): pass
    def create_analytics(self): pass

#abstract factory
#cria familias de objetos relacionados sem acoplamento direto 
#para desconectar a criação dos serviços e facilitar atualizações no futuro 
class DefaultWeatherServiceFactory(WeatherServiceFactory):
    def __init__(self, language: str, location: str):
        self.language = language
        self.location = location
        
    def create_collector(self):
        return WeatherDataCollector(self.language, self.location)

    def create_forecaster(self):
        return WeatherForecaster(self.language, self.location)

    def create_alert_system(self):
        return WeatherAlertSystem(self.language, self.location)

    def create_historical_data(self):
        return HistoricalWeatherData(self.language, self.location)

    def create_analytics(self):
        return ClimateAnalytics(self.language, self.location)

#metodo estrutural adicionado 
#Facade 
#usada para centralizar e simplificar o acesso aos serviços 
class WeatherFacade:
    """Facade para simplificar o acesso aos serviços de previsão do tempo."""
    
    def __init__(self, language: str = "english", location: str = "Washington DC"):
        self.factory = DefaultWeatherServiceFactory(language, location)
        self.forecasting_system = WeatherForecastingSystem(self.factory)
    
    def get_weather_update(self) -> Dict[str, Any]:
        """informações meteorológicas."""
        return self.forecasting_system.get_weather_update()
    
    def get_historical_data(self) -> Dict[str, Any]:
        """dados históricos."""
        return self.forecasting_system.historical_data.get_weather_history()
    
    def get_climate_trends(self) -> Dict[str, Any]:
        """tendências climáticas."""
        return self.forecasting_system.analytics.analyze_trends()



