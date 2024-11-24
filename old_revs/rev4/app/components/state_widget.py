"""
Widget for displaying vehicle state information
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from ..utils.constants import COLORS, STYLES

class StateWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet(STYLES["state_widget"])
        layout = QVBoxLayout(self)
        
        # Create labels
        self.state_label = QLabel("PARK")
        self.state_label.setObjectName("state_label")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.substate_label = QLabel("READY")
        self.substate_label.setObjectName("substate_label")
        self.substate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Status flags grid
        self.flags_widget = QWidget()
        self.flags_layout = QGridLayout(self.flags_widget)
        self.status_labels = {}
        
        # Add to main layout
        layout.addWidget(self.state_label)
        layout.addWidget(self.substate_label)
        layout.addWidget(self.flags_widget)
        
        self.setMinimumSize(200, 150)
        
    def update_state(self, state_data):
        """Update the state display with new data"""
        if not state_data:
            return
            
        # Update primary state
        primary_state = state_data.get("primary_state", "UNKNOWN")
        self.state_label.setText(primary_state)
        self.state_label.setStyleSheet(f"color: {COLORS.get(primary_state, COLORS['TEXT'])}")
        
        # Update substate
        substate = state_data.get("sub_state", "UNKNOWN")
        self.substate_label.setText(substate)
        
        # Update status flags
        flags = state_data.get("status_flags", [])
        
        # Clear existing flags
        for label in self.status_labels.values():
            label.setParent(None)
        self.status_labels.clear()
        
        # Add new flags
        for i, flag in enumerate(flags):
            label = QLabel(flag.replace("_", " "))
            label.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 4px; padding: 2px;")
            self.flags_layout.addWidget(label, i // 2, i % 2)
            self.status_labels[flag] = label