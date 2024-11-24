from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDrag
from ..utils.data_service import DataService
from PyQt6.QtCore import Qt, QMimeData

class VehicleWidget(QWidget):
    def __init__(self, widget_type, parent=None):
        super().__init__(parent)
        self.widget_type = widget_type
        self.data_service = DataService()
        self.drag_start_position = None
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QGridLayout(self)
        self.labels = {}
        
        metrics = [
            "charge_percent", "charging_rate", "full_charge_time",
            "battery_temp", "motor_temp", "inverter_temp",
            "tire_pressure", "tire_temp", "power_output",
            "torque_distribution", "suspension_metrics",
            "g_forces", "brake_temp"
        ]
        
        for i, metric in enumerate(metrics):
            label = QLabel(f"{metric.replace('_', ' ').title()}: --")
            self.labels[metric] = label
            self.layout.addWidget(label, i // 2, i % 2)
        
        self.setMinimumSize(300, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                font-size: 12px;
                color: black;
            }
        """)

    def update_data(self, vehicle_data):
        units = {
            "charge_percent": "%",
            "charging_rate": "kW",
            "full_charge_time": "min",
            "battery_temp": "°C",
            "motor_temp": "°C",
            "inverter_temp": "°C",
            "power_output": "W",
            "brake_temp": "°C"
        }
        
        for metric, label in self.labels.items():
            if metric in vehicle_data:
                data = vehicle_data[metric]
                unit = units.get(metric, "")
                if isinstance(data, list):
                    label.setText(f"{metric.replace('_', ' ').title()}: {data}")
                else:
                    label.setText(f"{metric.replace('_', ' ').title()}: {data}{unit}")

    def text(self):
        return self.widget_type

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() <= self.height() * 0.2:
                self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton) or not self.drag_start_position:
            return

        if (event.position().y() - self.drag_start_position.y()) > 10:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.widget_type)
            mime_data.setProperty("removal_drag", True)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)