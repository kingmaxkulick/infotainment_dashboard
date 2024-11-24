from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QDrag
from PyQt6.QtCore import Qt, QMimeData, QTimer, QSize


class DraggableButton(QPushButton):
    def __init__(self, text, icon_name=""):
        super().__init__(text)
        self._drag_cooldown = False
        self._cooldown_timer = QTimer(self)
        self._cooldown_timer.timeout.connect(self._reset_cooldown)
        self._cooldown_timer.setSingleShot(True)
        
        # Set fixed size for smaller buttons
        self.setFixedSize(60, 60)
        
        # Style the button to look more app-like
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #999;
                border-radius: 8px;
                font-weight: bold;
                padding: 4px;
                text-align: center;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 1.0);
                border: 1px solid #666;
            }
        """)

    def sizeHint(self):
        return QSize(60, 60)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self._drag_cooldown:
            self._drag_cooldown = True
            self._cooldown_timer.start(100)
            
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)

    def _reset_cooldown(self):
        self._drag_cooldown = False