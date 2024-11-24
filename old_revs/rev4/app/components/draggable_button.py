"""
Draggable app launcher button
"""
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QDrag
from PyQt6.QtCore import Qt, QMimeData, QTimer, QSize
from ..utils.constants import COLORS

class DraggableButton(QPushButton):
    def __init__(self, text, icon_name=""):
        super().__init__(text)
        self._drag_cooldown = False
        self._cooldown_timer = QTimer(self)
        self._cooldown_timer.timeout.connect(self._reset_cooldown)
        self._cooldown_timer.setSingleShot(True)
        
        # Set fixed size for app icons
        self.setFixedSize(70, 70)
        
        # Enhanced styling
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid {COLORS['BORDER']};
                border-radius: 10px;
                font-weight: bold;
                padding: 4px;
                text-align: center;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 1.0);
                border: 1px solid rgba(255, 255, 255, 1.0);
            }}
            QPushButton:pressed {{
                background-color: rgba(200, 200, 200, 0.9);
            }}
        """)

    def sizeHint(self):
        return QSize(70, 70)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self._drag_cooldown:
            self._drag_cooldown = True
            self._cooldown_timer.start(100)  # 100ms cooldown
            
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            
            # Start drag operation
            drag.exec(Qt.DropAction.MoveAction)

    def _reset_cooldown(self):
        self._drag_cooldown = False