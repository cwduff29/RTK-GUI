import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("RTK GPS Application")
        self.setWindowIcon(QtGui.QIcon('gpslogo.png'))

        extractAction = QtGui.QAction("&Quit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Exit the Application')
        extractAction.triggered.connect(self.close_application)

        prefAction = QtGui.QAction("&Preferences..", self)
        prefAction.setShortcut("Ctrl+P")
        prefAction.setStatusTip('Edit Application Preferences')
        prefAction.triggered.connect(self.edit_application)

        aboutAction = QtGui.QAction("&About", self)
        aboutAction.setStatusTip('About the Application')
        aboutAction.triggered.connect(self.about_application)
        
        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(prefAction)
        editMenu = mainMenu.addMenu('&Help')
        editMenu.addAction(aboutAction)
        
        self.home()

    def home(self):
        btn = QtGui.QPushButton("Run", self)
        btn.clicked.connect(self.start_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(0,100)

        commAction = QtGui.QAction(QtGui.QIcon('comport.png'), 'Select Comm Port', self)
        commAction.triggered.connect(self.comm_settings)
        logAction = QtGui.QAction(QtGui.QIcon('file.png'), 'Select Log File Directory', self)
        logAction.triggered.connect(self.log_settings)
        
        self.toolBar = self.addToolBar("Comm")
        self.toolBar.addAction(commAction)
        self.toolBar.addAction(logAction)

        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        
        self.show()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Quit",
                                            "Are you sure you want to quit?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def about_application(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")

    def comm_settings(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")

    def log_settings(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")

    def edit_application(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")

    def start_application(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()
