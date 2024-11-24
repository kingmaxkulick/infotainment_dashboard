import sys
import requests
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow, QGridLayout
from PyQt6.QtCore import QTimer

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Infotainment Dashboard")
        self.setGeometry(100, 100, 800, 480)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a grid layout for better organization
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # Add labels for metrics
        self.labels = {
            "charge_percent": QLabel("Charge Percentage: "),
            "charging_rate": QLabel("Charging Rate: "),
            "full_charge_time": QLabel("Full Charge Time: "),
            "battery_temp": QLabel("Battery Temperature: "),
            "motor_temp": QLabel("Motor Temperature: "),
            "inverter_temp": QLabel("Inverter Temperature: "),
            "tire_pressure": QLabel("Tire Pressure: "),
            "tire_temp": QLabel("Tire Temperature: "),
            "power_output": QLabel("Power Output: "),
            "torque_distribution": QLabel("Torque Distribution: "),
            "suspension_metrics": QLabel("Suspension Metrics: "),
            "g_forces": QLabel("G-Forces: "),
            "brake_temp": QLabel("Brake Temperature: ")
        }

        # Add all labels to the grid layout
        row = 0
        for key, label in self.labels.items():
            self.layout.addWidget(label, row, 0)
            row += 1

        # Set up periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every 1 second

    def update_data(self):
        try:
            # Fetch data from backend
            response = requests.get("http://192.168.5.172:8000/vehicle_data")
            data = response.json()

            # Update each label with the fetched data
            self.labels["charge_percent"].setText(f"Charge Percentage: {data['charge_percent']}%")
            self.labels["charging_rate"].setText(f"Charging Rate: {data['charging_rate']} kW")
            self.labels["full_charge_time"].setText(f"Full Charge Time: {data['full_charge_time']} min")
            self.labels["battery_temp"].setText(f"Battery Temp: {data['battery_temp']} °C")
            self.labels["motor_temp"].setText(f"Motor Temp: {data['motor_temp']} °C")
            self.labels["inverter_temp"].setText(f"Inverter Temp: {data['inverter_temp']} °C")
            self.labels["tire_pressure"].setText(f"Tire Pressure: {data['tire_pressure']}")
            self.labels["tire_temp"].setText(f"Tire Temp: {data['tire_temp']}")
            self.labels["power_output"].setText(f"Power Output: {data['power_output']} W")
            self.labels["torque_distribution"].setText(f"Torque: {data['torque_distribution']}")
            self.labels["suspension_metrics"].setText(f"Suspension: {data['suspension_metrics']}")
            self.labels["g_forces"].setText(f"G-Forces: {data['g_forces']}")
            self.labels["brake_temp"].setText(f"Brake Temp: {data['brake_temp']} °C")

        except requests.RequestException as e:
            print(f"Failed to fetch data: {e}")

# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())
