from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QPixmap
import sys
import cv2
from PySide6.QtCore import Signal, Slot, Qt, QThread
import numpy as np
import os
from imageRec import PerspectiveTransform, seagrass

class ImageListThread(QThread):
    fileListSignal = Signal(list)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.fileList = os.listdir("Images")
  
    def run(self):
        while self._run_flag:
            if os.listdir("Images") != self.fileList:
                self.fileList = os.listdir("Images")
                self.fileListSignal.emit(os.listdir("Images"))
            self.sleep(1)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.tree_width = 600
        self.tree_height = 720

        self.file_tree = QTreeWidget(self)
        self.file_tree.setColumnCount(1)
        self.file_tree.setHeaderLabels(["File Name"])

        self.file_tree.resize(self.tree_width, self.tree_width)
        self.imageItem = QTreeWidgetItem(["Images"])

        self.perspective_transform_button = QPushButton("Perspective transform")
        
        self.perspectiveImageNum = 0

        self.seagrass_button = QPushButton("Seagrass Task")

        self.perspective_transform_button.clicked.connect(self.perspectiveTransformSlot)
        self.seagrass_button.clicked.connect(self.seagrassSlot)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.file_tree)
        self.layout.addWidget(self.perspective_transform_button)
        self.layout.addWidget(self.seagrass_button)
        # self.file_tree.selectedItems()

        self.setLayout(self.layout)

        self.imageListThread = ImageListThread()
        self.imageListThread.fileListSignal.connect(self.updateFiles)
        self.imageListThread.start()

    @Slot(list)
    def updateFiles(self, files):
        if self.imageItem.childCount() > 0:
            for i in reversed(range(self.imageItem.childCount())):
                self.imageItem.removeChild(self.imageItem.child(i))

        items = [] 
        for file in files:
            self.imageItem.addChild(QTreeWidgetItem([file]))
        self.file_tree.insertTopLevelItem(0, self.imageItem)

    @Slot()
    def perspectiveTransformSlot(self):
        if len(self.file_tree.selectedItems()) == 1:
            image = cv2.imread(f"Images/{self.file_tree.selectedItems()[0].data(0, 0)}")

            transform = PerspectiveTransform(image, imageNum=self.perspectiveImageNum)
            transform.perspective_transform(image)

            self.perspectiveImageNum += 1

    @Slot()
    def seagrassSlot(self):
        if len(self.file_tree.selectedItems()) == 2:
            image = cv2.imread(f"Images/{self.file_tree.selectedItems()[0].data(0, 0)}")
            image1 = cv2.imread(f"Images/{self.file_tree.selectedItems()[1].data(0, 0)}")
            seagrass(image, image1)
            
            
    def closeEvent(self, event):
        self.imageListThread.stop()
        event.accept()

