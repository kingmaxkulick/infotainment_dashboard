"""
Popup window for displaying charging status when vehicle is in charging state
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QProgressBar, QPushButton, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from ..utils.constants import COLORS, STYLES

class ChargingPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the UI components"""
        # Set window flags for popup behavior
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main container with styling
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
            QLabel {
                color: white;
            }
        """)
        container_layout = QVBoxLayout(self.container)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Charging Status")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)
        
        # Close button
        self.close_button = QPushButton("×")
        self.close_button.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                font-size: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        self.close_button.clicked.connect(self.hide)
        header_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)
        container_layout.addLayout(header_layout)
        
        # Charge percentage
        self.percentage_label = QLabel("67%")
        self.percentage_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.percentage_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #2196F3;
                border-radius: 5px;
                text-align: center;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        container_layout.addWidget(self.progress_bar)
        
        # Charging info
        info_layout = QGridLayout()
        
        # Time remaining
        self.time_label = QLabel("Time Remaining:")
        self.time_value = QLabel("2h 15m")
        info_layout.addWidget(self.time_label, 0, 0)
        info_layout.addWidget(self.time_value, 0, 1)
        
        # Power
        self.power_label = QLabel("Charging Power:")
        self.power_value = QLabel("7.2 kW")
        info_layout.addWidget(self.power_label, 1, 0)
        info_layout.addWidget(self.power_value, 1, 1)
        
        # Range
        self.range_label = QLabel("Est. Range:")
        self.range_value = QLabel("285 mi")
        info_layout.addWidget(self.range_label, 2, 0)
        info_layout.addWidget(self.range_value, 2, 1)
        
        # Battery temp
        self.temp_label = QLabel("Battery Temp:")
        self.temp_value = QLabel("25°C")
        info_layout.addWidget(self.temp_label, 3, 0)
        info_layout.addWidget(self.temp_value, 3, 1)
        
        container_layout.addLayout(info_layout)
        main_layout.addWidget(self.container)
        
        # Set fixed size
        self.setFixedSize(300, 400)
        
    def update_data(self, data):
        """Update the charging display with new data"""
        if not data:
            return
            
        # Update charge percentage
        charge_percent = data.get("charge_percent", 0)
        self.percentage_label.setText(f"{charge_percent}%")
        self.progress_bar.setValue(charge_percent)
        
        # Update power
        power = data.get("charging_rate", 0)
        self.power_value.setText(f"{power} kW")
        
        # Update battery temp
        temp = data.get("battery_temp", 0)
        self.temp_value.setText(f"{temp}°C")
        
        # Update range (estimated based on charge percentage)
        max_range = 350  # Maximum range in miles
        est_range = int(max_range * charge_percent / 100)
        self.range_value.setText(f"{est_range} mi")
        
        # Update time remaining (estimated)
        if power > 0:
            remaining_charge = 100 - charge_percent
            hours_remaining = remaining_charge / (power * 100 / max_range)
            hours = int(hours_remaining)
            minutes = int((hours_remaining - hours) * 60)
            self.time_value.setText(f"{hours}h {minutes}m")
        else:
            self.time_value.setText("--")
            
    def show(self):
        """Show popup in the parent's center"""
        if self.parent():
            parent_rect = self.parent().geometry()
            x = parent_rect.center().x() - self.width() // 2
            y = parent_rect.center().y() - self.height() // 2
            self.move(x, y)
        super().show()