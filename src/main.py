import os
from ui.bbtwindow import BBTWindow
from PyQt5.QtWidgets import QApplication

cd = os.path.abspath("./")
mapPath = cd + "/map.html"
graphPath = cd + "/realbx.pkl"

app = QApplication([])
window = BBTWindow(mapPath, graphPath)
app.exec_()
