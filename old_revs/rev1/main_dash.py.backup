import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QGridLayout, QWidget, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QDrag, QImage
from PyQt6.QtCore import Qt, QMimeData, QPoint, QTimer, QSize
from PIL import Image, ImageFilter
import io


class DraggableButton(QPushButton):
    def __init__(self, text, icon_name=""):
        super().__init__(text)
        self._drag_cooldown = False
        self._cooldown_timer = QTimer(self)
        self._cooldown_timer.timeout.connect(self._reset_cooldown)
        self._cooldown_timer.setSingleShot(True)
        
        self.setFixedSize(60, 60)
        
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


class DraggableWidget(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
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
        self.drag_active = False
        self._last_drag_time = 0
        self.setMinimumHeight(50)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() <= self.height() * 0.2:
                self.drag_start_position = event.position().toPoint()
                self.drag_active = False

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton) or not self.drag_start_position:
            return

        delta = event.position().toPoint() - self.drag_start_position

        if (delta.y() > abs(delta.x()) and
            self.drag_start_position.y() <= self.height() * 0.2):
            
            if delta.y() > QApplication.startDragDistance() * 0.5:
                if not self.drag_active:
                    self.drag_active = True
                    drag = QDrag(self)
                    mime_data = QMimeData()
                    mime_data.setText(self.text())
                    mime_data.setProperty("removal_drag", True)
                    drag.setMimeData(mime_data)
                    drag.exec(Qt.DropAction.MoveAction)
                return

        if delta.manhattanLength() < QApplication.startDragDistance():
            return

        if not self.drag_active:
            self.drag_active = True
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)

    def mouseReleaseEvent(self, event):
        self.drag_start_position = None
        self.drag_active = False


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
                if len(self.widgets) == 0:  # If this was the last widget
                    self.parent().parent().restore_background()  # Restore clear background
                event.acceptProposedAction()
                return

            relative_x = drop_position.x() / self.width()
            desired_position = 0 if relative_x < 0.33 else (2 if relative_x > 0.67 else 1)

            if not any(w.text() == widget_text for w in self.widgets):
                if len(self.widgets) >= 3:
                    return
                if len(self.widgets) == 0:  # If this is the first widget
                    self.parent().parent().set_blurred_background()  # Set blurred background
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


class MainDash(QMainWindow):
    def __init__(self):
        super().__init__()
        
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        target_width = screen_width
        target_height = int(target_width * 9 / 16)
        if target_height > screen_height:
            target_height = screen_height
            target_width = int(target_height * 16 / 9)

        self.setWindowTitle("Infotainment Dashboard - Home Screen")
        self.setGeometry(100, 100, target_width, target_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Store the background image path
        self.background_image_path = "/home/mkulick/Documents/modern_sports_car_offcenter_right.jpg"
        
        # Load and store both normal and blurred backgrounds
        self.normal_background = QPixmap(self.background_image_path)
        self.blurred_background = self.create_blurred_background(self.background_image_path)
        
        # Set initial background
        self.set_background(self.normal_background)

        # Display Area
        self.display_area = DropArea()
        self.main_layout.addWidget(self.display_area)

        # Bottom Bar
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet("""
            QFrame {
                background-color: rgba(51, 51, 51, 0.9);
                border-top: 1px solid #666;
            }
        """)
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(15, 5, 15, 5)
        self.bottom_layout.setSpacing(15)
        
        bottom_bar_height = int(target_height / 8)
        self.bottom_bar.setFixedHeight(bottom_bar_height)

        self.app_names = [
            "Navigation",
            "Music",
            "Climate",
            "Phone",
            "Vehicle Info",
            "Settings"
        ]

        self.bottom_layout.addStretch()
        
        self.buttons = [DraggableButton(name) for name in self.app_names]
        for button in self.buttons:
            self.bottom_layout.addWidget(button)
        
        self.bottom_layout.addStretch()

        self.main_layout.addWidget(self.bottom_bar)

    def create_blurred_background(self, image_path):
        # Open image with PIL
        with Image.open(image_path) as img:
            # Apply gaussian blur
            blurred = img.filter(ImageFilter.GaussianBlur(radius=10))
            
            # Convert PIL image back to QPixmap
            byte_array = io.BytesIO()
            blurred.save(byte_array, format='PNG')
            qimg = QImage.fromData(byte_array.getvalue())
            return QPixmap.fromImage(qimg)

    def set_background(self, pixmap):
        scaled_background = pixmap.scaled(
            self.width(),
            self.height(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding
        )
        palette = self.central_widget.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_background))
        self.central_widget.setPalette(palette)
        self.central_widget.setAutoFillBackground(True)

    def set_blurred_background(self):
        self.set_background(self.blurred_background)

    def restore_background(self):
        self.set_background(self.normal_background)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if hasattr(Qt, 'AA_UseOpenGLES'):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseOpenGLES)
    elif hasattr(Qt, 'AA_UseDesktopOpenGL'):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
    
    main_dash = MainDash()
    main_dash.show()
    sys.exit(app.exec())