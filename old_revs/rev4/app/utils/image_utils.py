from PIL import Image, ImageFilter
from PyQt6.QtGui import QImage, QPixmap
import io


def create_blurred_background(image_path, blur_radius=10):
    """
    Creates a blurred version of the input image
    Args:
        image_path (str): Path to the source image
        blur_radius (int): Radius of the Gaussian blur (default: 10)
    Returns:
        QPixmap: Blurred image as a QPixmap
    """
    with Image.open(image_path) as img:
        # Apply gaussian blur
        blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # Convert PIL image back to QPixmap
        byte_array = io.BytesIO()
        blurred.save(byte_array, format='PNG')
        qimg = QImage.fromData(byte_array.getvalue())
        return QPixmap.fromImage(qimg)