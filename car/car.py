import RPi.GPIO as GPIO
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtSql
import time
from Raspi_MotorHAT import Raspi_MotorHAT#, Raspi_DCMotor
from gpiozero import *
from multiprocessing import Process

#motor init!!!
mh = Raspi_MotorHAT(addr=0x6f)
dcMotor = mh.getMotor(3)#
speed = 60 #
dcMotor.setSpeed(speed)
servo = mh._pwm
servo.setPWMFreq(60)
R_limit = 400
L_limit = 300
mid_center = 350
L_itv = L_limit-mid_center
R_itv = R_limit-mid_center

led_r1 = LED(23)
led_r2 = LED(7)
led_l = LED(8)
led_r = LED(24)
led = [led_l, led_r]

led_r1.off()
led_r2.off()
led_l.off()
led_r.off()

GPIO_TRIGGER = 17
GPIO_ECHO = 27
dd= 0

GPIO.setmode(GPIO.BCM)
SPKR = 18
KLX = 12
GPIO.setup(SPKR, GPIO.OUT)
GPIO.setup(KLX, GPIO.OUT)
p = GPIO.PWM(SPKR, 100)
k = GPIO.PWM(KLX, 100)

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.output(GPIO_TRIGGER, False)


notes = [
659, 622, 659, 622, 659, 494,
587, 523, 440, 440, 440, 262,
330, 440, 494, 494, 494, 330,
415, 494, 523, 523, 523, 330,
659, 622, 659, 622, 659, 494,
587, 523, 440, 440, 440, 262,
330, 440, 494, 494, 494, 330,
523, 494, 440, 440, 440, 494,
523, 587, 659, 659, 659, 391,
698, 659, 587, 587, 587, 349,
659, 587, 523, 523, 523, 330,
587, 523, 494, 494, 494, 330
]


print("motor init oK")

print("Waiting For Sensor To Settle");
time.sleep(2)

class MelodyThread(QThread):
  mySignal = pyqtSignal()
  def __init__(self):
    super().__init__()
    self.isRun = False
  
  def run(self):
    print("Melody On")
    p.start(100)
    p.ChangeDutyCycle(90)
    for i in range(len(notes)):
      p.ChangeFrequency(notes[i] *1.7)
      time.sleep(0.3)
      if self.isRun == False :
        break;
    p.stop()

#LED 깜빡이기
class LedThread(QThread):
  mySignal = pyqtSignal(int)
  def __init__(self):
    super().__init__()
    self.dirOn = False
    self.onLed = 0
  
  def run(self):
    print('on : {}   dir : {}'.format(self.dirOn, self.onLed))
    for i in range(len(led)):
      led[i].off()
    if self.dirOn is True :
      while True:
        if self.dirOn is False : 
          break;
        target = led[self.onLed]
        target.on()
        time.sleep(0.5)
        target.off()
        time.sleep(0.5)
  
class UwaveThread(QThread):
  mySignal = pyqtSignal()
  def __init__(self):
    super().__init__()
    #self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL', 'sensingDB')
    # self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    # self.db.setHostName("3.34.124.67")
    # self.db.setDatabaseName("15_11")
    # self.db.setUserName("15_11")
    # self.db.setPassword("1234")
    # ok = self.db.open()
    # print('sensing db ' + str(ok))
    #self.query = QtSql.QSqlQuery("select * from sensing2", db=self.db);
    

  
  def run(self):
    global dd
    while True :
      GPIO.output(GPIO_TRIGGER, True)
      time.sleep(0.00001)
      GPIO.output(GPIO_TRIGGER, False)
      while GPIO.input(GPIO_ECHO) == 0:
          pulse_start = time.time()
          #print('start : {}'.format(pulse_start))

      while GPIO.input(GPIO_ECHO) == 1:
          pulse_end = time.time()
          #print('end : {}'.format(pulse_end))

      pulse_duration = pulse_end - pulse_start
      distance = pulse_duration * 17150
      distance = round(distance, 2)

      #print("Distance:", distance, "cm")
      dd = distance
      # self.query = QtSql.QSqlQuery();
      # self.query.prepare("insert into sensing2 (time, num1, num2, num3, meta_string, is_finish) values (:time, :num1, :num2, :num3, :meta, :finish)");
      # time1 = QDateTime().currentDateTime()
      # self.query.bindValue(":time", time1)
      # self.query.bindValue(":num1", 1)
      # self.query.bindValue(":num2", 0)
      # self.query.bindValue(":num3", 0)
      # self.query.bindValue(":meta", "")
      # self.query.bindValue(":finish", 0)
      # self.query.exec()

      if distance <= 15 : 
        dcMotor.run(Raspi_MotorHAT.RELEASE)
      time.sleep(0.05)
      

class pollingThread(QThread):
  def __init__(self):
    super().__init__()
    self.th = MelodyThread()
    self.th_led = LedThread()
    self.th_uwave = UwaveThread()
    self.th_uwave.start()
    self.th_led.start() 

  def run(self):

    self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    self.db.setHostName("3.34.124.67")
    self.db.setDatabaseName("15_11")
    self.db.setUserName("15_11")
    self.db.setPassword("1234")
    ok = self.db.open()
    print(ok)


    while True :
      time.sleep(0.1)
      self.getQuery()
      self.setQuery()
  # def setQuery(self):
    
    # self.query.bindValue(":time", time)
    # self.query.bindValue(":num1", p)
    # self.query.bindValue(":num2", t)
    # self.query.bindValue(":num3", h)
    # self.query.bindValue(":meta", "")
    # self.query.bindValue(":finish", 0)
    # self.query.exec()

  def setQuery(self):
    global dd
    self.query = QtSql.QSqlQuery();
    self.query.prepare("insert into sensing2 (time, num1, num2, num3, meta_string, is_finish) values (:time, :num1, :num2, :num3, :meta, :finish)");
    time1 = QDateTime().currentDateTime()
    self.query.bindValue(":time", time1)
    self.query.bindValue(":num1", dd)
    self.query.bindValue(":num2", 0)
    self.query.bindValue(":num3", 0)
    self.query.bindValue(":meta", "")
    self.query.bindValue(":finish", 0)
    self.query.exec()

  
  
  def getQuery(self):
    query = QtSql.QSqlQuery("select * from command2 order by time desc limit 1");
    query.next()
    cmdTime = query.record().value(0)
    cmdType = query.record().value(1)
    cmdArg = query.record().value(2)
    is_finish = query.record().value(3)

    if is_finish == 0 :
      #detect new command
      print(cmdTime.toString(), cmdType, cmdArg)

      #update
      query = QtSql.QSqlQuery("update command2 set is_finish=1 where is_finish=0");

      #motor
      if cmdType == "go": self.go()
      if cmdType == "back": self.back()
      if cmdType == "left": self.left()
      if cmdType == "right": self.right()
      if cmdType == "mid": self.mid()
      if cmdType == "stop": self.stop()
      if cmdType == "horn": self.horn()
      if cmdType == "mute": self.mute()

  def go(self):
    print("MOTOR GO")
    led_r1.off()
    led_r2.off()
    dcMotor.run(Raspi_MotorHAT.FORWARD)
    self.th.isRun = False
    self.th_uwave.start()
    #time.sleep(1)
    #dcMotor.run(Raspi_MotorHAT.RELEASE)

  def back(self):
    print("MOTOR BACK")
    dcMotor.run(Raspi_MotorHAT.BACKWARD)
    led_r1.off()
    led_r2.off()
    self.th.isRun = True
    self.th.start()
    #time.sleep(1)
    #dcMotor.run(Raspi_MotorHAT.RELEASE)

  def left(self):
    steer(30)
    self.th_led.onLed = 0
    self.th_led.dirOn = True
    self.th_led.start()
    print("MOTOR LEFT")

  def right(self):
    steer(-30)
    self.th_led.onLed = 1
    self.th_led.dirOn = True
    self.th_led.start()
    print("MOTOR RIGHT")

  def mid(self):
    led_l.off()
    led_r.off()
    steer(0)
    self.th_led.dirOn = False
    self.th_led.start()
    print("MOTOR MID")

  def stop(self):
    led_r1.on()
    led_r2.on()
    print("MOTOR STOP")
    dcMotor.run(Raspi_MotorHAT.RELEASE)
    self.th.isRun = False

  def horn(self):
    k.start(100)
    k.ChangeDutyCycle(90)
    k.ChangeFrequency(800)
 
  def mute(self):
    k.stop()

def steer(angle=0): #
  if angle <= -30: #
      angle = -30

  if angle >= 30:
      angle = 30

  pulse_time = mid_center

  if angle == 0 :
      pulse_time = mid_center
      servo.setPWM(0,0,mid_center)

  elif angle > 0 : # LEFT
      #a2pul = int(angle*L_itv/30) + mid_center
      pulse_time = int(angle*L_itv/30) + mid_center
      servo.setPWM(0,0,pulse_time)

  elif angle < 0 : #RIGHT
      pulse_time = int(angle*R_itv/30)*(-1) + mid_center
      servo.setPWM(0,0,pulse_time)

  else :
      servo.setPWM(0,0,pulse_time)
  #pulse_time = 170+(340-200)//180*(angle+90)
  #servo.setPWM(0,0,pulse_time)

th = pollingThread()
th.start()

app = QApplication([])

#infinity loop
while True:
  pass
