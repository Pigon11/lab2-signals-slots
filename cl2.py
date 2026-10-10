## мили
from PyQt5.QtCore import QObject, pyqtSignal

class MilesSignal(QObject):
    changed = pyqtSignal(float)