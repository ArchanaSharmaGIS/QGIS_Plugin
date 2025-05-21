from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.core import QgsProject, QgsVectorLayer
from PyQt5.QtWidgets import QDialog
from .uploadshapefile_dialog_base import Ui_uploadshapefileDialogBase  # ✅ Correct import

import os

class UploadShapefile:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        self.action = QAction("Upload Shapefile", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("Upload Shapefile", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removePluginMenu("Upload Shapefile", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        if not self.dialog:
            self.dialog = UploadShapefileDialog()
        self.dialog.show()
        self.dialog.exec_()

class UploadShapefileDialog(QDialog, Ui_uploadshapefileDialogBase):  # ✅ Fixed here too
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.load_shapefile)

    def load_shapefile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Shapefile", "", "Shapefiles (*.shp)")
        if file_path:
            layer = QgsVectorLayer(file_path, os.path.basename(file_path), "ogr")
            if layer.isValid():
                QgsProject.instance().addMapLayer(layer)
            else:
                QMessageBox.critical(self, "Error", "Failed to load the shapefile.")
