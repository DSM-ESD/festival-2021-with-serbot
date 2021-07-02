from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import *
import sys
import platform
import requests
import socket

reset_url = "http://127.0.0.1:5000/reset"
get_password_url = "http://127.0.0.1:5000/password"

class Main(QLabel):
    def __init__(self) :
        super().__init__()
        
        self.ui()
        self.showFullScreen()
        self.setStyleSheet("background-color: white;")

    def reset_request(self):
        requests.get(reset_url)

    def password_request(self):
        password = requests.get(get_password_url).text
        return password

    def change_label_text(self):
        name = platform.node()
        password = self.password_request()
        self.setText(f"<h1>{name}</h1><h3>{password}</h3>")
    
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
       self.reset_request()
       self.change_label_text()
       return super().mousePressEvent(a0)

    def ui(self):
        name = platform.node()
        password = self.password_request()
        print(password)
        self.setText(f"<h1>{name}</h1><h3>{password}</h3>")
        '''
        x = self.width()
        y = self.height()

        n = x - y
        
        if n < 100:
            self.setFont(QtGui.QFont("궁서", n))
        else :
            b = n/10
            self.setFont(QtGui.QFont("궁서", b + 30))
        '''

        self.setFont(QtGui.QFont("Arial", 100))


        self.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        
        self.setWindowTitle(name)


if __name__ == "__main__" :
    print(socket.gethostbyname(socket.gethostname()))
    app = QApplication(sys.argv)
    main = Main()
    #main.show()


    app.exec_()
