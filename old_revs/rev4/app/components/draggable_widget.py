"""
Base class for draggable dashboard widgets
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag
from ..utils.constants import STYLES

class DraggableWidget(QWidget):
    def __init__(self, widget_type, parent=None):
        super().__init__(parent)
        self.widget_type = widget_type
        self.drag_start_position = None
        self.setup_ui()

    def setup_ui(self):
        """Setup basic widget UI"""
        self.setStyleSheet(STYLES["vehicle_widget"])
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 200)

    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Only start drag from the top portion of the widget
            if event.position().y() <= self.height() * 0.15:
                self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event):
        """Handle mouse move for drag operation"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if not self.drag_start_position:
            return
        
        # Check if we've moved far enough to start a drag
        distance = (event.position().toPoint() - self.drag_start_position).manhattanLength()
        if distance < Qt.ApplicationSettings.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.widget_type)
        mime_data.setProperty("removal_drag", True)
        drag.setMimeData(mime_data)
        
        # Execute drag operation
        drag.exec(Qt.DropAction.MoveAction)
        self.drag_start_position = None

    def text(self):
        """Return widget type for compatibility with drop handling"""
        return self.widget_type