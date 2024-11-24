from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QApplication
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt

from ..components.draggable_button import DraggableButton
from ..components.drop_area import DropArea
from ..utils.image_utils import create_blurred_background


class MainDash(QMainWindow):
    def __init__(self):
        super().__init__()
        
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        target_width = screen_width
        target_height = int(target_width * 9 / 16)
        if target_height > screen_height:
            target_height = screen_height
            target_width = int(target_height * 16 / 9)

        self.setWindowTitle("Infotainment Dashboard - Home Screen")
        self.setGeometry(100, 100, target_width, target_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Store the background image path
        self.background_image_path = "/home/mkulick/Documents/infotainment_dashboard/assets/modern_sports_car_offcenter_right.jpg"
        
        # Load and store both normal and blurred backgrounds
        self.normal_background = QPixmap(self.background_image_path)
        self.blurred_background = create_blurred_background(self.background_image_path)
        
        # Set initial background
        self.set_background(self.normal_background)

        # Display Area
        self.display_area = DropArea()
        self.main_layout.addWidget(self.display_area)

        # Bottom Bar
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet("""
            QFrame {
                background-color: rgba(51, 51, 51, 0.9);
                border-top: 1px solid #666;
            }
        """)
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(15, 5, 15, 5)
        self.bottom_layout.setSpacing(15)
        
        bottom_bar_height = int(target_height / 8)
        self.bottom_bar.setFixedHeight(bottom_bar_height)

        self.app_names = [
            "Navigation",
            "Music",
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

    def set_background(self, pixmap):
        scaled_background = pixmap.scaled(
            self.width(),
            self.height(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding
        )
        palette = self.central_widget.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_background))
        self.central_widget.setPalette(palette)
        self.central_widget.setAutoFillBackground(True)

    def set_blurred_background(self):
        self.set_background(self.blurred_background)

    def restore_background(self):
        self.set_background(self.normal_background)