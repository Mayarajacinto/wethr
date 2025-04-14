import requests

class Location:
    
    #private
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
    
#We can consume third party api ipinfo that returns our Ip information

#   example_response = self._location = {
#       "ip": "186.235.156.62",
#       "hostname": "YourProvider-mco-20207.186-235-156-62.domain.net.br",
#       "city": "Maceió",
#       "region": "Alagoas",
#       "country": "BR",
#       "loc": "-9.6658,-35.7353",
#       "org": "AS53202 Acesso10 Telecom",
#       "postal": "57000-000",
#       "timezone": "America/Maceio",
#   }
