import os
from ui.bbtwindow import BBTWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

GRAPH_NAME = "graph.pkl"
ICON_NAME = "icon.png"

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
window.setWindowIcon(QIcon(ICON_NAME))
app.exec_()

os.remove(mapPath)