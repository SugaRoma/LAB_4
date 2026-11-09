
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
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


def main():
    app = QApplication(sys.argv)

    window = PhotoEditor()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
