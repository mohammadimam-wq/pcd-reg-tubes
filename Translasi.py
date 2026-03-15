import sys
import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi


class ShowImage(QMainWindow):

    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('showgui.ui', self)

        self.image = None
        self.processed_image = None

        # Hubungkan menu
        self.actionGrayscale.triggered.connect(self.grayscale)
        self.actionBinary.triggered.connect(self.binary)
        self.actionResize.triggered.connect(self.resizeImage)
        self.actionRotation.triggered.connect(self.rotation)
        self.actionTranslasi.triggered.connect(self.translation)
        self.actionMedian.triggered.connect(self.median)

        self.loadButton.clicked.connect(self.loadClicked)

    # ================= LOAD IMAGE =================
    @pyqtSlot()
    def loadClicked(self):

        options = QFileDialog.Options()
        flname, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih Gambar",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)",
            options=options
        )

        if flname:
            self.loadImage(flname)

    def loadImage(self, flname):

        self.image = cv2.imread(flname)

        if self.image is not None:
            self.displayImage(self.image, self.imgLabel)

    # ================= GRAYSCALE =================
    def grayscale(self):

        if self.image is None:
            return

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        self.processed_image = gray
        self.displayImage(self.processed_image, self.hasilLabel)

    # ================= BINARY =================
    def binary(self):

        if self.image is None:
            return

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        self.processed_image = binary
        self.displayImage(self.processed_image, self.hasilLabel)

    # ================= RESIZE =================
    def resizeImage(self):

        if self.image is None:
            return

        height, width = self.image.shape[:2]

        resized = cv2.resize(self.image, (width // 2, height // 2))

        self.processed_image = resized
        self.displayImage(self.processed_image, self.hasilLabel)

    # ================= ROTATION =================
    def rotation(self):

        if self.image is None:
            return

        height, width = self.image.shape[:2]

        center = (width / 2, height / 2)

        matrix = cv2.getRotationMatrix2D(center, 90, 1)

        rotated = cv2.warpAffine(self.image, matrix, (width, height))

        self.processed_image = rotated
        self.displayImage(self.processed_image, self.hasilLabel)

    # ================= TRANSLATION =================
    def translation(self):

        if self.image is None:
            return

        height, width = self.image.shape[:2]

        tx = 100
        ty = 50

        matrix = np.float32([
            [1, 0, tx],
            [0, 1, ty]
        ])

        translated = cv2.warpAffine(self.image, matrix, (width, height))

        self.processed_image = translated
        self.displayImage(self.processed_image, self.hasilLabel)

    # ================= MEDIAN FILTER =================
    def median(self):

        if self.image is None:
            return

        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        img_out = img_gray.copy()

        h, w = img_gray.shape[:2]

        for i in range(3, h - 3):
            for j in range(3, w - 3):

                neighbors = []

                for k in range(-3, 4):
                    for l in range(-3, 4):

                        pixel = img_gray[i + k, j + l]
                        neighbors.append(pixel)

                neighbors.sort()

                median_value = neighbors[24]

                img_out[i, j] = median_value

        self.processed_image = img_out
        self.displayImage(self.processed_image, self.hasilLabel)

    # ================= DISPLAY IMAGE =================
    def displayImage(self, img_array, target_label):

        if img_array is None:
            return

        if len(img_array.shape) == 3:

            h, w, ch = img_array.shape
            bytes_per_line = ch * w

            img_display = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

            q_img = QImage(
                img_display.data,
                w,
                h,
                bytes_per_line,
                QImage.Format_RGB888
            )

        else:

            h, w = img_array.shape
            bytes_per_line = w

            q_img = QImage(
                img_array.data,
                w,
                h,
                bytes_per_line,
                QImage.Format_Grayscale8
            )

        target_label.setPixmap(QPixmap.fromImage(q_img))
        target_label.setScaledContents(True)
        target_label.setAlignment(QtCore.Qt.AlignCenter)


# ================= MAIN =================
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ShowImage()
    window.setWindowTitle('PCD - Show Image GUI')

    window.show()

    sys.exit(app.exec_())
