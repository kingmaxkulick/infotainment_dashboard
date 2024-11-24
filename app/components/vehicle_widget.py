"""
Main vehicle data display widget with integrated state and fault monitoring
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGridLayout, QFrame
)
from PyQt6.QtCore import Qt
from ..utils.constants import COLORS, STYLES
from .state_widget import StateWidget
from .fault_widget import FaultWidget

class VehicleWidget(QWidget):
    def __init__(self, widget_type="Vehicle Info", parent=None):
        super().__init__(parent)
        self.widget_type = widget_type
        self.drag_start_position = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the vehicle widget UI"""
        self.setStyleSheet(STYLES["vehicle_widget"])
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        # Header
        header = QLabel("Vehicle Information")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Horizontal layout for state and fault widgets
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)
        
        # Add state widget
        self.state_widget = StateWidget()
        status_layout.addWidget(self.state_widget)
        
        # Vertical divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);")
        status_layout.addWidget(divider)
        
        # Add fault widget
        self.fault_widget = FaultWidget()
        status_layout.addWidget(self.fault_widget)
        
        main_layout.addLayout(status_layout)
        
        # Horizontal divider
        h_divider = QFrame()
        h_divider.setFrameShape(QFrame.Shape.HLine)
        h_divider.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);")
        main_layout.addWidget(h_divider)
        
        # Metrics grid
        metrics_widget = QWidget()
        self.metrics_layout = QGridLayout(metrics_widget)
        self.metrics_layout.setSpacing(8)
        self.metric_labels = {}
        
        # Create metric sections
        self.setup_metric_section("Powertrain", [
            ("charge_percent", "Battery", "%"),
            ("power_output", "Power", "kW"),
            ("motor_temp", "Motor", "°C"),
            ("battery_temp", "Battery", "°C")
        ], 0)
        
        # Add spacing between sections
        spacer = QLabel()
        spacer.setFixedHeight(10)
        self.metrics_layout.addWidget(spacer, 5, 0)
        
        self.setup_metric_section("Tires", [
            ("tire_temp", "Temperature", "°C"),
            ("tire_pressure", "Pressure", "PSI")
        ], 6)
        
        main_layout.addWidget(metrics_widget)
        
        # Set minimum size
        self.setMinimumSize(500, 400)

    def setup_metric_section(self, title, metrics, row_offset):
        """Create a section of metrics with a title"""
        # Section title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 14px;
            color: #333;
            padding-top: 5px;
            padding-bottom: 5px;
        """)
        self.metrics_layout.addWidget(title_label, row_offset, 0, 1, 2)
        
        # Add metrics
        for i, (key, name, unit) in enumerate(metrics):
            # Create wrapper widget for consistent styling
            wrapper = QWidget()
            wrapper_layout = QHBoxLayout(wrapper)
            wrapper_layout.setContentsMargins(5, 2, 5, 2)
            
            # Create the label with the metric name and initial value
            label = QLabel(f"{name}: --{unit}")
            label.setStyleSheet("""
                padding: 3px;
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 4px;
            """)
            wrapper_layout.addWidget(label)
            
            self.metric_labels[key] = label
            self.metrics_layout.addWidget(wrapper, row_offset + i + 1, 0)

    def update_data(self, data):
        """Update all vehicle data displays"""
        if not data:
            return
            
        # Update state information
        if "vehicle_state" in data:
            self.state_widget.update_state(data["vehicle_state"])
            
        # Update fault information
        if "fault_status" in data:
            self.fault_widget.update_fault_status(data["fault_status"])
            
        # Update simple metrics
        simple_metrics = {
            "charge_percent": ("Battery", "%"),
            "power_output": ("Power", "kW"),
            "motor_temp": ("Motor", "°C"),
            "battery_temp": ("Battery", "°C")
        }
        
        for key, (name, unit) in simple_metrics.items():
            if key in data and key in self.metric_labels:
                value = data[key]
                self.metric_labels[key].setText(f"{name}: {value}{unit}")
                
                # Apply color coding based on thresholds
                if key in ["motor_temp", "battery_temp"]:
                    self.color_code_temperature(key, value)
                elif key == "charge_percent":
                    self.color_code_charge(value)
        
        # Update tire data with array formatting
        if "tire_temp" in data:
            temps = data["tire_temp"]
            temp_str = " / ".join(f"{t}" for t in temps)
            self.metric_labels["tire_temp"].setText(f"Temperature: {temp_str}°C")
            self.color_code_temperature("tire_temp", max(temps))
            
        if "tire_pressure" in data:
            pressures = data["tire_pressure"]
            pressure_str = " / ".join(f"{p}" for p in pressures)
            self.metric_labels["tire_pressure"].setText(f"Pressure: {pressure_str} PSI")
            self.color_code_pressure(max(pressures))

    def color_code_temperature(self, key, value):
        """Color code temperature values"""
        if value >= 80:
            color = COLORS["CRITICAL"]
            bg_color = "rgba(244, 67, 54, 0.1)"
        elif value >= 70:
            color = COLORS["WARNING"]
            bg_color = "rgba(255, 152, 0, 0.1)"
        else:
            color = COLORS["NORMAL"]
            bg_color = "rgba(76, 175, 80, 0.1)"
            
        self.metric_labels[key].setStyleSheet(f"""
            color: {color};
            padding: 3px;
            background-color: {bg_color};
            border-radius: 4px;
        """)

    def color_code_pressure(self, value):
        """Color code tire pressure values"""
        if value >= 38 or value <= 28:
            color = COLORS["CRITICAL"]
            bg_color = "rgba(244, 67, 54, 0.1)"
        elif value >= 35 or value <= 30:
            color = COLORS["WARNING"]
            bg_color = "rgba(255, 152, 0, 0.1)"
        else:
            color = COLORS["NORMAL"]
            bg_color = "rgba(76, 175, 80, 0.1)"
            
        self.metric_labels["tire_pressure"].setStyleSheet(f"""
            color: {color};
            padding: 3px;
            background-color: {bg_color};
            border-radius: 4px;
        """)

    def color_code_charge(self, value):
        """Color code battery charge values"""
        if value <= 20:
            color = COLORS["CRITICAL"]
            bg_color = "rgba(244, 67, 54, 0.1)"
        elif value <= 30:
            color = COLORS["WARNING"]
            bg_color = "rgba(255, 152, 0, 0.1)"
        else:
            color = COLORS["NORMAL"]
            bg_color = "rgba(76, 175, 80, 0.1)"
            
        self.metric_labels["charge_percent"].setStyleSheet(f"""
            color: {color};
            padding: 3px;
            background-color: {bg_color};
            border-radius: 4px;
        """)

    def text(self):
        """Return widget type for drag and drop compatibility"""
        return self.widget_type