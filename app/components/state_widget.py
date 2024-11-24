"""
Widget for displaying vehicle state information including primary state, substate, and status flags
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from ..utils.constants import COLORS, STYLES

class StateWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the state widget UI"""
        self.setStyleSheet(STYLES["state_widget"])
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Primary state label (PARK, DRIVE, etc.)
        self.state_label = QLabel("PARK")
        self.state_label.setObjectName("state_label")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {COLORS['PARK']};
                padding: 5px;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.05);
            }}
        """)
        
        # Substate label (READY, ACTIVE, etc.)
        self.substate_label = QLabel("READY")
        self.substate_label.setObjectName("substate_label")
        self.substate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.substate_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666;
                padding: 3px;
            }
        """)
        
        # Status flags grid
        self.flags_widget = QWidget()
        self.flags_layout = QGridLayout(self.flags_widget)
        self.flags_layout.setSpacing(5)
        self.status_labels = {}
        
        # Add everything to main layout
        layout.addWidget(self.state_label)
        layout.addWidget(self.substate_label)
        layout.addWidget(self.flags_widget)
        
        # Set minimum size
        self.setMinimumSize(200, 150)
        
    def update_state(self, state_data):
        """Update the state display with new data"""
        if not state_data:
            return
            
        # Update primary state with color coding
        primary_state = state_data.get("primary_state", "UNKNOWN")
        self.state_label.setText(primary_state)
        self.state_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {COLORS.get(primary_state, COLORS['TEXT'])};
                padding: 5px;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 0.05);
            }}
        """)
        
        # Update substate
        substate = state_data.get("sub_state", "UNKNOWN")
        self.substate_label.setText(substate)
        
        # Update status flags
        flags = state_data.get("status_flags", [])
        
        # Clear existing flags
        for label in self.status_labels.values():
            label.setParent(None)
        self.status_labels.clear()
        
        # Add new flags in a grid layout
        for i, flag in enumerate(flags):
            label = QLabel(flag.replace("_", " "))
            label.setStyleSheet("""
                QLabel {
                    background-color: rgba(0, 0, 0, 0.1);
                    color: #333;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 11px;
                }
            """)
            
            # Special styling for certain flags
            if flag == "MOTOR_READY":
                label.setStyleSheet("""
                    QLabel {
                        background-color: rgba(76, 175, 80, 0.2);
                        color: #2E7D32;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-size: 11px;
                    }
                """)
            elif flag == "BATTERY_OK":
                label.setStyleSheet("""
                    QLabel {
                        background-color: rgba(33, 150, 243, 0.2);
                        color: #1565C0;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-size: 11px;
                    }
                """)
            elif flag == "CHARGING_CONNECTED":
                label.setStyleSheet("""
                    QLabel {
                        background-color: rgba(156, 39, 176, 0.2);
                        color: #7B1FA2;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-size: 11px;
                    }
                """)
            
            # Add to grid layout (2 columns)
            row = i // 2
            col = i % 2
            self.flags_layout.addWidget(label, row, col)
            self.status_labels[flag] = label

    def showEvent(self, event):
        """Handle widget show event"""
        super().showEvent(event)
        self.adjustSize()
        
    def sizeHint(self):
        """Provide size hint for layout management"""
        return self.minimumSize()
        
    def minimumSizeHint(self):
        """Provide minimum size hint"""
        return self.minimumSize()