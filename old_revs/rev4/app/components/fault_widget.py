"""
Widget for displaying vehicle fault information
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from ..utils.constants import COLORS, STYLES

class FaultWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet(STYLES["fault_widget"])
        layout = QVBoxLayout(self)
        
        # Header
        self.header_label = QLabel("System Status")
        self.header_label.setObjectName("fault_header")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Fault status
        self.fault_status = QLabel("✓ System Normal")
        self.fault_status.setObjectName("fault_active")
        self.fault_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);")
        
        # Fault details
        self.source_label = QLabel("Source: --")
        self.type_label = QLabel("Type: --")
        self.severity_label = QLabel("Severity: --")
        self.time_label = QLabel("Time: --")
        
        # Add everything to layout
        layout.addWidget(self.header_label)
        layout.addWidget(self.fault_status)
        layout.addWidget(divider)
        layout.addWidget(self.source_label)
        layout.addWidget(self.type_label)
        layout.addWidget(self.severity_label)
        layout.addWidget(self.time_label)
        
        self.setMinimumSize(200, 200)
        
    def update_fault_status(self, fault_data):
        """Update the fault display with new data"""
        if not fault_data:
            return
            
        fault_active = fault_data.get("active", False)
        
        if fault_active:
            self.fault_status.setText("⚠️ FAULT ACTIVE")
            self.fault_status.setStyleSheet(f"color: {COLORS['FAULT_ACTIVE']}; font-weight: bold;")
            
            # Update fault details
            source = fault_data.get("source", "UNKNOWN")
            fault_type = fault_data.get("type", "UNKNOWN")
            severity = fault_data.get("severity", 0)
            
            self.source_label.setText(f"Source: {source}")
            self.type_label.setText(f"Type: {fault_type}")
            self.severity_label.setText(f"Severity: {severity}")
            
            # Format timestamp
            timestamp = fault_data.get("timestamp", 0)
            time_str = f"Time: {timestamp/1000:.1f}s ago"
            self.time_label.setText(time_str)
            
            # Style based on severity
            if severity > 1:
                self.setStyleSheet(STYLES["fault_widget"] + f"""
                    QWidget {{
                        background-color: rgba(244, 67, 54, 0.1);
                    }}
                """)
        else:
            self.fault_status.setText("✓ System Normal")
            self.fault_status.setStyleSheet(f"color: {COLORS['FAULT_CLEARED']}; font-weight: bold;")
            self.source_label.setText("Source: --")
            self.type_label.setText("Type: --")
            self.severity_label.setText("Severity: --")
            self.time_label.setText("Time: --")
            self.setStyleSheet(STYLES["fault_widget"])