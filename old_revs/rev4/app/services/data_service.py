"""
Service for fetching and managing vehicle data from the backend API
"""
import requests
import logging
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from ..utils.constants import API_BASE_URL, API_ENDPOINTS, UPDATE_INTERVALS

class DataService(QObject):
    # Signals for different data updates
    data_updated = pyqtSignal(dict)
    state_updated = pyqtSignal(dict)
    fault_updated = pyqtSignal(dict)
    connection_status_changed = pyqtSignal(bool)
    
    def __init__(self, base_url=API_BASE_URL):
        super().__init__()
        self.base_url = base_url
        self.connected = False
        self.session = requests.Session()
        self.last_state_counter = 0
        
        # Setup update timers
        self.state_timer = QTimer()
        self.state_timer.timeout.connect(self.fetch_state)
        self.state_timer.start(UPDATE_INTERVALS["vehicle_state"])
        
        self.fault_timer = QTimer()
        self.fault_timer.timeout.connect(self.fetch_fault_status)
        self.fault_timer.start(UPDATE_INTERVALS["fault_status"])
        
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.fetch_vehicle_data)
        self.metrics_timer.start(UPDATE_INTERVALS["metrics"])
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
    def fetch_vehicle_data(self):
        """Fetch all vehicle data"""
        try:
            response = self.session.get(
                f"{self.base_url}{API_ENDPOINTS['vehicle_data']}",
                timeout=1.0
            )
            if response.status_code == 200:
                data = response.json()
                self.data_updated.emit(data)
                if not self.connected:
                    self.connected = True
                    self.connection_status_changed.emit(True)
                return data
        except requests.RequestException as e:
            self.handle_connection_error(f"Failed to fetch vehicle data: {e}")
        return None

    def fetch_state(self):
        """Fetch vehicle state information"""
        try:
            response = self.session.get(
                f"{self.base_url}{API_ENDPOINTS['vehicle_state']}",
                timeout=0.5
            )
            if response.status_code == 200:
                state_data = response.json()
                
                # Check for missed messages
                new_counter = state_data.get('message_counter', 0)
                if self.last_state_counter > 0:
                    expected = (self.last_state_counter + 1) % 65536
                    if new_counter != expected:
                        self.logger.warning(
                            f"Missed state message(s). Expected {expected}, got {new_counter}"
                        )
                self.last_state_counter = new_counter
                
                self.state_updated.emit(state_data)
                return state_data
        except requests.RequestException as e:
            self.handle_connection_error(f"Failed to fetch state: {e}")
        return None

    def fetch_fault_status(self):
        """Fetch fault status information"""
        try:
            response = self.session.get(
                f"{self.base_url}{API_ENDPOINTS['fault_status']}",
                timeout=0.5
            )
            if response.status_code == 200:
                fault_data = response.json()
                self.fault_updated.emit(fault_data)
                return fault_data
        except requests.RequestException as e:
            self.handle_connection_error(f"Failed to fetch fault status: {e}")
        return None

    def fetch_powertrain_metrics(self):
        """Fetch powertrain-specific metrics"""
        try:
            response = self.session.get(
                f"{self.base_url}{API_ENDPOINTS['metrics']['powertrain']}",
                timeout=0.5
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch powertrain metrics: {e}")
        return None

    def fetch_tire_metrics(self):
        """Fetch tire-specific metrics"""
        try:
            response = self.session.get(
                f"{self.base_url}{API_ENDPOINTS['metrics']['tires']}",
                timeout=0.5
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch tire metrics: {e}")
        return None

    def handle_connection_error(self, error_msg):
        """Handle connection errors and update status"""
        self.logger.error(error_msg)
        if self.connected:
            self.connected = False
            self.connection_status_changed.emit(False)

    def start_monitoring(self):
        """Start all update timers"""
        self.state_timer.start()
        self.fault_timer.start()
        self.metrics_timer.start()

    def stop_monitoring(self):
        """Stop all update timers"""
        self.state_timer.stop()
        self.fault_timer.stop()
        self.metrics_timer.stop()

    def set_update_interval(self, data_type, interval):
        """Update the refresh interval for a specific data type"""
        if data_type == "vehicle_state":
            self.state_timer.setInterval(interval)
        elif data_type == "fault_status":
            self.fault_timer.setInterval(interval)
        elif data_type == "metrics":
            self.metrics_timer.setInterval(interval)