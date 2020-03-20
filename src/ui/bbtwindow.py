from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from customwidgets import *
import os, folium

bxlat = 44.8333
bxlon = -0.5667

path = "map.html"

class BBTWindow(QWidget):
    def __init__(self, url):
        QWidget.__init__(self)

        ###     GUI PART     ###
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowTitle("Bordeaux Bike Travel")

        self.globalLayout = QHBoxLayout()

        #MAIN PART
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 5, 10, 0)

        self.firstLayout = QHBoxLayout()
        self.secondLayout = QHBoxLayout()

        self.lbl_start = QLabel("Départ : ", self)
        self.lbl_end = QLabel("Arrivée : ", self)

        self.startAdress = SearchEdit(self)
        self.endAdress = SearchEdit(self)

        self.firstLayout.addWidget(self.lbl_start)
        self.firstLayout.addWidget(self.startAdress)
        self.secondLayout.addWidget(self.lbl_end)
        self.secondLayout.addWidget(self.endAdress)

        self.btn_update = QPushButton("Aller !", self)
        self.btn_update.clicked.connect(self.setPoints)

        self.webview = QWebEngineView(self)

        self.statusLabel = QLabel("Fait.", self)
        self.statusLabel.setMaximumHeight(20)

        self.mainLayout.addLayout(self.firstLayout)
        self.mainLayout.addLayout(self.secondLayout)
        self.mainLayout.addWidget(self.btn_update)
        self.mainLayout.addWidget(self.webview)
        self.mainLayout.addWidget(self.statusLabel)

        #PARAMS PART
        self.paramsBox = QGroupBox("Paramètres", self)
        self.paramsBox.setMaximumWidth(300)
        self.paramsLayout = QVBoxLayout()

        self.pathCheck = QCheckBox("Eviter les chemins", self)
        self.safetySlide = SafetySlider(self)

        self.paramsLayout.addWidget(self.safetySlide)
        self.paramsLayout.addWidget(self.pathCheck)
        self.paramsLayout.addStretch(1)
        self.paramsBox.setLayout(self.paramsLayout)

        self.globalLayout.addLayout(self.mainLayout)
        self.globalLayout.addWidget(self.paramsBox)
        self.setLayout(self.globalLayout)

        self.show()

        ###     MAP PART     ###
        self.statusLabel.setText("Sauvegarde de la carte...")
        
        self.url = url
        self.map = folium.Map(location=(bxlat, bxlon), zoom_start=12)
        self.map.save(path)
        self.webview.setUrl(QUrl(self.url))
        
        self.statusLabel.setText("Fait.")

    def setPoints(self):
        self.statusLabel.setText("Placement des points...")
        try:
            startCoords = self.startAdress.getCoords()
            endCoords = self.endAdress.getCoords()
        except Exception as err:
            QMessageBox.information(self, "Adresses", """Vous devez remplir les deux champs avec des adresses réelles\n
            Tip: Appuyez sur Tab pour l'auto-completion""", QMessageBox.Ok)
            self.statusLabel.setText("Fait.")
            return

        self.statusLabel.setText("Sauvegarde de la carte...")
        self.map = folium.Map(location=(bxlat, bxlon), zoom_start=12)
        self.map.add_child(folium.Marker(startCoords, tooltip="Départ", popup=self.startAdress.text()))
        self.map.add_child(folium.Marker(endCoords, tooltip="Arivée", popup=self.endAdress.text()))

        self.map.save(path)
        self.webview.setUrl(self.url)

        self.statusLabel.setText("Fait.")

if __name__ == "__main__":    
    app = QApplication([])
    window = BBTWindow(QUrl("file://" + os.path.abspath("./") + "/" + path))
    app.exec_()