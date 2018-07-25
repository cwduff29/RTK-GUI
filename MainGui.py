import sys
from PyQt4 import QtGui, QtCore
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.client.loggers.json_logger import JSONLogger
from sbp.system import *
from sbp.settings import *
from sbp.navigation import *
from sbp.observation import *
import time
import datetime
import csv
import utm

DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_LOG_FILE = time.strftime("GPS_Log-%Y%m%d-%H%M%S.log")


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        Window.port = DEFAULT_PORT
        Window.logFile = DEFAULT_LOG_FILE
        
        self.setGeometry(50, 50, 800, 500)
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

#My test_RL
        self.testingAction = QtGui.QAction("&Test", self)
        self.testingAction.setStatusTip('I am testing this')
        self.testingAction.triggered.connect(self.testing_application) #I'm going to need to hook it up to something_RL
#end my test_RL
        
        self.statusBar()

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.extractAction)
#My test_RL
        self.testMenu = self.menuBar()
        self.testMenu = self.mainMenu.addMenu('&TestThis')
        self.testMenu.addAction(self.testingAction)
#end my test
        
        self.editMenu = self.mainMenu.addMenu('&Edit')
        self.editMenu.addAction(self.prefAction)
        self.editMenu = self.mainMenu.addMenu('&Help')
        self.editMenu.addAction(self.aboutAction)

        self.commAction = QtGui.QAction(QtGui.QIcon('comport.png'), 'Select Comm Port', self)
        self.commAction.triggered.connect(self.comm_settings)
        self.logAction = QtGui.QAction(QtGui.QIcon('file.png'), 'Select Log File Directory', self)
        self.logAction.triggered.connect(self.log_settings)
        
        self.toolBar = self.addToolBar("Comm")
        self.toolBar.addAction(self.commAction)
        self.toolBar.addAction(self.logAction)
        #Starts Widgets
        self.home = HomeWidget(self)
        self.setCentralWidget(self.home)
        self.show()
      

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Quit", "Are you sure you want to quit?",
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def comm_settings(self):
        
        port, ok = QtGui.QInputDialog.getText(self, "Input Port", "Enter Port\nDefault /dev/ttyUSB0")
        
        if ok and str(port):
            Window.port = port
    

    def log_settings(self):
        
        logFile, ok = QtGui.QInputDialog.getText(self, "Input File Name", "Enter Log File Name")

        if ok and str(port):
            Window.logFile = logFile
       

    def about_application(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")

    def edit_application(self):
        about = QtGui.QMessageBox.about(self, "About", "RTK GPS Application\nVersion 1.0\nChristopher Duff")

#My test_RL
    def testing_application(self):
        test = QtGui.QMessageBox.about(self, "Testing", "Hey Check this out") #Look up "about" function_RL
#end my test_RL
        

class HomeWidget(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)      
        
        HomeWidget.pause = False
        
        self.latLabel = QtGui.QLabel("Latitude", self)
        self.longLabel = QtGui.QLabel("Longitude", self)
        self.heightLabel = QtGui.QLabel("Height", self)
        self.fixLabel = QtGui.QLabel("GPS Fix Type", self)
        self.eastLabel = QtGui.QLabel("Easting", self)
        self.northLabel = QtGui.QLabel("Northing", self)
        self.logLabel = QtGui.QLabel("Monument Name", self)

        self.latEdit = QtGui.QLineEdit(self)
        self.latEdit.setReadOnly(True)
        self.longEdit = QtGui.QLineEdit(self)
        self.longEdit.setReadOnly(True)
        self.heightEdit = QtGui.QLineEdit(self)
        self.heightEdit.setReadOnly(True)
        self.fixEdit = QtGui.QLineEdit(self)
        self.fixEdit.setReadOnly(True)
        self.eastEdit = QtGui.QLineEdit(self)
        self.eastEdit.setReadOnly(True)
        self.northEdit = QtGui.QLineEdit(self)
        self.northEdit.setReadOnly(True)
        self.logEdit = QtGui.QLineEdit(self)
        self.logEdit.setReadOnly(False)

        self.qBtn = QtGui.QPushButton("Quit", self)
        self.qBtn.clicked.connect(self.close_application)
        self.qBtn.resize(self.qBtn.minimumSizeHint())

        self.rBtn = QtGui.QPushButton("Run", self)
        self.rBtn.clicked.connect(self.run_application)
        self.rBtn.resize(self.rBtn.minimumSizeHint())

        self.pBtn = QtGui.QPushButton("Pause", self)
        self.pBtn.clicked.connect(self.pause_application)
        self.pBtn.resize(self.rBtn.minimumSizeHint())

        self.lBtn = QtGui.QPushButton("Log", self)
        self.lBtn.clicked.connect(self.log_application)
        self.lBtn.resize(self.rBtn.minimumSizeHint())
        
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        
        grid.addWidget(self.latLabel, 1, 0)
        grid.addWidget(self.latEdit, 1, 1)
        grid.addWidget(self.longLabel, 2, 0)
        grid.addWidget(self.longEdit, 2, 1)
        grid.addWidget(self.eastLabel, 1, 2)
        grid.addWidget(self.eastEdit, 1, 3)
        grid.addWidget(self.northLabel, 2, 2)
        grid.addWidget(self.northEdit, 2, 3)
        grid.addWidget(self.heightLabel, 3, 0)
        grid.addWidget(self.heightEdit, 3, 1)
        grid.addWidget(self.fixLabel, 4, 0)
        grid.addWidget(self.fixEdit, 4, 1)
        grid.addWidget(self.logLabel, 5, 0)
        grid.addWidget(self.logEdit, 5, 1)
        grid.addWidget(self.lBtn, 5, 2)
        grid.addWidget(self.qBtn, 6, 0)
        grid.addWidget(self.rBtn, 6, 1)
        grid.addWidget(self.pBtn,6,2)


    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Quit",
                                    "Are you sure you want to quit?",
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def pause_application(self):

        if HomeWidget.pause == False:
            HomeWidget.pause = True
            self.pBtn.setText("Unpause")

        else:
            HomeWidget.pause = False
            self.pBtn.setText("Pause")
            

    def run_application(self):
        
        self.port = Window.port
        self.logFile = Window.logFile
        self.buad = 115200

        # Open a connection to Piksi using the default baud rate (115200) and port (/dev/ttyUSB0)
        driver = PySerialDriver(self.port, self.buad)
        source = Handler(Framer(driver.read, None, verbose=True))
                         
        # Use SBP built in callback function to create callback for posLLH messages
        source.add_callback(self.posLLH, SBP_MSG_POS_LLH)
        #source.add_callback(baselineCallback, SBP_MSG_BASELINE_NED)
        source.start()


    def posLLH(self, msg, **metadata):

        if HomeWidget.pause == False:

            #update the fields everytime a posLLH message is recieved
            self.latEdit.setText(str(msg.lat))
            self.longEdit.setText(str(msg.lon)) 
            self.heightEdit.setText(str(msg.height))
        
            if msg.flags == 1:
                self.fixEdit.setText("Single Point Position")
                
            elif msg.flags == 2:
                self.fixEdit.setText("Differential GNSS")

            elif msg.flags == 3:
                self.fixEdit.setText("Float RTK")

            elif msg.flags == 4:
                self.fixEdit.setText("Fixed RTK")

            else:
                self.fixEdit.setText("Invalid")

            conv = utm.from_latlon(msg.lat, msg.lon)
            self.eastEdit.setText(str(conv[0])) 
            self.northEdit.setText(str(conv[1]))

        else:
            pass

    def log_application(self):

        now = datetime.datetime.now()
        name = self.logEdit.text()
        lat = self.latEdit.text()
        lon = self.longEdit.text()
        height = self.heightEdit.text()

        log = now.strftime("%y/%m/%d-%H:%M:%S") + " " + name + " " + lat + " " + lon + " " + height

        with open(self.logFile, "a") as file:
            file.write(log +chr(10))
	    #self.logEdit.setText(" ")

     

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



