## метры

from PyQt5.QtCore import QObject, pyqtSignal

class MetersSignal(QObject):
    changed = pyqtSignal(float)