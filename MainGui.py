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

        
        self.statusBar()

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.extractAction)
        

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


        

class HomeWidget(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)      
        
        HomeWidget.pause = False

    #ROVER LAT LONG CODE
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

    #BASE STATION CODE
        self.baseLatLabel = QtGui.QLabel("Base Latitude", self)
        self.baseLatLabel.hide()
        self.baseLongLabel = QtGui.QLabel("Base Longitude", self)
        self.baseLongLabel.hide()
        self.baseLatEdit = QtGui.QLineEdit(self)
        self.baseLatEdit.hide()
        self.baseLatEdit.setReadOnly(True)
        self.baseLongEdit = QtGui.QLineEdit(self)
        self.baseLongEdit.hide()
        self.baseLongEdit.setReadOnly(True)

    #GPS TIME CODE
      # self.timeLabel = QtGui.QLabel("GPS TOW", self) #added GPS Time of Week label JM
      # self.GPSWeekLabel = QtGui.QLabel("GPS Week", self) #added GPS Week label
      # self.timeEdit = QtGui.QLineEdit(self) #added timeEdit for displaying GPS Time of Week JM
      # self.timeEdit.setReadOnly(True) #set to read only to display the time from the swift RTK JM
      # self.GPSWeekEdit = QtGui.QLineEdit(self) #added GPSWeekEdit for displaying GPS Week JM
      # self.GPSWeekEdit.setReadOnly(True) #set to read only to display the GPS Week from the swift RTK JM

    #UTC TIME CODE
        self.yearLabel = QtGui.QLabel("Year", self) #added year label for UTC time
        self.yearLabel.hide() #hides the yearLabel on GUI startup
        self.monthLabel = QtGui.QLabel("Month", self) #added month label for UTC time
        self.monthLabel.hide()#hides the yearLabel on GUI startup
        self.dayLabel = QtGui.QLabel("Day", self) #added day label for UTC time
        self.dayLabel.hide()#hides the dayLabel on GUI startup
        self.hoursLabel = QtGui.QLabel("Hours", self) #added hours label for UTC time
        self.hoursLabel.hide()#hides the hoursLabel on GUI startup
        self.minutesLabel = QtGui.QLabel("Minutes", self) #added minutes label for UTC time
        self.minutesLabel.hide()#hides the minutesLabel on GUI startup
        self.secondsLabel = QtGui.QLabel("Seconds", self) #added Seconds label for UTC time
        self.secondsLabel.hide()#hides the secondsrLabel on GUI startup
        self.nanoLabel = QtGui.QLabel("Nanoseconds", self) #added nanoseconds label for UTC timne
        self.nanoLabel.hide()#hides the nanoLabel on GUI startup
        self.yearEdit = QtGui.QLineEdit(self)
        self.yearEdit.setReadOnly(True)
        self.yearEdit.hide() #hides the yearEdit on GUI startup
        self.monthEdit = QtGui.QLineEdit(self)
        self.monthEdit.setReadOnly(True)
        self.monthEdit.hide()#hides the monthEdit on GUI startup
        self.dayEdit = QtGui.QLineEdit(self)
        self.dayEdit.setReadOnly(True)
        self.dayEdit.hide()#hides the dayEdit on GUI startup
        self.hoursEdit = QtGui.QLineEdit(self)
        self.hoursEdit.setReadOnly(True)
        self.hoursEdit.hide()#hides the hoursEdit on GUI startup
        self.minutesEdit = QtGui.QLineEdit(self)
        self.minutesEdit.setReadOnly(True)
        self.minutesEdit.hide()#hides the minutesEdit on GUI startup
        self.secondsEdit = QtGui.QLineEdit(self)
        self.secondsEdit.setReadOnly(True)
        self.secondsEdit.hide()#hides the secondsEdit on GUI startup
        self.nanoEdit = QtGui.QLineEdit(self)
        self.nanoEdit.setReadOnly(True)
        self.nanoEdit.hide()#hides the nanoEdit on GUI startup
        



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

        #check boxes for added/subtracted functionality
        #check box for Coordinated Universatl Time (UTC)
        self.timeCheckBox = QtGui.QCheckBox('UTC Time', self)
        self.timeCheckBox.stateChanged.connect(self.time_check)

        #check box for base station lat long display
        self.baseCheckBox = QtGui.QCheckBox('Base GPS', self)
        self.baseCheckBox.stateChanged.connect(self.base_check)


        #initialization of layout for a uniform GUI look
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        #Dimensional layout of labels and edits for a uniform GUI
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
        grid.addWidget(self.baseLatLabel, 3, 2)
        grid.addWidget(self.baseLatEdit, 3, 3)
        #grid.addWidget(self.GPSWeekLabel, 3, 2) #added to display time functionality on main gui window JM
        #grid.addWidget(self.GPSWeekEdit, 3, 3)  #added to display time functionality on main gui window JM                         
        grid.addWidget(self.fixLabel, 4, 0)
        grid.addWidget(self.fixEdit, 4, 1)
        grid.addWidget(self.baseLongLabel, 4, 2)
        grid.addWidget(self.baseLongEdit, 4, 3)
        #grid.addWidget(self.timeLabel, 4, 2) #added to display time functionality on main gui window JM
        #grid.addWidget(self.timeEdit, 4, 3)  #added to display time functionality on main gui window JM    
        grid.addWidget(self.logLabel, 5, 0)
        grid.addWidget(self.logEdit, 5, 1)
        grid.addWidget(self.lBtn, 5, 2)
        grid.addWidget(self.timeCheckBox, 6, 0)
        grid.addWidget(self.baseCheckBox, 6, 1)
        grid.addWidget(self.qBtn, 7, 0)
        grid.addWidget(self.rBtn, 7, 1)
        grid.addWidget(self.pBtn,7,2)
    #Grid layout for the UTC TIME
        grid.addWidget(self.yearLabel, 1, 4)
        grid.addWidget(self.yearEdit, 1, 5)
        grid.addWidget(self.monthLabel, 2, 4)
        grid.addWidget(self.monthEdit, 2, 5)
        grid.addWidget(self.dayLabel, 3, 4)
        grid.addWidget(self.dayEdit, 3, 5)
        grid.addWidget(self.hoursLabel, 1, 6)
        grid.addWidget(self.hoursEdit, 1, 7)
        grid.addWidget(self.minutesLabel, 2, 6)
        grid.addWidget(self.minutesEdit, 2, 7)
        grid.addWidget(self.secondsLabel, 3, 6)
        grid.addWidget(self.secondsEdit, 3, 7)
        grid.addWidget(self.nanoLabel, 4, 6)
        grid.addWidget(self.nanoEdit, 4, 7)


    #time_check is used to toggle the appearance of the gui
    #this allows the user the option of diplaying the time in UTC format
    def time_check(self, state):
        if state == QtCore.Qt.Checked:
            self.yearLabel.show()
            self.monthLabel.show()
            self.dayLabel.show()
            self.hoursLabel.show()
            self.minutesLabel.show()
            self.secondsLabel.show()
            self.nanoLabel.show()
            self.yearEdit.show()
            self.monthEdit.show()
            self.dayEdit.show()
            self.hoursEdit.show()
            self.minutesEdit.show()
            self.secondsEdit.show()
            self.nanoEdit.show()
            
        else:
            self.yearLabel.hide()
            self.monthLabel.hide()
            self.dayLabel.hide()
            self.hoursLabel.hide()
            self.minutesLabel.hide()
            self.secondsLabel.hide()
            self.nanoLabel.hide()
            self.yearEdit.hide()
            self.monthEdit.hide()
            self.dayEdit.hide()
            self.hoursEdit.hide()
            self.minutesEdit.hide()
            self.secondsEdit.hide()
            self.nanoEdit.hide()
            
    def base_check(self, state):
        if state == QtCore.Qt.Checked:
            self.baseLatLabel.show()
            self.baseLatEdit.show()
            self.baseLongLabel.show()
            self.baseLongEdit.show()
        else:
            self.baseLatLabel.hide()
            self.baseLatEdit.hide()
            self.baseLongLabel.hide()
            self.baseLongEdit.hide()

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

        #Use SBP built in callback function to create callback for GPS Time messages JM
        #source.add_callback(self.GPSTime, SBP_MSG_GPS_TIME)


        #Use SBP built in callback function to create callback for UTC Time messages JM
        source.add_callback(self.UTCTime, SBP_MSG_UTC_TIME)

        #Use SBP built in callback function to create callback for Base posLLH messages
        source.add_callback(self.baseLLH, SBP_MSG_BASE_POS_LLH)
 
        source.start()

    #function is used to return the time being read from the callback messages for UTC time
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!THERE IS A HARDCODED VARIABLE FOR SETTING THE TIME TO PACIFIC STANDARD FROM UTC BE AWARE OF THIS BEFORE TESTING!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def UTCTime(self, msg, **metadata):
        if HomeWidget.pause == False:
            
            #update the fields everytime a UTC time message is recieved JM
            #need to account for the time zone difference between UTC and current
            #location. UTC is +7 ahead of Pacific Time
            timeChange = msg.hours - 7
            self.yearEdit.setText(str(msg.year))
            self.monthEdit.setText(str(msg.month))
            self.dayEdit.setText(str(msg.day))
            self.hoursEdit.setText(str(timeChange))
            #self.hoursEdit.setText(str(msg.hours))
            self.minutesEdit.setText(str(msg.minutes))
            self.secondsEdit.setText(str(msg.seconds))
            self.nanoEdit.setText(str(msg.ns))

    #function is used to return the time read from the callback messages for GPS time
    #currently not implemented as of 08/07/2018
    def GPSTime(self, msg, **metadata):
        if HomeWidget.pause == False:

            #update the fields everytime a GPS Time message is recieved JM
            day = msg.tow/7
            hour = day/24
            minute = hour/60
            second = minute/60

            
            self.GPSWeekEdit.setText(str(msg.wn))
            self.timeEdit.setText(str(msg.tow))

    #function is used to display the current LLH of the base unit
    def baseLLH(self, msg, **metadata):

        if HomeWidget.pause == False:

        #update the fields everytime a posLLH message is recieved
            self.baseLatEdit.setText(str(msg.lat))
            self.baselongEdit.setText(str(msg.lon))

        else:
            pass
          

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
        time = self.timeEdit.text()

        log = now.strftime("%y/%m/%d-%H:%M:%S") + " " + name + " " + lat + " " + lon + " " + height + " " + time

        with open(self.logFile, "a") as file:
            file.write(log +chr(10))
	    #self.logEdit.setText(" ")

     

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



