# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface.ui'
#
# Created: Sun Aug 10 13:49:05 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LogPlot(object):
    def setupUi(self, LogPlot):
        LogPlot.setObjectName(_fromUtf8("LogPlot"))
        LogPlot.resize(867, 637)
        self.centralwidget = QtGui.QWidget(LogPlot)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.upload = QtGui.QWidget()
        self.upload.setObjectName(_fromUtf8("upload"))
        self.gridLayout_3 = QtGui.QGridLayout(self.upload)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.filePath = QtGui.QLineEdit(self.upload)
        self.filePath.setObjectName(_fromUtf8("filePath"))
        self.gridLayout_3.addWidget(self.filePath, 0, 0, 1, 1)
        self.FileBrowseButton = QtGui.QPushButton(self.upload)
        self.FileBrowseButton.setObjectName(_fromUtf8("FileBrowseButton"))
        self.gridLayout_3.addWidget(self.FileBrowseButton, 0, 1, 1, 1)
        self.RecordButton = QtGui.QPushButton(self.upload)
        self.RecordButton.setObjectName(_fromUtf8("RecordButton"))
        self.gridLayout_3.addWidget(self.RecordButton, 0, 2, 1, 1)
        self.uploadLayout = QtGui.QGridLayout()
        self.uploadLayout.setObjectName(_fromUtf8("uploadLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.upload)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.previewAll = QtGui.QRadioButton(self.groupBox_2)
        self.previewAll.setGeometry(QtCore.QRect(10, 30, 95, 20))
        self.previewAll.setObjectName(_fromUtf8("previewAll"))
        self.previewSummary = QtGui.QRadioButton(self.groupBox_2)
        self.previewSummary.setGeometry(QtCore.QRect(10, 60, 101, 20))
        self.previewSummary.setObjectName(_fromUtf8("previewSummary"))
        self.uploadLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.uploadLayout, 1, 0, 1, 3)
        self.tabWidget.addTab(self.upload, _fromUtf8(""))
        self.plot = QtGui.QWidget()
        self.plot.setObjectName(_fromUtf8("plot"))
        self.gridLayout_5 = QtGui.QGridLayout(self.plot)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label = QtGui.QLabel(self.plot)
        self.label.setMaximumSize(QtCore.QSize(182, 16777215))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.beginDate = QtGui.QDateEdit(self.plot)
        self.beginDate.setObjectName(_fromUtf8("beginDate"))
        self.gridLayout_5.addWidget(self.beginDate, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.plot)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_5.addWidget(self.label_2, 0, 2, 1, 1)
        self.endDate = QtGui.QDateEdit(self.plot)
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.gridLayout_5.addWidget(self.endDate, 0, 3, 1, 1)
        self.plotLayout = QtGui.QGridLayout()
        self.plotLayout.setObjectName(_fromUtf8("plotLayout"))
        self.groupBox = QtGui.QGroupBox(self.plot)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.MinTempCheck = QtGui.QCheckBox(self.groupBox)
        self.MinTempCheck.setGeometry(QtCore.QRect(12, 55, 82, 20))
        self.MinTempCheck.setObjectName(_fromUtf8("MinTempCheck"))
        self.MaxTempCheck = QtGui.QCheckBox(self.groupBox)
        self.MaxTempCheck.setGeometry(QtCore.QRect(12, 28, 85, 20))
        self.MaxTempCheck.setObjectName(_fromUtf8("MaxTempCheck"))
        self.AvgTempCheck = QtGui.QCheckBox(self.groupBox)
        self.AvgTempCheck.setGeometry(QtCore.QRect(12, 82, 83, 20))
        self.AvgTempCheck.setObjectName(_fromUtf8("AvgTempCheck"))
        self.WaterLevelCheck = QtGui.QCheckBox(self.groupBox)
        self.WaterLevelCheck.setGeometry(QtCore.QRect(12, 109, 94, 20))
        self.WaterLevelCheck.setObjectName(_fromUtf8("WaterLevelCheck"))
        self.plotButton = QtGui.QPushButton(self.groupBox)
        self.plotButton.setGeometry(QtCore.QRect(10, 200, 93, 28))
        self.plotButton.setObjectName(_fromUtf8("plotButton"))
        self.plotLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.plotLayout, 1, 0, 1, 4)
        self.tabWidget.addTab(self.plot, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        LogPlot.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(LogPlot)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 867, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        LogPlot.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(LogPlot)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        LogPlot.setStatusBar(self.statusbar)
        self.action_Open = QtGui.QAction(LogPlot)
        self.action_Open.setObjectName(_fromUtf8("action_Open"))
        self.action_Quit = QtGui.QAction(LogPlot)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.menu_File.addAction(self.action_Quit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(LogPlot)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(LogPlot)

    def retranslateUi(self, LogPlot):
        LogPlot.setWindowTitle(_translate("LogPlot", "LogPlot", None))
        self.filePath.setPlaceholderText(_translate("LogPlot", "Path to .csv file", None))
        self.FileBrowseButton.setText(_translate("LogPlot", "Browse...", None))
        self.RecordButton.setText(_translate("LogPlot", "Add to Database", None))
        self.groupBox_2.setTitle(_translate("LogPlot", "Data Plot Preview", None))
        self.previewAll.setText(_translate("LogPlot", "All Records", None))
        self.previewSummary.setText(_translate("LogPlot", "Summary", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.upload), _translate("LogPlot", "Upload", None))
        self.label.setText(_translate("LogPlot", "Begin Date", None))
        self.label_2.setText(_translate("LogPlot", "End Date", None))
        self.groupBox.setTitle(_translate("LogPlot", "Parameters to Plot:", None))
        self.MinTempCheck.setText(_translate("LogPlot", "Min Temp", None))
        self.MaxTempCheck.setText(_translate("LogPlot", "Max Temp", None))
        self.AvgTempCheck.setText(_translate("LogPlot", "Avg Temp", None))
        self.WaterLevelCheck.setText(_translate("LogPlot", "Water Level", None))
        self.plotButton.setText(_translate("LogPlot", "Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plot), _translate("LogPlot", "Plot", None))
        self.menu_File.setTitle(_translate("LogPlot", "&File", None))
        self.action_Open.setText(_translate("LogPlot", "&Open...", None))
        self.action_Quit.setText(_translate("LogPlot", "&Quit", None))

