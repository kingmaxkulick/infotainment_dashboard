"""
Base class for draggable widgets in the display area with improved drag handling
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QPoint, QMimeData
from PyQt6.QtGui import QDrag
import ast

class DraggableWidget(QWidget):
    def __init__(self, widget_type, parent=None):
        super().__init__(parent)
        self.widget_type = widget_type
        self.drag_start_position = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize widget UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }
        """)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)
        
        # Header for drag handle
        self.header = QWidget()
        self.header.setFixedHeight(30)
        self.header.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.1);
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border: none;
            }
        """)
        
        # Header layout
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        # Title in header
        self.title = QLabel(self.widget_type)
        self.title.setStyleSheet("""
            QLabel {
                color: rgba(0, 0, 0, 0.8);
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        header_layout.addWidget(self.title)
        
        # Add header to main layout
        self.layout.addWidget(self.header)
        
        # Content area
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.layout.addWidget(self.content)

    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Only start drag if clicking in header area
            if self.header.geometry().contains(event.position().toPoint()):
                self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if not self.drag_start_position:
            return
            
        # Check if the movement is significant enough to start a drag
        delta = event.position().toPoint() - self.drag_start_position
        if delta.manhattanLength() < 10:
            return
            
        # Create drag object
        drag = QDrag(self)
        mime_data = QMimeData()
        
        # Include widget information in mime data
        data = {
            "type": "existing_widget",
            "widget_type": self.widget_type,
            "current_position": self.parent().layout.indexOf(self)
        }
        mime_data.setText(str(data))
        
        drag.setMimeData(mime_data)
        
        # Optional: Create and set drag pixmap
        # drag.setPixmap(self.grab())
        # drag.setHotSpot(event.position().toPoint())
        
        # Execute drag operation
        result = drag.exec(Qt.DropAction.MoveAction)
        
        # Reset drag start position
        self.drag_start_position = None

    def add_content(self, widget):
        """Add content to the widget's content area"""
        self.content_layout.addWidget(widget)
        
    def remove_content(self):
        """Remove all content from the widget"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def update_data(self, data):
        """Update widget with new data - to be implemented by subclasses"""
        pass

    def sizeHint(self):
        """Suggested size for the widget"""
        return QPoint(300, 200)  # Default size

    def minimumSizeHint(self):
        """Minimum size for the widget"""
        return QPoint(200, 150)  # Minimum size

    def text(self):
        """Return widget type for compatibility with drag and drop"""
        return self.widget_type