
import sys

import cv2
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget
)


class PhotoEditor(QMainWindow):
    """Фоторедактор."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Фоторедактор")
        self.resize(900, 700)

        # Переменные для хранения изображений
        self.original_image = None
        self.current_image = None

        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса."""

        # Область отображения изображения
        self.image_label = QLabel("Загрузите изображение")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid gray;")

        # Кнопки управления
        self.load_button = QPushButton("Загрузить")
        self.apply_button = QPushButton("Применить фильтр")
        self.save_button = QPushButton("Сохранить")

        # Выбор фильтра
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "Размытие",
            "Оттенки серого"
        ])

        # Слайдер радиуса размытия
        self.radius_label = QLabel("Радиус: 0")

        self.radius_slider = QSlider(Qt.Orientation.Horizontal)
        self.radius_slider.setRange(0, 50)
        self.radius_slider.setValue(0)

        # Подключение сигналов
        self.load_button.clicked.connect(self.load_image)
        self.apply_button.clicked.connect(self.apply_filter)
        self.save_button.clicked.connect(self.save_image)
        self.radius_slider.valueChanged.connect(self.on_slider_changed)
        self.filter_combo.currentIndexChanged.connect(self.on_filter_changed)

        # Компоновка слайдера
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.radius_label)
        slider_layout.addWidget(self.radius_slider)

        # Основная компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.image_label, stretch=1)
        layout.addWidget(self.load_button)
        layout.addWidget(self.filter_combo)
        layout.addLayout(slider_layout)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.save_button)

        # Центральный виджет
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def load_image(self):
        """Загрузка изображения."""

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)"
        )

        if not path:
            return

        # Чтение изображения с поддержкой кириллицы в пути
        data = np.fromfile(path, dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if image is None:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось загрузить изображение"
            )
            return

        self.original_image = image
        self.current_image = image.copy()

        self.radius_slider.setValue(0)
        self.display_image(self.current_image)

    def display_image(self, image):
        """Отображение изображения в QLabel."""

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb.shape

        qimage = QImage(
            rgb.data,
            w,
            h,
            ch * w,
            QImage.Format.Format_RGB888
        )

        pixmap = QPixmap.fromImage(qimage)

        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def on_slider_changed(self, value):
        """Изменение радиуса размытия."""

        self.radius_label.setText(f"Радиус: {value}")

        if self.filter_combo.currentText() == "Размытие":
            self.apply_filter()

    def on_filter_changed(self):
        """Управление доступностью слайдера."""

        self.radius_slider.setEnabled(
            self.filter_combo.currentText() == "Размытие"
        )

    def apply_filter(self):
        """Применение выбранного фильтра."""

        if self.original_image is None:
            return

        filter_name = self.filter_combo.currentText()

        if filter_name == "Размытие":
            radius = self.radius_slider.value()

            if radius == 0:
                result = self.original_image.copy()
            else:
                ksize = 2 * radius + 1

                result = cv2.GaussianBlur(
                    self.original_image,
                    (ksize, ksize),
                    0
                )

        elif filter_name == "Оттенки серого":
            gray = cv2.cvtColor(
                self.original_image,
                cv2.COLOR_BGR2GRAY
            )

            result = cv2.cvtColor(
                gray,
                cv2.COLOR_GRAY2BGR
            )

        else:
            return

        self.current_image = result
        self.display_image(self.current_image)

    def save_image(self):
        """Сохранение обработанного изображения."""

        if self.current_image is None:
            QMessageBox.information(
                self,
                "Сохранение",
                "Нет изображения для сохранения"
            )
            return

        path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Сохранить изображение",
            "result.png",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)"
        )

        if not path:
            return

        # Определение формата файла
        ext = "." + path.rsplit(".", 1)[-1] if "." in path else ".png"

        if "." not in path:
            path += ext

        # Кодирование изображения
        ok, buffer = cv2.imencode(ext, self.current_image)

        if ok:
            # Сохранение с поддержкой кириллицы в пути
            buffer.tofile(path)

            QMessageBox.information(
                self,
                "Сохранение",
                "Изображение сохранено"
            )
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось сохранить изображение"
            )

    def resizeEvent(self, event):
        """Обновление изображения при изменении размера окна."""

        super().resizeEvent(event)

        if self.current_image is not None:
            self.display_image(self.current_image)


def main():
    app = QApplication(sys.argv)

    window = PhotoEditor()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
