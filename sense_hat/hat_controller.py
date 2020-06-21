from PyQt5.QtWidgets import *
from PyQt5.uic import * 
from PyQt5.QtCore import * 
from PyQt5 import QtSql
from sense_hat import SenseHat

temp = ""
sense = SenseHat()
   
class MyApp(QMainWindow): 
    def __init__(self):
        super().__init__() 
        #loadUi("project.ui", self)
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL') 
        self.db.setHostName("3.34.124.67") 
        self.db.setDatabaseName("15_11") 
        self.db.setUserName("15_11") 
        self.db.setPassword("1234")
        ok = self.db.open() 
        self.query = QtSql.QSqlQuery("select * from command2");
        print(ok)
        

    def commandQuery(self,cmd,arg):
        
        self.query.prepare("insert into command2 (time, cmd_string, arg_string, is_finish) values(:time, :cmd, :arg, :finish)");
        time = QDateTime().currentDateTime() 
        self.query.bindValue(":time", time) 
        self.query.bindValue(":cmd", cmd) 
        self.query.bindValue(":arg", arg) 
        self.query.bindValue(":finish", 0) 
        self.query.exec()
    
    def right(self):
        print("right")
        self.commandQuery("right","1 sec")
    def left(self):
        print("left")
        self.commandQuery("left","1 sec")
    def go(self):
        print("go")
        print(self.__class__.__name__)
        self.commandQuery("go","1 sec")
    def stop(self):
        print("stop")
        self.commandQuery("stop","1 sec")
    def mid(self):
        print("mid")
        self.commandQuery("mid","1 sec")
    def back(self):
        print("back")
        self.commandQuery("back","1 sec")
    def horn(self):
        print("horn")
        self.commandQuery("horn","1 sec")
        

sense.clear()
app = QApplication([]) 
win = MyApp() 

def sense_up(self):
    sense.clear()
    for i in range (0, 8) :
        sense.set_pixel(3, i, 0, 150, 150)
        sense.set_pixel(4, i, 0, 150, 150)
    for i in range (2, 6) :
        sense.set_pixel(i, 1, 0, 150, 150)
    for i in range (1, 7) :
        sense.set_pixel(i, 2, 0, 150, 150)
    win.go()
def sense_down(self):
    sense.clear()
    for i in range (0, 8) :
        sense.set_pixel(3, i, 0, 150, 150)
        sense.set_pixel(4, i, 0, 150, 150)
    for i in range (2, 6) :
        sense.set_pixel(i, 6, 0, 150, 150)
    for i in range (1, 7) :
        sense.set_pixel(i, 5, 0, 150, 150)
    win.back()
def sense_left(self):
    sense.clear()
    for i in range (0, 8) :
        sense.set_pixel(i, 3, 0, 150, 150)
        sense.set_pixel(i, 4, 0, 150, 150)
    for i in range (2, 6) :
        sense.set_pixel(1, i, 0, 150, 150)
    for i in range (1, 7) :
        sense.set_pixel(2, i, 0, 150, 150)
    win.left()
def sense_right(self):
    sense.clear()
    for i in range (0, 8) :
        sense.set_pixel(i, 3, 0, 150, 150)
        sense.set_pixel(i, 4, 0, 150, 150)
    for i in range (2, 6) :
        sense.set_pixel(6, i, 0, 150, 150)
    for i in range (1, 7) :
        sense.set_pixel(5, i, 0, 150, 150)
    win.right()
def sense_push(self):
    sense.clear()
    for i in range (1,7) :
        sense.set_pixel(i, i, 150, 0, 0)
        sense.set_pixel(7-i, i, 150, 0, 0)
    for i in range (2,6) :
        sense.set_pixel(i, 0, 150, 0, 0)
        sense.set_pixel(i, 7, 150, 0, 0)
        sense.set_pixel(0, i, 150, 0, 0)
        sense.set_pixel(7, i, 150, 0, 0)
    win.stop()
    win.mid()

    
sense.stick.direction_up = sense_up
sense.stick.direction_down = sense_down
sense.stick.direction_left = sense_left
sense.stick.direction_right = sense_right
sense.stick.direction_middle = sense_push

win.show() 
app.exec()
