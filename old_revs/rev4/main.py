"""
Main entry point for the infotainment dashboard application
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent)
sys.path.append(project_root)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from app.windows.main_dashboard import MainDash


def main():
    """Initialize and run the application"""
    app = QApplication(sys.argv)
    
    # Enable OpenGL support if available
    if hasattr(Qt, 'AA_UseOpenGLES'):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseOpenGLES)
    elif hasattr(Qt, 'AA_UseDesktopOpenGL'):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
    
    # Create and show the main window
    window = MainDash()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()