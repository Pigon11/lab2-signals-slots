from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit
)
import sys

import cl1
import cl2
import cl3


class LengthConverter(QMainWindow):
    METERS_PER_MILE = 1609.344
    METERS_PER_FOOT = 0.3048

    STYLE_NORMAL = ""
    STYLE_ERROR = "border: 2px solid red; background-color: #ffe6e6;"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лаба 2 — Конвертер длины (сигналы-слоты)")
        self.resize(460, 320)

        self.updating = False

        # --- источники сигналов ---
        self.meters_signal = cl1.MetersSignal()
        self.miles_signal = cl2.MilesSignal()
        self.feet_signal = cl3.FeetSignal()

        self.meters_signal.changed.connect(self.on_meters_signal)
        self.miles_signal.changed.connect(self.on_miles_signal)
        self.feet_signal.changed.connect(self.on_feet_signal)

        # --- поля ввода ---
        self.meters = QLineEdit()
        self.miles = QLineEdit()
        self.feet = QLineEdit()

        self.meters.setPlaceholderText("например, 100")
        self.miles.setPlaceholderText("например, 1")
        self.feet.setPlaceholderText("например, 10")

        self.meters.textEdited.connect(self.on_meters_edited)
        self.miles.textEdited.connect(self.on_miles_edited)
        self.feet.textEdited.connect(self.on_feet_edited)

        # --- подсказка об ошибке ---
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)

        # --- раскладка ---
        layout = QVBoxLayout()
        layout.addLayout(self._row("Метры (м):", self.meters))
        layout.addLayout(self._row("Мили (mi):", self.miles))
        layout.addLayout(self._row("Футы (ft):", self.feet))
        layout.addWidget(self.error_label)

        hint = QLabel("Введите любое значение — остальные пересчитаются автоматически")
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def _row(self, label_text, widget):
        row = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(110)
        row.addWidget(label)
        row.addWidget(widget)
        return row

    # ---------- обработчики полей ----------

    def on_meters_edited(self, text):
        if self.updating:
            return
        value = self._validate(text, self.meters)
        if value is None:
            return
        self.meters_signal.changed.emit(value)

    def on_miles_edited(self, text):
        if self.updating:
            return
        value = self._validate(text, self.miles)
        if value is None:
            return
        self.miles_signal.changed.emit(value)

    def on_feet_edited(self, text):
        if self.updating:
            return
        value = self._validate(text, self.feet)
        if value is None:
            return
        self.feet_signal.changed.emit(value)

    # ---------- слоты сигналов ----------

    def on_meters_signal(self, meters):
        self._update_fields(meters, source="meters")

    def on_miles_signal(self, miles):
        self._update_fields(miles * self.METERS_PER_MILE, source="miles")

    def on_feet_signal(self, feet):
        self._update_fields(feet * self.METERS_PER_FOOT, source="feet")

    # ---------- пересчёт (обновляем ВСЕ поля, кроме того, где сидит пользователь) ----------

    def _update_fields(self, meters, source):
        self.updating = True
        try:
            if source != "meters":
                self.meters.setText(f"{meters:.4f}")
            if source != "miles":
                self.miles.setText(f"{meters / self.METERS_PER_MILE:.4f}")
            if source != "feet":
                self.feet.setText(f"{meters / self.METERS_PER_FOOT:.4f}")
        finally:
            self.updating = False

    # ---------- валидация ----------

    def _validate(self, text, field):
        text = text.strip().replace(",", ".")

        if not text:
            self._clear_error()
            field.setStyleSheet(self.STYLE_NORMAL)
            return None

        try:
            value = float(text)
        except ValueError:
            self._show_error(f"«{text}» — не является числом")
            field.setStyleSheet(self.STYLE_ERROR)
            return None

        if value < 0:
            self._show_error("Расстояние не может быть отрицательным")
            field.setStyleSheet(self.STYLE_ERROR)
            return None

        self._clear_error()
        field.setStyleSheet(self.STYLE_NORMAL)
        return value

    def _show_error(self, message):
        self.error_label.setText(message)

    def _clear_error(self):
        self.error_label.setText("")


class Data:
    def __init__(self):
        self.myData = []

    def getData(self):
        return self.myData


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LengthConverter()
    window.show()
    app.exec()