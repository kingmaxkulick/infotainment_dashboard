"""
Main dashboard window for the infotainment system
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QFrame, QApplication, QLabel
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer

from ..components.draggable_button import DraggableButton
from ..components.drop_area import DropArea
from ..components.state_widget import StateWidget
from ..components.fault_widget import FaultWidget
from ..utils.image_utils import create_blurred_background
from ..utils.constants import COLORS, STYLES
from ..services.data_service import DataService

class MainDash(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_data_service()
        
    def setup_ui(self):
        """Initialize the UI"""
        # Get screen dimensions
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate window size (16:9 aspect ratio)
        target_width = screen_width
        target_height = int(target_width * 9 / 16)
        if target_height > screen_height:
            target_height = screen_height
            target_width = int(target_height * 16 / 9)

        # Set window properties
        self.setWindowTitle("Vehicle Infotainment System")
        self.setGeometry(100, 100, target_width, target_height)
        self.setStyleSheet(STYLES["main_window"])

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Load background
        self.background_image_path = "assets/modern_sports_car_offcenter_right.jpg"
        self.normal_background = QPixmap(self.background_image_path)
        self.blurred_background = create_blurred_background(self.background_image_path)
        self.set_background(self.normal_background)

        # Status bar for connection status
        self.status_label = QLabel()
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.7);
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        self.main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignRight)
        self.status_label.hide()

        # Display Area
        self.display_area = DropArea()
        self.main_layout.addWidget(self.display_area)

        # Bottom Bar
        self.setup_bottom_bar(target_height)

        # Initialize widgets dictionary
        self.active_widgets = {}

    def setup_bottom_bar(self, window_height):
        """Setup the bottom app bar"""
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['BACKGROUND']};
                border-top: 1px solid {COLORS['BORDER']};
            }}
        """)
        
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(15, 5, 15, 5)
        self.bottom_layout.setSpacing(15)
        
        bottom_bar_height = int(window_height / 8)
        self.bottom_bar.setFixedHeight(bottom_bar_height)

        # App buttons
        self.app_names = [
            "Navigation",
            "Media",
            "Climate",
            "Phone",
            "Vehicle Info",
            "Settings"
        ]

        self.bottom_layout.addStretch()
        self.buttons = [DraggableButton(name) for name in self.app_names]
        for button in self.buttons:
            self.bottom_layout.addWidget(button)
        self.bottom_layout.addStretch()

        self.main_layout.addWidget(self.bottom_bar)

    def setup_data_service(self):
        """Initialize and connect the data service"""
        self.data_service = DataService()
        
        # Connect signals
        self.data_service.data_updated.connect(self.update_vehicle_data)
        self.data_service.state_updated.connect(self.update_vehicle_state)
        self.data_service.fault_updated.connect(self.update_fault_status)
        self.data_service.connection_status_changed.connect(self.update_connection_status)
        
        # Start monitoring
        self.data_service.start_monitoring()

    def update_vehicle_data(self, data):
        """Update all vehicle-related widgets with new data"""
        if "Vehicle Info" in self.display_area.widgets:
            for widget in self.display_area.widgets:
                if hasattr(widget, 'update_data'):
                    widget.update_data(data)

    def update_vehicle_state(self, state_data):
        """Update state-specific widgets"""
        for widget in self.display_area.widgets:
            if hasattr(widget, 'state_widget'):
                widget.state_widget.update_state(state_data)

    def update_fault_status(self, fault_data):
        """Update fault-specific widgets"""
        for widget in self.display_area.widgets:
            if hasattr(widget, 'fault_widget'):
                widget.fault_widget.update_fault_status(fault_data)

    def update_connection_status(self, connected):
        """Update the connection status display"""
        if connected:
            self.status_label.setText("✓ Connected")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(0, 150, 0, 0.7);
                    color: white;
                    padding: 5px;
                    border-radius: 3px;
                }
            """)
            # Hide after 3 seconds if connected
            QTimer.singleShot(3000, self.status_label.hide)
        else:
            self.status_label.setText("⚠ Connection Lost")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(200, 0, 0, 0.7);
                    color: white;
                    padding: 5px;
                    border-radius: 3px;
                }
            """)
            self.status_label.show()

    def set_background(self, pixmap):
        """Set the window background"""
        scaled_background = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        palette = self.central_widget.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_background))
        self.central_widget.setPalette(palette)
        self.central_widget.setAutoFillBackground(True)

    def set_blurred_background(self):
        """Set blurred background when widgets are present"""
        self.set_background(self.blurred_background)

    def restore_background(self):
        """Restore normal background when no widgets are present"""
        self.set_background(self.normal_background)

    def closeEvent(self, event):
        """Clean up when closing"""
        self.data_service.stop_monitoring()
        super().closeEvent(event)