import os
from ui.bbtwindow import BBTWindow
from PyQt5.QtWidgets import QApplication

GRAPH_NAME = "realbx.pkl"

cd = os.path.abspath("./")
mapPath = ""
graphPath = ""

if os.name == "nt": #WINDOWS
    mapPath = (cd + "\\map.html").split('\\')
    mapPath = '/'.join(mapPath)
    graphPath = cd + "\\" + GRAPH_NAME
else: #LINUX/MACOS/OTHERS
    mapPath = cd + "/map.html"
    graphPath = cd + "/" + GRAPH_NAME

app = QApplication([])
window = BBTWindow(mapPath, graphPath)
app.exec_()
