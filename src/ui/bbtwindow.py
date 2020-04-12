import os, sys
sys.path.append(os.path.abspath("src/"))

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from .customwidgets import SearchEdit, SafetySlider
from utils.algorithms import pathAStar
from utils.osmparser import geoDistance
from utils.graphserializer import deserialize
import folium, math, threading

bxlat = 44.8333
bxlon = -0.5667

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

class BBTWindow(QWidget):
    reloadWebview = pyqtSignal()
    showMessageBox = pyqtSignal(str)

    def __init__(self, mapPath, graphPath):
        QWidget.__init__(self)

        self.initializeUI()

        ###     ATRIBUTES   ###
        self.mapPath = mapPath
        self.url = "file://" + self.mapPath
        self.graph = None
        self.threadpool = QThreadPool(self)
        self.threadpool.setMaxThreadCount(1)

        self.reloadWebview.connect(self.onReloadWebview)
        self.showMessageBox.connect(self.onShowMessageBox)

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

        self.stopBtn = QPushButton("Stop", self)
        self.stopBtn.clicked.connect(self.stop)

        self.webview = QWebEngineView(self)
        self.webview.urlChanged.connect(lambda url: self.webview.setUrl(QUrl(url)) if url != self.url else None) 
            
        self.statusLabel = QLabel("Fait.", self)
        self.statusLabel.setMaximumHeight(20)

        self.mainLayout.addLayout(self.firstLayout)
        self.mainLayout.addLayout(self.secondLayout)
        self.mainLayout.addWidget(self.goBtn)
        self.mainLayout.addWidget(self.stopBtn)
        self.mainLayout.addWidget(self.webview)
        self.mainLayout.addWidget(self.statusLabel)

        #RIGHT PART
        self.rightLayout = QVBoxLayout()

        #INFO PART
        self.infoBox = QGroupBox("Informations", self)
        self.infoBox.setMaximumWidth(300)
        self.infoLayout = QVBoxLayout()

        self.distanceLabel = QLabel("<strong>Distance</strong>: ", self)
        self.percentLabel = QLabel("<strong>Pistes cyclables ou chemins:</strong> ", self)

        self.infoLayout.addWidget(self.distanceLabel)
        self.infoLayout.addWidget(self.percentLabel)

        self.infoBox.setLayout(self.infoLayout)

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

        self.rightLayout.addWidget(self.infoBox)
        self.rightLayout.addWidget(self.paramsBox)

        self.globalLayout.addLayout(self.mainLayout)
        self.globalLayout.addLayout(self.rightLayout)
        self.setLayout(self.globalLayout)

        self.show()

    def onReloadWebview(self):
        self.webview.setUrl(QUrl(self.url))

    def onShowMessageBox(self, message):
        QMessageBox.information(self, "Information", message, QMessageBox.Ok)

    def go(self):
        if self.graph == None:
            return
        
        if self.threadpool.activeThreadCount() >= 1:
            return
        
        self.threadpool.start(Worker(self._goFunc))

    def stop(self):
        if self.threadpool.activeThreadCount() == 0:
            return

        self.statusLabel.setText("Arrêt du thread...")
        self.threadpool.reserveThread()
        self.threadpool.releaseThread()
        self.statusLabel.setText("Démarquage du graphe...")
        self.graph.unmarkAll()
        self.statusLabel.setText("Fait.")

    def _goFunc(self):
        self.statusLabel.setText("Placement des points...")
        try:
            startCoords = self.startAdress.getCoords()
            endCoords = self.endAdress.getCoords()
        except:
            self.showMessageBox.emit("Vous devez remplir les deux champs avec des adresses réelles\nTip: Appuyez sur Entrer pour la sélectionner")
            self.statusLabel.setText("Fait.")
            return

        self.map = folium.Map(location=(bxlat, bxlon), zoom_start=12)
        self.map.add_child(folium.Marker(startCoords, tooltip="Départ", popup=self.startAdress.text()))
        self.map.add_child(folium.Marker(endCoords, tooltip="Arivée", popup=self.endAdress.text()))

        self.statusLabel.setText("En cours de traitement du chemin optimal...")

        (start, end) = self.findNearestNodes(startCoords, endCoords)
        path = pathAStar(self.graph, start, end, 1.05)

        safeDistance = 0
        for i in range(len(path)-1):
            coord1 = path[i].getCoordinates()
            coord2 = path[i+1].getCoordinates()
            edge = self.graph.edgeBetween(path[i], path[i+1])

            #Safety color
            c = 'gray'
            if edge.getSafety() == "safe":
                c = 'green'
                safeDistance += edge.getLength()
            elif edge.getSafety() == "normal": c = 'blue'
            elif edge.getSafety() == "unsafe": c = 'orange'
            elif edge.getSafety() == "very_unsafe": c = 'red'

            #Comfort color
        
            self.map.add_child(folium.PolyLine([coord1, coord2], color=c))

        length = path[len(path)-1].getDistance()
        self.distanceLabel.setText(f"<strong>Distance:</strong> {round(length)}m")
        if length != 0: self.percentLabel.setText(f"<strong>Pistes cyclables ou chemins:</strong> {round(safeDistance/length * 100)}%")

        self.statusLabel.setText("Fait.")

        self.statusLabel.setText("Sauvegarde de la carte...")
        self.map.save(self.mapPath)
        self.reloadWebview.emit()#self.webview.setUrl(QUrl(self.url))

        self.statusLabel.setText("Démarquage du graphe...")
        self.graph.unmarkAll()
        for node in self.graph.getNodes():
            node.setPredecessor(None)
            node.setDistance(math.inf)
            node.setCost(math.inf)
        self.statusLabel.setText("Fait.")

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