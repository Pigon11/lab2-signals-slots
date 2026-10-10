## футы
from PyQt5.QtCore import QObject, pyqtSignal

class FeetSignal(QObject):
    changed = pyqtSignal(float)