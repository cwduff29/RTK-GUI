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
        
        self.setGeometry(50, 50, 700, 400)
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

#Functionallity to settings menu_RL
        self.windowsizeAction1 = QtGui.QAction("&Enlarge Window", self, checkable=True)
        self.windowsizeAction1.setStatusTip('Enlarge Window Size')
        self.windowsizeAction1.triggered.connect(self.enlargewindow_application)
        self.windowsizeAction2 = QtGui.QAction("&Minimize Window", self, checkable=True)
        self.windowsizeAction2.setStatusTip('Reduce Window Size')
        self.windowsizeAction2.triggered.connect(self.reducewindow_application)
        self.fontsizeAction1 = QtGui.QAction("&Large Font", self, checkable=True)
        self.fontsizeAction1.setStatusTip('Large Font Size')
        self.fontsizeAction1.triggered.connect(self.largefont_application)
        self.fontsizeAction2 = QtGui.QAction("&Medium Font", self, checkable=True)
        self.fontsizeAction2.setStatusTip('Medium Font Size')
        self.fontsizeAction2.triggered.connect(self.mediumfont_application)
        self.fontsizeAction3 = QtGui.QAction("&Small Font", self, checkable=True)
        self.fontsizeAction3.setStatusTip('Small Font Size')
        self.fontsizeAction3.triggered.connect(self.smallfont_application)
#end my test_RL
        
        self.statusBar()

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.extractAction)
#Add settings option to settings menu_RL
        self.settingsMenu = self.menuBar()
        self.settingsMenu = self.mainMenu.addMenu('&Settings')
        self.windowsize = self.settingsMenu.addMenu("&Window Size")
        self.fontsize = self.settingsMenu.addMenu("&Font Size")
        self.windowsize.addAction(self.windowsizeAction1)
        self.windowsize.addAction(self.windowsizeAction2)
        self.fontsize.addAction(self.fontsizeAction1)
        self.fontsize.addAction(self.fontsizeAction2)
        self.fontsize.addAction(self.fontsizeAction3)
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

        ports = ("/dev/ttyUSB0", "/dev/ttyAMA0")
        
        port, ok = QtGui.QInputDialog.getItem(self, "Input Port", "Enter Port\nDefault /dev/ttyUSB0", ports)
        
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

#Window Size_RL
    def enlargewindow_application(self):
        if self.windowsizeAction1.isChecked():
            self.windowsizeAction2.setChecked(False)
            self.setGeometry(50, 50, 800, 500)
        else:
            self.setGeometry(50, 50, 700, 400)

    def reducewindow_application(self):
        if self.windowsizeAction2.isChecked():
            self.windowsizeAction1.setChecked(False)
            self.setGeometry(50, 50, 500, 300)
        else:
            self.setGeometry(50, 50, 700, 400)
#end my test_RL
#Font Size_RL
    def largefont_application(self):
        if self.fontsizeAction1.isChecked():
            self.fontsizeAction2.setChecked(False)
            self.fontsizeAction3.setChecked(False)
            self.setStyleSheet("font: 20pt")
        else:
            self.setStyleSheet("font: 15pt")

    def mediumfont_application(self):
        if self.fontsizeAction2.isChecked():
            self.fontsizeAction1.setChecked(False)
            self.fontsizeAction3.setChecked(False)
            self.setStyleSheet("font: 16pt")
        else:
            self.setStyleSheet("font:15pt")

    def smallfont_application(self):
        if self.fontsizeAction3.isChecked():
            self.fontsizeAction1.setChecked(False)
            self.fontsizeAction2.setChecked(False)
            self.setStyleSheet("font: 12pt")
        else:
            self.setStyleSheet("font: 15pt")
        

class HomeWidget(QtGui.QWidget):
    
    def __init__(self, *args):
        
        self.marker = False
        self.lat_choice = 1
        self.long_choice = 1
        self.height_choice = 1
        
        QtGui.QWidget.__init__(self, *args)      
        
        HomeWidget.pause = False

        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        
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

#Show and log data_RL
        self.latCheckBox = QtGui.QCheckBox('Latitude', self)
        self.latCheckBox.setChecked(True)
        self.latCheckBox.stateChanged.connect(self.lat_check)
        self.longCheckBox = QtGui.QCheckBox('Longitude', self)
        self.longCheckBox.setChecked(True)
        self.longCheckBox.stateChanged.connect(self.long_check)
        self.heightCheckBox = QtGui.QCheckBox('Height', self)
        self.heightCheckBox.setChecked(True)
        self.heightCheckBox.stateChanged.connect(self.height_check)
        self.fixCheckBox = QtGui.QCheckBox('GPS Fix Type', self)
        self.fixCheckBox.setChecked(True)
        self.fixCheckBox.stateChanged.connect(self.fix_check)
        self.eastCheckBox = QtGui.QCheckBox('Easting', self)
        self.eastCheckBox.setChecked(True)
        self.eastCheckBox.stateChanged.connect(self.east_check)
        self.northCheckBox = QtGui.QCheckBox('Northing', self)
        self.northCheckBox.setChecked(True)
        self.northCheckBox.stateChanged.connect(self.north_check)
#end test_RL
        
        #grid = QtGui.QGridLayout()
        #self.setLayout(grid)
        
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

#Grid Layout for log checkboxes_RL
        grid.addWidget(self.latCheckBox, 7, 0)
        grid.addWidget(self.longCheckBox, 8, 0)
        grid.addWidget(self.heightCheckBox, 9, 0)
        grid.addWidget(self.fixCheckBox, 10, 0)
        grid.addWidget(self.eastCheckBox, 7, 1)
        grid.addWidget(self.northCheckBox, 8, 1)
#end test_RL
#Func for Logging
    def lat_check(self, state):
        if state == QtCore.Qt.Unchecked:
            choice = QtGui.QMessageBox.question(self, "Log Latitude",
                                    "Would you still like to log latitude?",
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.No:
                self.lat_choice = False
                self.latLabel.hide()
                self.latEdit.hide()
            
        elif state == QtCore.Qt.Checked:
            self.lat_choice = True
            self.latLabel.show()
            self.latEdit.show()
        
    def long_check(self, state):
        if state == QtCore.Qt.Unchecked:
            choice = QtGui.QMessageBox.question(self, "Log Longitude",
                                            "Would you still like to log longitude?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.No:
                self.long_choice = False
                self.longLabel.hide()
                self.longEdit.hide()
            
        elif state == QtCore.Qt.Checked:
            self.long_choice = True
            self.longLabel.show()
            self.longEdit.show()

    def height_check(self, state):
        if state == QtCore.Qt.Unchecked:
            choice = QtGui.QMessageBox.question(self, "Log Height",
                                            "Would you still like to log height?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.No:
                self.height_choice = False
                self.heightLabel.hide()
                self.heightEdit.hide()
            
        elif state == QtCore.Qt.Checked:
            self.height_choice = True
            self.heightLabel.show()
            self.heightEdit.show()

    def fix_check(self, state):
        if state == QtCore.Qt.Unchecked:
            self.fixLabel.hide()
            self.fixEdit.hide()
        else:
            self.fixLabel.show()
            self.fixEdit.show()

    def east_check(self, state):
        if state == QtCore.Qt.Unchecked:
            self.eastLabel.hide()
            self.eastEdit.hide()
        else:
            self.eastLabel.show()
            self.eastEdit.show()

    def north_check(self, state):
        if state == QtCore.Qt.Unchecked:
            self.northLabel.hide()
            self.northEdit.hide()
        else:
            self.northLabel.show()
            self.northEdit.show()
#end test_RL

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

        self.rBtn.setDisabled(True)


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
       
        if self.lat_choice == False:
            lat = " "*(len(lat))
        elif self.lat_choice == True:
            lat = self.latEdit.text()
        
        if self.long_choice == False:
            lon = " "*(len(lon))
        elif self.long_choice == True:
            lon = self.longEdit.text()
        
        if self.height_choice == False:
            height = " "*(len(height))
        elif self.height_choice == True:
            height = self.heightEdit.text()
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!! DO NOT NAME LOG FILES LONGER THAN 25 CHARACTERS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        header = (" y /m /d-H: M: S" + " "*2 + "name" + 21*" " + "latitude" + (len(lat)-7)*" " + "longitude" + (len(lon)-8)*" " + "height\n")
        
        log = now.strftime("%y/%m/%d-%H:%M:%S") + " " + name + " "*(25-len(name)) + lat + " " + lon + " " + height

        if len(name) <= 25:
            if self.marker == False:
                with open(self.logFile, "w") as file:
                    file.write(header)
                    file.write(log+chr(10))
                    self.marker = True
            else:
                with open(self.logFile, "a") as file:
                    file.write(log+chr(10))
        else:
           QtGui.QMessageBox.about(self, "Log Error", "Log Name is longer than 25 characters!\n Choose a new name.") 

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()




