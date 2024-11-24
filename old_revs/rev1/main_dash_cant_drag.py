import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QGridLayout, QWidget
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt


class MainDash(QMainWindow):
    def __init__(self):
        super().__init__()

        # Dynamically set the window size based on screen size
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Maintain 16:9 aspect ratio
        target_width = screen_width
        target_height = int(target_width * 9 / 16)
        if target_height > screen_height:  # If it overflows, adjust
            target_height = screen_height
            target_width = int(target_height * 16 / 9)

        self.setWindowTitle("Infotainment Dashboard - Home Screen")
        self.setGeometry(100, 100, target_width, target_height)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Set Background Image
        self.set_background_image("/home/mkulick/Documents/modern_sports_car_offcenter_right.jpg")

        # Display Area (Initially blank)
        self.display_area = QFrame()
        self.display_area.setStyleSheet("background-color: transparent; border: none;")
        self.display_layout = QGridLayout(self.display_area)
        self.display_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.display_area)

        # Placeholder Widgets for Main Sections
        self.sections = [QLabel(f"Section {i + 1}", self) for i in range(3)]
        for label in self.sections:
            label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Bottom Bar
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet("background-color: #333333;")
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(5, 5, 5, 5)

        # Set the fixed height to 1/4 of the original height
        bottom_bar_height = int(self.height() / 10)  # Adjust as needed (1/10th of screen height for this example)
        self.bottom_bar.setFixedHeight(bottom_bar_height)

        # Bottom Bar Buttons
        self.buttons = [QPushButton(str(i + 1)) for i in range(6)]
        for button in self.buttons:
            button.setStyleSheet(
                "background-color: white; border: 1px solid black; font-weight: bold;"
            )
            self.bottom_layout.addWidget(button)

        # Add bottom bar to main layout
        self.main_layout.addWidget(self.bottom_bar)


        # Add buttons for drag-and-drop functionality
        self.setup_drag_and_drop()

    def set_background_image(self, image_path):
        # Load the background image
        background = QPixmap(image_path)

        # Scale the image to fit the screen
        scaled_background = background.scaled(
            self.width(),  # Use the width of the window
            self.height(),  # Use the height of the window
            Qt.AspectRatioMode.KeepAspectRatioByExpanding  # Ensures the image covers the screen
        )

        # Set the scaled background
        palette = self.central_widget.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_background))
        self.central_widget.setPalette(palette)
        self.central_widget.setAutoFillBackground(True)

    def setup_drag_and_drop(self):
        # Add a placeholder for dragging widgets from the bottom bar
        for i, button in enumerate(self.buttons):
            button.setCheckable(True)
            button.clicked.connect(lambda checked, b=button, idx=i: self.select_widget(b, idx))

    def select_widget(self, button, index):
        if button.isChecked():
            button.setStyleSheet("background-color: lightblue; font-weight: bold;")
            # Placeholder logic for dragging widget
            print(f"Widget {index + 1} selected for dragging.")
        else:
            button.setStyleSheet("background-color: white; font-weight: bold;")
            print(f"Widget {index + 1} deselected.")

        # Add logic for dragging widget to sections

    def set_display_mode(self, mode):
        # Single widget
        if mode == 1:
            self.display_layout.addWidget(self.sections[0], 0, 0, 1, 3)
        # Split into 2 sections
        elif mode == 2:
            self.display_layout.addWidget(self.sections[0], 0, 0, 1, 1)
            self.display_layout.addWidget(self.sections[1], 0, 1, 1, 2)
        # Split into 3 sections
        elif mode == 3:
            self.display_layout.addWidget(self.sections[0], 0, 0, 1, 1)
            self.display_layout.addWidget(self.sections[1], 0, 1, 1, 1)
            self.display_layout.addWidget(self.sections[2], 0, 2, 1, 1)


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dash = MainDash()
    main_dash.show()
    sys.exit(app.exec())
