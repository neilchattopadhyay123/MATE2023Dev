from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap
import sys
import cv2
from PySide6.QtCore import Signal, Slot, Qt, QThread
import numpy as np
from videoThread import VideoThread
from videoWidget import VideoWidget
from imageWidget import ImageWidget

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mate GUI")

        self.videoWidget = VideoWidget()
        self.imageWidget = ImageWidget()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.videoWidget)
        self.layout.addWidget(self.imageWidget)

        self.setLayout(self.layout)

    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())
