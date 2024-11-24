from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QGridLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QMimeData
from PyQt6.QtGui import QDrag
from ..utils.data_service import DataService

class DraggableWidget(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setText(text)
        self.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid black;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_start_position = None
        
        if text == "Settings":
            self.data_service = DataService()
            self.setup_data_display()
            
    def setup_data_display(self):
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)  # Set spacing to 0
        self.layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
        self.data_labels = {}
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(1000)

    def update_data(self):
        data = self.data_service.fetch_vehicle_data()
        if data:
            self.setText("")
            row = 0
            for key, value in data.items():
                if key not in self.data_labels:
                    label = QLabel(f"{key}: {value}")
                    label.setStyleSheet("border: none; padding: 2px;")  # Remove border, add minimal padding
                    self.data_labels[key] = label
                    self.layout.addWidget(label, row, 0)
                else:
                    self.data_labels[key].setText(f"{key}: {value}")
                row += 1

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() <= self.height() * 0.15:
                self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if not self.drag_start_position:
            return
        
        distance = (event.position().toPoint() - self.drag_start_position).manhattanLength()
        if distance < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)
        drag.exec(Qt.DropAction.MoveAction)
        self.drag_start_position = None