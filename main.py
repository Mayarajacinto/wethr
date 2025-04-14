"""
Wethr App - A Weather Forecasting and Analysis System

This program provides weather forecasts, historical data analysis, and climate trends
for user-specified locations. It supports multiple languages and can use either
user-provided locations or automatically detected ones.

Author: Caio Daniel de Jesus Cavalcante
Github: @caiojcavalcante
Repository: caiojcavalcante/wethr
Email: cdjc@ic.ufal.br
"""

import sys
from typing import Dict, Any, Optional
import weather
import languages as lang
import location

class WethrApp:
    """Main application class for the Wethr system"""
    
    def __init__(self):
        """Initialize the Wethr application with language and location services"""
        # Initialize language settings
        self.language_service = lang.Language()
        self.language = self.language_service.get_language()
        self.dictionary = self.language_service.get_dictionary()
        
        # Initialize location service
        self.location_service = location.Location()
        
        # Weather system will be initialized once we have the location
        self.weather_system = None
    
    def get_user_location(self) -> str:
        """
        Prompt user for location preference and return the chosen city.
        Returns either automatically detected or manually entered location.
        """
        user_location = self.location_service.get_location()
        
        print(f"[User Location Services] {self.dictionary['choose_location']}")
        try:
            use_detected = int(input())
            
            if use_detected:
                return input(self.dictionary['location_prompt'])
            return user_location['city']
            
        except ValueError:
            print(f"Error: {self.dictionary.get('invalid_input', 'Invalid input')}") 
            return user_location['city']  # Default to detected location on error
    
    def get_weather_feedback(self) -> Optional[str]:
        """
        Collect weather feedback from the user if they choose to provide it.
        Returns the feedback text or None if user declines.
        """
        try:
            if int(input(self.dictionary['feedback_prompt'])):
                return input(self.dictionary['weather_feedback'])
        except ValueError:
            print(f"Error: {self.dictionary.get('invalid_input', 'Invalid input')}")
        return None
    
    def display_weather_info(self, weather_update: Dict[str, Any]) -> None:
        """Display formatted weather information to the user in the selected language"""
        # Get dictionary for current language
        d = self.dictionary
        
        print(f"\n{d['weather_update']}")
        print(f"{d['location']}: {weather_update['location']}")
        print(f"{d['current_temp']}: {weather_update['current_weather']['temperature']}°C")
        print(f"{d['condition']}: {weather_update['current_weather']['condition']}")
        print(f"{d['humidity']}: {weather_update['current_weather']['humidity']}%")
        print(f"{d['wind_speed']}: {weather_update['current_weather']['wind_speed']} m/s")
        
        print(f"\n{d['forecast']}")
        print(f"{d['tomorrow']}: {weather_update['forecast']['tomorrow']}")
        print(f"{d['week_ahead']}: {weather_update['forecast']['week_ahead']}")
        print(f"{d['long_term']}: {weather_update['forecast']['long_term']}")
        
        if weather_update['alerts'] != self.weather_system.alert_system.get_translation(self.language, "no_alerts"):
            print(f"\n⚠️ {weather_update['alerts']}")
        
        print(f"\n{d['climate_trends']}")
        print(f"{d['trend']}: {weather_update['climate_trends']['trend']}")
        print(f"{d['confidence']}: {weather_update['climate_trends']['confidence']:.2%}")
        
    def run(self) -> None:
        """Main application loop"""
        try:
            # Get user's preferred location
            city = self.get_user_location()
            print(f"{self.dictionary['chosen_place']} [ {city} ]")
            
            # Initialize weather system with chosen location
            self.weather_system = weather.WeatherForecastingSystem(
                location=city,
                language=self.language
            )
            
            # Get and display weather update
            weather_update = self.weather_system.get_weather_update()
            self.display_weather_info(weather_update)
            
            # Collect user feedback
            feedback = self.get_weather_feedback()
            if feedback and hasattr(self.weather_system, 'feedback_system'):
                self.weather_system.feedback_system.submit_report(city, feedback)
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            sys.exit(1)

app = WethrApp()
app.run()
