# Bem vindo ao Wethr
 Projeto inicial de Projeto de Software

## Executar main.py

O projeto **Wethr App** utiliza vários **fundamentos da Programação Orientada a Objetos (OOP)** para organizar e estruturar o código de forma modular e reutilizável. Vamos analisar os principais conceitos aplicados:

---

## Requisitos do Projeto
- Weather Data Collection: weather/WeatherDataCollector;
- Forecast Generation: weather/WeatherForecaster;
- User Location Services: location/Location;
- Alert System for Severe Weather: weather/WeatherAlertSystem;
- Historical Weather Data Access: weather/HistoricalWeatherData;
- Customizable Weather Widgets: (Não foi implementada por não ter interface gráfica);
- Interactive Weather Maps: (Não foi implementada por não ter interface gráfica);
- Climate Analytics and Reporting: weather/ClimateAnalytics;
- User Feedback and Reporting: main/get_weather_feedback;
- Multi-Language Support: languages/Language;
  
---

## **1. Encapsulamento**

- No módulo `location.py`, a classe `Location` usa um **atributo privado** (`_location`) para armazenar a localização do usuário. Esse atributo só pode ser acessado indiretamente através do método `get_location()`:

```python
class Location:
    _instance = None
    _location = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Location, cls).__new__(cls)
            cls._instance.set_location()
        return cls._instance

    def set_location(self):
        response = requests.get("https://ipinfo.io/json")
        self._location = response.json()

    def get_location(self):
        if self._location is None:
            self.set_location()
        return self._location
```

**Vantagens:**  
- Protege os dados internos da classe (`_location`).
- Apenas métodos específicos (`get_location()`) podem acessar ou modificar `_location`.

---

## **2. Herança**

- `WeatherService` é uma **classe base** (superclasse) para diferentes serviços climáticos, como `WeatherDataCollector`, `WeatherForecaster` e `HistoricalWeatherData`.

```python
class WeatherService:
    def __init__(self, service_name, language="english"):
        self.service_name = service_name
        self.language = language
```

Agora, outras classes podem **herdar** essa base e estender suas funcionalidades:

```python
class WeatherDataCollector(WeatherService):
    def collect_data(self, location):
        weather_data = {
            "temperature": random.uniform(-10, 40),
            "humidity": random.randint(20, 90),
            "wind_speed": random.uniform(0, 20),
            "condition": random.choice(["Sunny", "Rainy", "Cloudy", "Snowy", "Windy"])
        }
        print(f"[{self.service_name}] Dados coletados para {location}: {weather_data}\n")
        return weather_data
```

**Vantagens:**  
- Evita duplicação de código.
- Permite reuso e fácil manutenção.

---

## **3. Polimorfismo**

- `WeatherService` é genérico, mas cada classe filha (`WeatherDataCollector`, `WeatherForecaster`, `WeatherAlertSystem`) tem sua própria implementação de métodos.

```python
class WeatherAlertSystem(WeatherService):
    def check_for_alerts(self, weather_data):
        if weather_data["condition"] in ["Stormy", "Snowy"] or weather_data["wind_speed"] > 15:
            alert_message = f"{self.service_name} alerta: {weather_data['condition']}!"
            print(alert_message)
            return alert_message
        return "Sem alertas de tempo severo."
```
**Vantagens:**  
- Cada serviço climático implementa sua própria lógica sem precisar modificar a classe base.

---

## **4. Abstração**

- O usuário do sistema não precisa saber **como** os dados climáticos são coletados, apenas usa `system.get_weather_update(city)` para obter a previsão.

```python
class WeatherForecastingSystem:
    def __init__(self, language="english"):
        self.weather_collector = WeatherDataCollector("Weather Data Collector", language)
        self.forecaster = WeatherForecaster("Weather Forecaster", language)
        self.alert_system = WeatherAlertSystem("Weather Alert System", language)
        self.historical_data = HistoricalWeatherData()
        self.analytics = ClimateAnalytics("Climate Analytics", language)

    def get_weather_update(self, location):
        weather_info = self.weather_collector.collect_data(location)
        forecast = self.forecaster.generate_forecast(weather_info)
        alert = self.alert_system.check_for_alerts(weather_info)
        self.historical_data.store_weather_data(location, weather_info)
        return {"weather_info": weather_info, "forecast": forecast, "alert": alert}
```
