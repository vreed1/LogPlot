import sys
import matplotlib.pyplot as plt
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QVBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from logPlotController import *
from Interface import Ui_LogPlot

class LogPlot(QMainWindow, Ui_LogPlot):

    def __init__(self):
        self.controller = Controller()
        QMainWindow.__init__(self)

        #Set up the user interface from Designer
        self.ui = Ui_LogPlot()
        self.ui.setupUi(self)

        #Set up plots
        self.CreateGraphCanvases()
        
        #Connect buttons
        self.ui.FileBrowseButton.clicked.connect(self.FileBrowse)
        self.ui.RecordButton.clicked.connect(self.Record)
        self.ui.PlotExcelButton.clicked.connect(self.PlotExcel)
        self.ui.previewSummary.toggled.connect(self.PreviewSummary)
        self.ui.previewAll.toggled.connect(self.PreviewAll)

    def CreateGraphCanvases(self):
        #Create empty plot
        figure = plt.Figure()
        axes = figure.add_subplot(111)
        
        #Create the preview canvas for Upload tab
        self.previewCanvas = FigureCanvas(figure)
        self.previewCanvas.setParent(self.ui.upload)
        self.previewToolbar = NavigationToolbar(self.previewCanvas, self.ui.upload)
        preview = self.CanvasLayout(self.previewCanvas, self.previewToolbar)
        self.ui.uploadLayout.addLayout(preview, 0, 1)

        #Create canvas for Plot tab
        self.plotCanvas = FigureCanvas(figure)
        self.plotCanvas.setParent(self.ui.plot)
        self.plotToolbar = NavigationToolbar(self.plotCanvas, self.ui.plot)
        plot = self.CanvasLayout(self.plotCanvas, self.plotToolbar)
        self.ui.plotLayout.addLayout(plot, 0, 1)
        
    def CanvasLayout(self, canvas, toolbar):
        plot = QVBoxLayout()
        plot.addWidget(canvas)
        plot.addWidget(toolbar)
        return plot
        
    def FileBrowse(self):
        self.ui.filePath.setText(QFileDialog.getOpenFileName())
        if not self.FileNameValid(self.ui.filePath.text()): return
        #By default, plot preview of summary when a file is opened
        self.ui.previewSummary.setChecked(True)
        self.PreviewSummary()
        
    def Record(self):
        records = []
        filename = self.ui.filePath.text()
        if not self.FileNameValid(filename): return
        self.controller.RecordDataFromFile(filename)

    def FileNameValid(self, filename):
        if not filename or not filename.endswith('.csv'):
            #TODO: error dialog, must provide valid filename
            return False
        else: return True

    def PreviewSummary(self):
        #get size of current figure and then clear
        figSize = self.previewCanvas.figure.get_size_inches()
        self.previewCanvas.figure.clf()
        #get new figure and adjust size
        self.previewCanvas.figure = self.controller.PlotSummaryPreview(self.ui.filePath.text())
        self.previewCanvas.figure.set_size_inches(figSize)
        #re-draw canvas
        self.previewCanvas.draw()

    def PreviewAll(self):
        #get size of current figure and then clear
        figSize = self.previewCanvas.figure.get_size_inches()
        self.previewCanvas.figure.clf()
        #get new figure and adjust size
        self.previewCanvas.figure = self.controller.PlotDetailedPreview(self.ui.filePath.text())
        self.previewCanvas.figure.set_size_inches(figSize)
        #re-draw canvas
        self.previewCanvas.draw()

    def PlotExcel(self):
        #Get directory of save location
        savePath = str(QFileDialog.getSaveFileName(self,
                                                   "Choose save location",
                                                   "untitled.xlsx",
                                                   "Excel files (*xlsx)"))
        if not savePath or not savePath.endswith('.xlsx'):
            #TODO: handle bad save path
            return
        
        #Plotting all records or just summary?
        if self.ui.previewAll.isChecked(): self.controller.PlotTempsExcel(savePath)
        elif self.ui.previewSummary.isChecked(): self.controller.PlotSummaryExcel(savePath)
        else: return
        
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    logPlot = LogPlot()
    logPlot.show()
    sys.exit(app.exec_())
