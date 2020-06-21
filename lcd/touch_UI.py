from PyQt5.QtWidgets import *
from PyQt5.uic import * 
from PyQt5.QtCore import * 
from PyQt5 import QtSql

temp = ""
class MyApp(QMainWindow): 
    def __init__(self):
        super().__init__() 
        loadUi("project.ui", self)
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL') 
        self.db.setHostName("3.34.124.67") 
        self.db.setDatabaseName("15_11") 
        self.db.setUserName("15_11") 
        self.db.setPassword("1234")
        ok = self.db.open() 
        print(ok)
        
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.pollingQuery)
        self.timer.start()
    
    def pollingQuery(self):
        self.query = QtSql.QSqlQuery("select * from command2 order by time desc limit 15");
        global temp
        temp_str=""
        while (self.query.next()): 
            self.record = self.query.record()
            str = "%s | %10s | %10s | %4d" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
            temp_str=temp_str+str+"\n"
        if(temp!=temp_str):
            self.text.setPlainText(temp_str)
            temp=temp_str

        #sensing log
        self.query = QtSql.QSqlQuery("select * from sensing2 order by time desc limit 15");        
        str = ""
        while (self.query.next()):
            self.record = self.query.record()
            str += "%s | %10s | %10s | %10s\n" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
        self.text2.setPlainText(str)

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
    def mute(self):
        print("mute")
        self.commandQuery("mute","1 sec")
app = QApplication([]) 
win = MyApp() 
win.show() 
app.exec()
