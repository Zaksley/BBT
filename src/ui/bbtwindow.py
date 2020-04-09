import os, sys
sys.path.append(os.path.abspath("src/"))

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from .customwidgets import SearchEdit, SafetySlider
from utils.algorithms import pathAStar
from utils.osmparser import geoDistance
from utils.graphserializer import deserialize
import folium, math

bxlat = 44.8333
bxlon = -0.5667

class BBTWindow(QWidget):
    def __init__(self, mapPath, graphPath):
        QWidget.__init__(self)

        self.initializeUI()

        ###     ATRIBUTES   ###
        self.mapPath = mapPath
        self.url = "file://" + self.mapPath
        self.graph = None

        ###     MAP PART     ###
        self.statusLabel.setText("Sauvegarde de la carte...")
        
        self.map = folium.Map(location=(bxlat, bxlon), zoom_start=12)
        self.map.save(self.mapPath)
        self.webview.setUrl(QUrl(self.url))
        
        self.statusLabel.setText("Fait.")

        ###     GRAPH PART   ###
        self.statusLabel.setText("Ouverture du graph...")      
        self.graph = deserialize(graphPath)
        self.statusLabel.setText("Fait.")   

        if self.graph == None:
            QMessageBox.critical(self, "Erreur", "Le graph n'a pas pu être chargé au chemin " + graphPath, QMessageBox.Ok)
 
    def initializeUI(self):
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

        self.goBtn = QPushButton("Aller !", self)
        self.goBtn.clicked.connect(self.go)

        self.webview = QWebEngineView(self)
        self.webview.urlChanged.connect(lambda url: self.webview.setUrl(QUrl(url)) if url != self.url else None) 
            
        self.statusLabel = QLabel("Fait.", self)
        self.statusLabel.setMaximumHeight(20)

        self.mainLayout.addLayout(self.firstLayout)
        self.mainLayout.addLayout(self.secondLayout)
        self.mainLayout.addWidget(self.goBtn)
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

    def go(self):
        if self.graph == None:
            return

        self.statusLabel.setText("Placement des points...")
        try:
            startCoords = self.startAdress.getCoords()
            endCoords = self.endAdress.getCoords()
        except:
            QMessageBox.information(self, "Adresses", """Vous devez remplir les deux champs avec des adresses réelles\n
            Tip: Appuyez sur Tab pour l'auto-completion""", QMessageBox.Ok)
            self.statusLabel.setText("Fait.")
            return

        self.map = folium.Map(location=(bxlat, bxlon), zoom_start=12)
        self.map.add_child(folium.Marker(startCoords, tooltip="Départ", popup=self.startAdress.text()))
        self.map.add_child(folium.Marker(endCoords, tooltip="Arivée", popup=self.endAdress.text()))

        self.statusLabel.setText("En cours de traitement du chemin optimal...")

        (start, end) = self.findNearestNodes(startCoords, endCoords)
        path = pathAStar(self.graph, start, end, 1.05)

        for i in range(len(path)-1):
            coord1 = path[i].getCoordinates()
            coord2 = path[i+1].getCoordinates()
            edge = self.graph.edgeBetween(path[i], path[i+1])

            #Safety color
            c = 'red'
            if edge.getSafety() == "safe":  c = 'green'
            elif edge.getSafety() == "normal":  c = 'blue'
            elif edge.getSafety() == "unsafe": c = 'orange'
            elif edge.getSafety() == "very_unsafe": c = 'black'

            #Comfort color
        
            self.map.add_child(folium.PolyLine([coord1, coord2], color=c))

        self.statusLabel.setText("Fait.")

        self.statusLabel.setText("Sauvegarde de la carte...")
        self.map.save(self.mapPath)
        self.webview.setUrl(QUrl(self.url))

        self.statusLabel.setText("Fait.")

        self.graph.unmarkAll()

    def findNearestNodes(self, startCoords, endCoords):
        nearStart = None
        nearStartDistance = math.inf
        nearEnd = None
        nearEndDistance = math.inf

        for node in self.graph.getNodes():
            coords = node.getCoordinates()
            fromStart = geoDistance(coords[0], coords[1], startCoords[0], startCoords[1])
            fromEnd = geoDistance(coords[0], coords[1], endCoords[0], endCoords[1])

            if fromStart < nearStartDistance:
                nearStart = node
                nearStartDistance = fromStart
            if fromEnd < nearEndDistance:
                nearEnd = node
                nearEndDistance = fromEnd

        return (nearStart, nearEnd)