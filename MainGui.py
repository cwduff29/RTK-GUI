import sys
from PyQt4 import QtGui, QtCore
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.client.loggers.json_logger import JSONLogger
from sbp.system import *
from sbp.settings import *
from sbp.navigation import *
from sbp.observation import *
import argparse
import time
import csv

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.home = HomeWidget(self)
        self.setCentralWidget(self.home)
        
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("RTK GPS Application")
        self.setWindowIcon(QtGui.QIcon('gpslogo.png'))

        self.extractAction = QtGui.QAction("&Quit", self)
        self.extractAction.setShortcut("Ctrl+Q")
        self.extractAction.setStatusTip('Exit the Application')
        self.extractAction.triggered.connect(self.close_application)

        self.prefAction = QtGui.QAction("&Preferences..", self)
        self.prefAction.setShortcut("Ctrl+P")
        self.prefAction.setStatusTip('Edit Application Preferences')
        self.prefAction.triggered.connect(self.edit_application)

        self.aboutAction = QtGui.QAction("&About", self)
        self.aboutAction.setStatusTip('About the Application')
        self.aboutAction.triggered.connect(self.about_application)
        
        self.statusBar()

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.extractAction)
        self.editMenu = self.mainMenu.addMenu('&Edit')
        self.editMenu.addAction(self.prefAction)
        self.editMenu = self.mainMenu.addMenu('&Help')
        self.editMenu.addAction(self.aboutAction)

        self.commAction = QtGui.QAction(QtGui.QIcon('comport.png'), 'Select Comm Port', self)
        self.port = self.commAction.triggered.connect(self.comm_settings)
        self.logAction = QtGui.QAction(QtGui.QIcon('file.png'), 'Select Log File Directory', self)
        self.logAction.triggered.connect(self.log_settings)
        
        self.toolBar = self.addToolBar("Comm")
        self.toolBar.addAction(self.commAction)
        self.toolBar.addAction(self.logAction)
        
        self.show()
        

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Quit", "Are you sure you want to quit?",
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def comm_settings(self):
        self.port, ok = QtGui.QInputDialog.getText(self, "Input Port", "Enter Port\nDefault /dev/ttyUSB0")
        print(self.port)

    def log_settings(self):
        logFile = QtGui.QInputDialog.getText(self, "Input File Name", "Enter Log File Name")
        print(self.port)

    def about_application(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")

    def edit_application(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")


class HomeWidget(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)      
        
        self.latLabel = QtGui.QLabel("Latitude", self)
        self.longLabel = QtGui.QLabel("Longitude", self)
        self.heightLabel = QtGui.QLabel("Height", self)
        self.fixLabel = QtGui.QLabel("GPS Fix Type", self)

        self.latEdit = QtGui.QLineEdit(self)
        self.latEdit.setReadOnly(True)
        self.longEdit = QtGui.QLineEdit(self)
        self.longEdit.setReadOnly(True)
        self.heightEdit = QtGui.QLineEdit(self)
        self.heightEdit.setReadOnly(True)
        self.fixEdit = QtGui.QLineEdit(self)
        self.fixEdit.setReadOnly(True)

        self.qBtn = QtGui.QPushButton("Quit", self)
        self.qBtn.clicked.connect(self.close_application)
        self.qBtn.resize(self.qBtn.minimumSizeHint())

        self.rBtn = QtGui.QPushButton("Run", self)
        self.rBtn.clicked.connect(self.run_application)
        self.rBtn.resize(self.rBtn.minimumSizeHint())
        
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        
        grid.addWidget(self.latLabel, 1, 0)
        grid.addWidget(self.latEdit, 1, 1)
        grid.addWidget(self.longLabel, 2, 0)
        grid.addWidget(self.longEdit, 2, 1)
        grid.addWidget(self.heightLabel, 3, 0)
        grid.addWidget(self.heightEdit, 3, 1)
        grid.addWidget(self.fixLabel, 4, 0)
        grid.addWidget(self.fixEdit, 4, 1)
        grid.addWidget(self.qBtn, 5, 0)
        grid.addWidget(self.rBtn, 5, 1)


    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Quit",
                                    "Are you sure you want to quit?",
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def run_application(self):
        DEFAULT_LOG_FILENAME=time.strftime("sbp-%Y%m%d-%H%M%S.log")
        w=Window.__init__
        attrs = vars(w)
        print(attrs)
        parser = argparse.ArgumentParser(
        description="Swift Navigation SBP Example.")
        parser.add_argument(
            "-p",
            "--port",
            default=['/dev/ttyUSB0'],
            nargs=1,
            help="specify the serial port to use.")
        parser.add_argument(
            "-b",
            "--baud",
            default=[115200],
            nargs=1,
            help="specify the baud rate")
        parser.add_argument(
            "-f",
            "--filename",
            default=[DEFAULT_LOG_FILENAME],
            nargs=1,
            help="specify the name of the log file")
        args = parser.parse_args()

        # Open a connection to Piksi using the default baud rate (115200) and port (/dev/ttyUSB0
        driver = PySerialDriver(args.port[0], args.baud[0])
        source = Handler(Framer(driver.read, None, verbose=True))
                         
        # Use SBP built in callback function to create callback for posLLH messages
        source.add_callback(self.posLLH, SBP_MSG_POS_LLH)
        #source.add_callback(baselineCallback, SBP_MSG_BASELINE_NED)
        source.start()


    def posLLH(self, msg, **metadata):

        #update the feilds everytime a posLLH message is recieved
        self.latEdit.setText(str(msg.lat))
        self.longEdit.setText(str(msg.lon)) 
        self.heightEdit.setText(str(msg.height))
        self.fixEdit.setText(str(msg.flags))

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



