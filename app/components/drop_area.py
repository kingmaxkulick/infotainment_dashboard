"""
Drop area for dashboard widgets with intelligent layout management
"""
from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from .vehicle_widget import VehicleWidget
import ast

class DropArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the UI"""
        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Main layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Widget tracking
        self.widgets = []
        self.widget_positions = {}
        
        # Update handling
        self._update_pending = False
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._do_update)
        self._update_timer.setSingleShot(True)

    def dragEnterEvent(self, event):
        """Accept drag entry if it has text data"""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """Handle drag movement and show potential drop zones"""
        if not event.mimeData().hasText():
            return

        pos = event.position()
        relative_x = pos.x() / self.width()
        relative_y = pos.y() / self.height()

        # Handle drag from header for removal
        try:
            data = ast.literal_eval(event.mimeData().text())
            is_existing = data.get("type") == "existing_widget"
        except:
            is_existing = False

        # Check for removal zone
        if is_existing and relative_y < 0.15:
            self.showRemovalIndicator()
            event.acceptProposedAction()
            return

        # Calculate and show appropriate drop zones
        self.updateDropZones(relative_x, len(self.widgets))
        event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle widget drops"""
        if not event.mimeData().hasText():
            return

        pos = event.position()
        relative_x = pos.x() / self.width()
        relative_y = pos.y() / self.height()

        try:
            data = ast.literal_eval(event.mimeData().text())
            widget_type = data.get("widget_type")
            is_new = data.get("type") == "new_widget"
            
            # Handle widget removal
            if not is_new and relative_y < 0.15:
                self.remove_widget(widget_type)
                if len(self.widgets) == 0:
                    self.parent().parent().restore_background()
                event.acceptProposedAction()
                return

            # Calculate desired position based on layout
            if len(self.widgets) == 0:
                # First widget - full screen
                if len(self.widgets) == 0:
                    self.parent().parent().set_blurred_background()
                self.add_widget(widget_type, 0)
            elif len(self.widgets) == 1:
                # Second widget - split into halves
                position = 0 if relative_x < 0.5 else 1
                self.add_widget(widget_type, position)
            else:
                # Third widget - split into thirds
                if relative_x < 0.33:
                    position = 0
                elif relative_x < 0.66:
                    position = 1
                else:
                    position = 2
                self.add_widget(widget_type, position)

            event.acceptProposedAction()

        except Exception as e:
            print(f"Error handling drop: {e}")
            return

    def add_widget(self, widget_type, desired_position):
        """Add a new widget to the specified position"""
        # Create appropriate widget based on type
        if widget_type == "Vehicle Info":
            widget = VehicleWidget(widget_type, self)
        else:
            return  # Only handle Vehicle Info for now
            
        if len(self.widgets) >= 3:
            return  # Maximum 3 widgets
            
        self.widgets.append(widget)
        
        # Handle positioning
        taken_positions = set(self.widget_positions.values())
        if desired_position in taken_positions:
            if len(self.widgets) < 3:
                available = set(range(3)) - taken_positions
                position = min(available, key=lambda x: abs(x - desired_position))
            else:
                position = desired_position
        else:
            position = desired_position
            
        self.widget_positions[widget] = position
        self.schedule_update()

    def remove_widget(self, widget_type):
        """Remove a widget and adjust layout"""
        widget_to_remove = next((w for w in self.widgets 
                               if hasattr(w, 'text') and w.text() == widget_type), None)
        if widget_to_remove:
            self.widgets.remove(widget_to_remove)
            del self.widget_positions[widget_to_remove]
            widget_to_remove.setParent(None)
            self.schedule_update()

    def schedule_update(self):
        """Schedule a layout update"""
        if not self._update_pending:
            self._update_pending = True
            self._update_timer.start(50)  # 50ms delay

    def _do_update(self):
        """Perform the actual layout update"""
        self._update_pending = False
        self.rearrange_widgets()

    def rearrange_widgets(self):
        """Rearrange all widgets in the layout"""
        self.layout.blockSignals(True)
        
        # Clear current layout
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        # Add widgets in their new positions
        for widget, position in sorted(self.widget_positions.items(), key=lambda x: x[1]):
            # Adjust column span based on widget count
            colspan = 1
            if len(self.widgets) == 1:
                colspan = self.layout.columnCount()
            elif len(self.widgets) == 2:
                colspan = self.layout.columnCount() // 2
                
            self.layout.addWidget(widget, 0, position * colspan, 1, colspan)
            
        self.layout.blockSignals(False)
        self.layout.update()

    def updateDropZones(self, relative_x, widget_count):
        """Update visual drop zone indicators"""
        # Implementation for visual feedback during drag
        # This would show where the widget will be placed
        pass

    def showRemovalIndicator(self):
        """Show visual indicator for removal zone"""
        # Implementation for removal zone visual feedback
        pass