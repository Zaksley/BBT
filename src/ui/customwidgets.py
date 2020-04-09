from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests, threading, decimal

def formatAdress(text):
    adress = text.split(" ")
    sep = "+"
    return sep.join(adress)

class SearchEdit(QLineEdit):
    showMessageBox = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SearchEdit, self).__init__(parent)

        self.currentThread = None
        self.model = QStandardItemModel()
        self.selectedItem = None

        completer = QCompleter()
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setModel(self.model)
        completer.activated[QModelIndex].connect(self.onSelectedItem)
        self.setCompleter(completer)

        self.showMessageBox.connect(self.onShowMessageBox)
        
    def onShowMessageBox(self, text):
        QMessageBox.critical(self, "Erreur", text, QMessageBox.Ok)
    
    def textChanged(self, text):
        self.selectedItem = None
        super(SearchEdit, self).textChanged(text)

    def onSelectedItem(self, modelIndex):
        self.selectedItem = modelIndex.row()
    
    def getCoords(self):
        if self.selectedItem != None:
            return self.model.takeItem(self.selectedItem).data()
        else: raise Exception("No adress selected")

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self._launchThread()
            return True

        return super(SearchEdit, self).event(event)
    
    def _updateAdresses(self):
        if self.text() == "":
            return

        self.model.clear()

        try:
            adresses = requests.get('https://nominatim.openstreetmap.org/search?q=' + formatAdress(self.text()) +'&format=json&countrycodes=fr',
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"},
                timeout=1.0).json()
        except Exception as err:
            self.showMessageBox.emit(str(err))
            return

        for adress in adresses:
            item = QStandardItem()
            item.setText(adress["display_name"])
            item.setData((decimal.Decimal(adress["lat"]), decimal.Decimal(adress["lon"])))
            self.model.appendRow(item)
        
    def _launchThread(self):
        if self.currentThread == None or not self.currentThread.is_alive():
            self.currentThread = threading.Thread(target=self._updateAdresses)
            self.currentThread.setDaemon(True)
            self.currentThread.start()
        
class SafetySlider(QWidget):
    def __init__(self, parent=None):
        super(SafetySlider, self).__init__(parent)

        self.layout = QHBoxLayout()

        self.safeLabel = QLabel("Sur ", self)
        self.fastLabel = QLabel(" Rapide", self)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(20)
        self.slider.setValue(10)

        self.layout.addWidget(self.safeLabel)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.fastLabel)

        self.setLayout(self.layout)

    def getValue(self):
        return self.slider.value() * 0.05