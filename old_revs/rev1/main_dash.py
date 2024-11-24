import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QGridLayout, QWidget
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QDrag
from PyQt6.QtCore import Qt, QMimeData


class DraggableButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)


class DropArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.widgets = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            widget_text = event.mimeData().text()
            drop_position = event.position().toPoint()  # Convert to QPoint
            if drop_position.y() > self.height() * 0.8:  # Dragged down near the bottom
                self.remove_widget(widget_text)
            else:
                self.add_widget(widget_text)
            event.acceptProposedAction()

    def add_widget(self, widget_text):
        if len(self.widgets) >= 3:
            return  # Max 3 widgets on display
        widget = QLabel(widget_text)
        widget.setStyleSheet("background-color: white; border: 1px solid black; font-weight: bold;")
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgets.append(widget)
        self.rearrange_widgets()

    def remove_widget(self, widget_text):
        for widget in self.widgets:
            if widget.text() == widget_text:
                self.widgets.remove(widget)
                widget.setParent(None)
                self.rearrange_widgets()
                break

    def rearrange_widgets(self):
        # Clear the current layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        if len(self.widgets) == 1:
            self.layout.addWidget(self.widgets[0], 0, 1)  # Center
        elif len(self.widgets) == 2:
            self.layout.addWidget(self.widgets[0], 0, 0)  # Left
            self.layout.addWidget(self.widgets[1], 0, 2)  # Right
        elif len(self.widgets) == 3:
            self.layout.addWidget(self.widgets[0], 0, 0)  # Left
            self.layout.addWidget(self.widgets[1], 0, 1)  # Center
            self.layout.addWidget(self.widgets[2], 0, 2)  # Right


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

        # Display Area (with Drop Functionality)
        self.display_area = DropArea()
        self.main_layout.addWidget(self.display_area)

        # Bottom Bar
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet("background-color: #333333;")
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(5, 5, 5, 5)

        # Set the fixed height to 1/8 of the window height
        bottom_bar_height = int(target_height / 8)
        self.bottom_bar.setFixedHeight(bottom_bar_height)

        # Bottom Bar Buttons with Drag Functionality
        self.buttons = [DraggableButton(f"Widget {i + 1}") for i in range(6)]
        for button in self.buttons:
            button.setStyleSheet(
                "background-color: white; border: 1px solid black; font-weight: bold;"
            )
            self.bottom_layout.addWidget(button)

        # Add bottom bar to main layout
        self.main_layout.addWidget(self.bottom_bar)

    def set_background_image(self, image_path):
        # Load the background image
        background = QPixmap(image_path)

        # Scale the image to fit the screen
        scaled_background = background.scaled(
            self.width(),
            self.height(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding
        )

        # Set the scaled background
        palette = self.central_widget.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_background))
        self.central_widget.setPalette(palette)
        self.central_widget.setAutoFillBackground(True)


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dash = MainDash()
    main_dash.show()
    sys.exit(app.exec())
