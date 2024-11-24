import sys
import os
# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.windows.main_dashboard import MainDash


def main():
    app = QApplication(sys.argv)
    
    if hasattr(Qt, 'AA_UseOpenGLES'):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseOpenGLES)
    elif hasattr(Qt, 'AA_UseDesktopOpenGL'):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
    
    main_dash = MainDash()
    main_dash.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()