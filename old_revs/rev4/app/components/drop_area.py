"""
Drop area for dashboard widgets with improved layout management
"""
from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from .vehicle_widget import VehicleWidget
from ..utils.constants import STYLES

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
        
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        self.widgets = []
        self.widget_positions = {}
        
        # Setup update mechanism
        self._update_pending = False
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._do_update)
        self._update_timer.setSingleShot(True)

    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """Handle drag move event"""
        if event.mimeData().hasText():
            # Handle removal drag differently
            if event.mimeData().property("removal_drag"):
                if event.position().y() > self.height() * 0.7:  # Increased removal zone
                    event.acceptProposedAction()
                    return
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event"""
        if event.mimeData().hasText():
            widget_text = event.mimeData().text()
            drop_position = event.position().toPoint()
            relative_y = drop_position.y() / self.height()
            
            # Handle widget removal
            if (event.mimeData().property("removal_drag") and relative_y > 0.7) or relative_y > 0.9:
                self.remove_widget(widget_text)
                if len(self.widgets) == 0:
                    self.parent().parent().restore_background()
                event.acceptProposedAction()
                return

            # Calculate desired position based on drop location
            relative_x = drop_position.x() / self.width()
            desired_position = 0 if relative_x < 0.33 else (2 if relative_x > 0.67 else 1)

            # Handle new widget or reposition existing
            if not any(w.text() == widget_text for w in self.widgets):
                if len(self.widgets) >= 3:  # Maximum 3 widgets
                    return
                if len(self.widgets) == 0:
                    self.parent().parent().set_blurred_background()
                self.add_widget(widget_text, desired_position)
            else:
                self.reposition_widget(widget_text, desired_position)
            
            event.acceptProposedAction()

    def add_widget(self, widget_text, desired_position):
        """Add a new widget to the drop area"""
        # Create appropriate widget based on type
        if widget_text == "Vehicle Info":
            widget = VehicleWidget(widget_text, self)
        else:
            return  # Only handle Vehicle Info widgets for now
            
        self.widgets.append(widget)
        
        # Find available position
        taken_positions = set(self.widget_positions.values())
        if desired_position in taken_positions:
            if len(self.widgets) < 3:
                available_positions = set([0, 1, 2]) - taken_positions
                position = min(available_positions, key=lambda x: abs(x - desired_position))
            else:
                position = desired_position
        else:
            position = desired_position
        
        self.widget_positions[widget] = position
        self.schedule_update()

    def remove_widget(self, widget_text):
        """Remove a widget from the drop area"""
        widget_to_remove = next((w for w in self.widgets if w.text() == widget_text), None)
        if widget_to_remove:
            self.widgets.remove(widget_to_remove)
            del self.widget_positions[widget_to_remove]
            widget_to_remove.setParent(None)
            self.schedule_update()

    def reposition_widget(self, widget_text, desired_position):
        """Reposition an existing widget"""
        moving_widget = next((w for w in self.widgets if w.text() == widget_text), None)
        if moving_widget:
            widget_to_swap = next((w for w, pos in self.widget_positions.items() 
                                 if pos == desired_position and w != moving_widget), None)
            if widget_to_swap:
                old_position = self.widget_positions[moving_widget]
                self.widget_positions[widget_to_swap] = old_position
            self.widget_positions[moving_widget] = desired_position
            self.schedule_update()

    def schedule_update(self):
        """Schedule a layout update"""
        if not self._update_pending:
            self._update_pending = True
            self._update_timer.start(50)

    def _do_update(self):
        """Perform the layout update"""
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
            self.layout.addWidget(widget, 0, position)
            
        self.layout.blockSignals(False)
        self.layout.update()