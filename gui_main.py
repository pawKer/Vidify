import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize,QThread  
from webbrowser import open
from threading import Timer

PORT = 9999
ROOT_URL = 'http://localhost:{}'.format(PORT)

class FlaskThread(QThread):

    def __init__(self, application):
        QThread.__init__(self)
        self.application = application

    def __del__(self):
        self.wait()

    def run(self):
        self.application.run(port=PORT)

class VidifyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(240, 120))    
        self.setWindowTitle("Vidify Web") 

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout()     
        centralWidget.setLayout(gridLayout)  

        title = QLabel("Vidify Web is now running. A new tab will be opened in your browser!", self) 
        title.setAlignment(QtCore.Qt.AlignCenter) 
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)

        stopInst = QLabel("To stop the app just close this window.", self) 
        stopInst.setAlignment(QtCore.Qt.AlignCenter) 

        gridLayout.addWidget(title, 0, 0)
        gridLayout.addWidget(stopInst, 1, 0)
        self.show()

if __name__ == '__main__':
    from server import app as flaskServer
    webapp = FlaskThread(flaskServer)
    webapp.start()

    Timer(5, open, args=[ROOT_URL]).start()

    qtApp = QApplication(sys.argv)
    mainWin = VidifyWindow()

    sys.exit(qtApp.exec_())