from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QSpinBox, QSlider,
    QHBoxLayout, QVBoxLayout, QGridLayout
)

from model import Model

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛР3 - Часть 2 - MVC")
        self.resize(700, 300)

        self._model = Model()
        self._update_count = 0

        self.build_ui()
        self._model.attach(self.update_from_model)


    # Интерфейс

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        grid = QGridLayout()
        central.setLayout(grid)

        # Подписи "A <= B <= C"
        grid.addWidget(self._make_caption("A"), 0, 0)
        grid.addWidget(self._make_caption("<="), 0, 1)
        grid.addWidget(self._make_caption("B"), 0, 2)
        grid.addWidget(self._make_caption("<="), 0, 3)
        grid.addWidget(self._make_caption("C"), 0, 4)

        self._lines = []
        self._spins = []
        self._sliders = []

        for i in range(3):
            line = QLineEdit()
            spin = QSpinBox()
            slider = QSlider(Qt.Horizontal)

            spin.setRange(self._model.get_min(), self._model.get_max())
            slider.setRange(self._model.get_min(), self._model.get_max())

            line.editingFinished.connect(lambda idx=i: self._on_line(idx))
            spin.valueChanged.connect(lambda v, idx=i: self._on_spin_changed(idx, v))
            slider.valueChanged.connect(lambda v, idx=i: self._on_slider_changed(idx, v))

            grid.addWidget(line, 1, i * 2)
            grid.addWidget(spin, 2, i * 2)
            grid.addWidget(slider, 3, i * 2)

            self._lines.append(line)
            self._spins.append(spin)
            self._sliders.append(slider)

    def _make_caption(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(20)
        label.setFont(font)
        return label

    # Обработка ввода

    def _on_line(self, index):
        text = self._lines[index].text().strip()
        try:
            value = int(text)
        except ValueError:
            value = self._model.get_values()[index]
        self._model.set_value(index, value)
        # Возвращаем в поле актуальное значение (модель могла обрезать).
        current = self._model.get_values()[index]
        self._lines[index].blockSignals(True)
        self._lines[index].setText(str(current))
        self._lines[index].blockSignals(False)

    def _on_spin_changed(self, index, value):
        self._model.set_value(index, value)
        current = self._model.get_values()[index]
        if self._spins[index].value() != current:
            self._spins[index].blockSignals(True)
            self._spins[index].setValue(current)
            self._spins[index].blockSignals(False)

    def _on_slider_changed(self, index, value):
        self._model.set_value(index, value)
        current = self._model.get_values()[index]
        if self._sliders[index].value() != current:
            self._sliders[index].blockSignals(True)
            self._sliders[index].setValue(current)
            self._sliders[index].blockSignals(False)

    # Обновление формы

    def update_from_model(self):
        self._update_count += 1
        values = self._model.get_values()
        print("[Visual] update_from_model №" + str(self._update_count) + " - " + str(values))

        for i in range(3):
            # blockSignals, чтобы программная установка не дёргала модель снова.
            self._lines[i].blockSignals(True)
            self._spins[i].blockSignals(True)
            self._sliders[i].blockSignals(True)

            self._lines[i].setText(str(values[i]))
            self._spins[i].setValue(values[i])
            self._sliders[i].setValue(values[i])

            self._lines[i].blockSignals(False)
            self._spins[i].blockSignals(False)
            self._sliders[i].blockSignals(False)
