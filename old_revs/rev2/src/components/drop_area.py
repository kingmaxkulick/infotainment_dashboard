from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from .draggable_widget import DraggableWidget


class DropArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.widgets = []
        self.widget_positions = {}
        
        self._update_pending = False
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._do_update)
        self._update_timer.setSingleShot(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            if event.mimeData().property("removal_drag"):
                if event.position().y() > self.height() * 0.6:
                    event.acceptProposedAction()
                    return
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            widget_text = event.mimeData().text()
            drop_position = event.position().toPoint()
            relative_y = drop_position.y() / self.height()
            
            if (event.mimeData().property("removal_drag") and relative_y > 0.6) or relative_y > 0.8:
                self.remove_widget(widget_text)
                if len(self.widgets) == 0:
                    self.parent().parent().restore_background()
                event.acceptProposedAction()
                return

            relative_x = drop_position.x() / self.width()
            desired_position = 0 if relative_x < 0.33 else (2 if relative_x > 0.67 else 1)

            if not any(w.text() == widget_text for w in self.widgets):
                if len(self.widgets) >= 3:
                    return
                if len(self.widgets) == 0:
                    self.parent().parent().set_blurred_background()
                self.add_widget(widget_text, desired_position)
            else:
                moving_widget = next((w for w in self.widgets if w.text() == widget_text), None)
                if moving_widget:
                    widget_to_swap = next((w for w, pos in self.widget_positions.items() 
                                         if pos == desired_position and w != moving_widget), None)
                    if widget_to_swap:
                        old_position = self.widget_positions[moving_widget]
                        self.widget_positions[widget_to_swap] = old_position
                    self.widget_positions[moving_widget] = desired_position
                    self.schedule_update()

            event.acceptProposedAction()

    def add_widget(self, widget_text, desired_position):
        widget = DraggableWidget(widget_text, self)
        self.widgets.append(widget)
        
        taken_positions = set(self.widget_positions.values())
        
        if desired_position in taken_positions:
            if len(self.widgets) < 3:
                available_positions = set([0, 1, 2]) - taken_positions
                if available_positions:
                    position = min(available_positions, key=lambda x: abs(x - desired_position))
                else:
                    position = desired_position
            else:
                available_positions = set([0, 1, 2]) - taken_positions
                position = available_positions.pop() if available_positions else desired_position
        else:
            position = desired_position
        
        self.widget_positions[widget] = position
        self.schedule_update()

    def remove_widget(self, widget_text):
        widget_to_remove = next((w for w in self.widgets if w.text() == widget_text), None)
        if widget_to_remove:
            self.widgets.remove(widget_to_remove)
            del self.widget_positions[widget_to_remove]
            widget_to_remove.setParent(None)
            self.schedule_update()

    def schedule_update(self):
        if not self._update_pending:
            self._update_pending = True
            self._update_timer.start(50)

    def _do_update(self):
        self._update_pending = False
        self.rearrange_widgets()

    def rearrange_widgets(self):
        self.layout.blockSignals(True)
        
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        for widget, position in sorted(self.widget_positions.items(), key=lambda x: x[1]):
            self.layout.addWidget(widget, 0, position)
            
        self.layout.blockSignals(False)
        self.layout.update()