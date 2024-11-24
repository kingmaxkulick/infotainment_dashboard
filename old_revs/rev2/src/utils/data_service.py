import requests
from PyQt6.QtCore import QObject, pyqtSignal
import json

class DataService(QObject):
    data_updated = pyqtSignal(dict)
    
    def __init__(self, base_url="http://192.168.5.172:8000"):
        super().__init__()
        self.base_url = base_url
        
    def fetch_vehicle_data(self):
        try:
            response = requests.get(f"{self.base_url}/vehicle_data")
            data = response.json()
            self.data_updated.emit(data)
            return data
        except requests.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return None