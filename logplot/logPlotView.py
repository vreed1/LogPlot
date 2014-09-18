import matplotlib.pyplot as plt
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QVBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from Interface import Ui_LogPlot

class LogPlot(QMainWindow, Ui_LogPlot):

    def __init__(self):
        #self.controller = Controller()
        QMainWindow.__init__(self)

        #Set up the user interface from Designer
        self.ui = Ui_LogPlot()
        self.ui.setupUi(self)

        #Set up plots
        self.CreateGraphCanvases()

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

    def UpdateCanvas(self, canvas, figure):
        #get size of current figure and then clear
        figSize = canvas.figure.get_size_inches()
        canvas.figure.clf()
        #get new figure and adjust size
        canvas.figure = figure
        canvas.figure.set_size_inches(figSize)
        #re-draw canvas
        canvas.draw()

    def FileBrowseDialog(self):
        return QFileDialog.getOpenFileName()

    def SaveDialog(self, defaultName, extensionFilter):
        return str(QFileDialog.getSaveFileName(self,"Choose save location",
                                               defaultName,extensionFilter))
        

    
