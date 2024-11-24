"""
Draggable app button that includes layout position information in drag data
"""
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QDrag
from PyQt6.QtCore import Qt, QMimeData, QTimer, QSize
from ..utils.constants import COLORS

class DraggableButton(QPushButton):
    def __init__(self, text, icon_name=""):
        super().__init__()
        self._drag_cooldown = False
        self._cooldown_timer = QTimer(self)
        self._cooldown_timer.timeout.connect(self._reset_cooldown)
        self._cooldown_timer.setSingleShot(True)
        
        # Create layout for icon and text
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # Add text label
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 11px;
            }
        """)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label)
        
        self.setLayout(layout)
        self.setFixedSize(70, 70)
        
        # Enhanced styling
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid {COLORS['BORDER']};
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            QPushButton:pressed {{
                background-color: rgba(255, 255, 255, 0.15);
            }}
        """)

    def mousePressEvent(self, event):
        """Handle mouse press for dragging with position information"""
        if event.button() == Qt.MouseButton.LeftButton and not self._drag_cooldown:
            self._drag_cooldown = True
            self._cooldown_timer.start(100)
            
            drag = QDrag(self)
            mime_data = QMimeData()
            
            # Include button information
            data = {
                "type": "new_widget",  # Indicates this is a new widget creation
                "widget_type": self.text()
            }
            
            mime_data.setText(str(data))
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)

    def _reset_cooldown(self):
        self._drag_cooldown = False
        
    def text(self):
        """Return the button's text"""
        return self.findChild(QLabel).text()