import cv2
from PySide6.QtCore import Signal, QThread, Slot
import numpy as np

class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.cv_img = None
        self.imageNum = 0

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, self.cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(self.cv_img)
        # shut down capture system
        cap.release()

    @Slot()
    def saveImg(self):
        if self.cv_img is not None:
            cv2.imwrite(f'Images\img{self.imageNum}.png', self.cv_img)
            self.imageNum += 1

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()