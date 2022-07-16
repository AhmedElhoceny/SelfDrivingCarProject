import RPi.GPIO as GPIO
import time
import sys
import tkinter as tk
import requests
import pyautogui

potentiometer_Value = 10
Algorithm_Angle_Value = 0.5

BaseURL = ""

Senstivity = 0.1
SafeSpace = 30


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def SelfDriveCar(Angle):
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)
    potentiometer_Value = translate(analog_read() , 38,45, -1 , 1)
#     potentiometer_Value = analog_read()
    print(potentiometer_Value)
    if Angle - potentiometer_Value > Senstivity :
        print(potentiometer_Value)
#         StepperMotorLeft()
        print("Moving Right.......")
        # Move Direction_Dc_Motor To Right Direction ---> E=0 & F = 1
    elif  Angle - potentiometer_Value < -Senstivity:
#         StepperMotorRight()
        print("Moving Left.......")
        print(potentiometer_Value)
        # Move Direction_Dc_Motor To Left Direction ---> E=1 & F = 0
    else:
        StepperMotorStop()
        print("Stop............")
        # Stop ----> E=0 & F = 0   


timeSleep = 0.02

OutPut_Pins = [15 , 16 , 18 , 19 ,21 , 31 , 32 , 33 , 35 , 36 ]

def discharge():
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)
    GPIO.setup(37,GPIO.IN)
    GPIO.setup(38,GPIO.OUT)
    
    GPIO.output(38 , 0)
    time.sleep(timeSleep)
    
def charge_time():
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)
    GPIO.setup(37,GPIO.OUT)
    GPIO.setup(38,GPIO.IN)
    count = 0
    GPIO.output(37 , 1)
    while not GPIO.input(38):
        count = count + 1
    return count

def analog_read():
    discharge()
    return charge_time()
    
    
def StopAllProcess():

    init()
    GPIO.output(35 , 1)
    GPIO.output(36 , 1)
    GPIO.output(15 , 1)
    GPIO.output(16 , 1)
    GPIO.output(18 , 1)
    GPIO.output(19 , 1)

     
def altra():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    #set GPIO Pins
    GPIO_TRIGGER1 = 3
    GPIO_ECHO1 = 5
    GPIO_TRIGGER2 = 7
    GPIO_ECHO2 = 8
    GPIO_TRIGGER3 = 10
    GPIO_ECHO3 = 11
    GPIO_TRIGGER4 = 12
    GPIO_ECHO4 = 13
     
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
    GPIO.setup(GPIO_ECHO1, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
    GPIO.setup(GPIO_ECHO2, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
    GPIO.setup(GPIO_ECHO3, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER4, GPIO.OUT)
    GPIO.setup(GPIO_ECHO4, GPIO.IN)
    GPIO.output(GPIO_TRIGGER1, False)
    GPIO.output(GPIO_TRIGGER2, False)
    GPIO.output(GPIO_TRIGGER3, False)
    GPIO.output(GPIO_TRIGGER4, False)

    print ("sensor1")
    time.sleep(timeSleep)
    GPIO.output(GPIO_TRIGGER1, True)
    time.sleep(timeSleep)
    GPIO.output(GPIO_TRIGGER1, False)
    while GPIO.input(GPIO_ECHO1) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO1) == 1:
        StopTime = time.time()  
    TimeElapsed = StopTime - StartTime
    distance = TimeElapsed * 17150
    distance_Forward = round(distance, 2)
    print ("sensor1 :" ,distance_Forward, "cm")
    while(distance_Forward < SafeSpace):
        StopAllProcess()
        print("Warning Left.....")
        time.sleep(timeSleep)
        GPIO.output(GPIO_TRIGGER1, True)
        time.sleep(timeSleep)
        GPIO.output(GPIO_TRIGGER1, False)
        while GPIO.input(GPIO_ECHO1) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO1) == 1:
            StopTime = time.time()  
        TimeElapsed = StopTime - StartTime
        distance = TimeElapsed * 17150
        distance_Forward = round(distance, 2)
#         response = requests.get( BaseURL + "SendData?Sensor_1=" + str(distance_Forward) + "&Sensor_2=0&Sensor_3=0&Sensor_4=0")
#     if distance_Forward < Safe_Space:
#         Move('s');
#         print("Sensor_1 Warnning.....")
#         for i in range(20):
#             SelfDriveCar(0)
#         for x in range(20):
#             Move("B1")
            
    print ("sensor2")
    time.sleep(timeSleep)
    GPIO.output(GPIO_TRIGGER2, True)
    time.sleep(timeSleep)
    GPIO.output(GPIO_TRIGGER2, False)
    while GPIO.input(GPIO_ECHO2) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO2) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = TimeElapsed * 17150
    distance_Back = round(distance, 2)
    print ("sensor2 :" ,distance_Back, "cm")
    while(distance_Back < SafeSpace):
        StopAllProcess()
        print("Warning Forward.....")
        time.sleep(timeSleep)
        GPIO.output(GPIO_TRIGGER2, True)
        time.sleep(timeSleep)
        GPIO.output(GPIO_TRIGGER2, False)
        while GPIO.input(GPIO_ECHO2) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO2) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance = TimeElapsed * 17150
        distance_Back = round(distance, 2)
#         response = requests.get( BaseURL + "SendData?Sensor_2=" +str(distance_Back) + "&Sensor_1=0&Sensor_3=0&Sensor_4=0")

#     if distance_Back < Safe_Space:
#         Move('s');
#         print("Sensor_2 Warnning.....")
#         for i in range(20):
#             SelfDriveCar(0)
#         for x in range(20):
#             Move("F1")

    print ("sensor3")
    time.sleep(timeSleep)
    GPIO.output(GPIO_TRIGGER3, True)
    time.sleep(timeSleep)
    GPIO.output(GPIO_TRIGGER3, False)
    while GPIO.input(GPIO_ECHO3) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO3) == 1:
        StopTime = time.time()  
    TimeElapsed = StopTime - StartTime
    distance = TimeElapsed * 17150
    distance_Right = round(distance, 2)
    print ("sensor3 :" ,distance_Right, "cm")
    while(distance_Right < SafeSpace):
        StopAllProcess()
        print("Warning Right.....")
        time.sleep(timeSleep)
        GPIO.output(GPIO_TRIGGER3, True)
        time.sleep(timeSleep)
        GPIO.output(GPIO_TRIGGER3, False)
        while GPIO.input(GPIO_ECHO3) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO3) == 1:
            StopTime = time.time()  
        TimeElapsed = StopTime - StartTime
        distance = TimeElapsed * 17150
        distance_Right = round(distance, 2)
#         response = requests.get( BaseURL + "SendData?Sensor_3=" + str(distance_Right) + "&Sensor_1=0&Sensor_2=0&Sensor_4=0")

#     if distance_Right < Safe_Space:
#         for i in range(20):
#             SelfDriveCar(-0.8)
#         for x in range(20):
#             Move("B1")
#     
#     
    print ("sensor4")
    time.sleep(timeSleep)
    GPIO.output(GPIO_TRIGGER4, True)
    time.sleep(timeSleep)
    GPIO.output(GPIO_TRIGGER4, False)
    while GPIO.input(GPIO_ECHO4) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO4) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = TimeElapsed * 17150
    distance_Left = round(distance, 2)
    print ("sensor4 :" ,distance_Left, "cm")
    while distance_Left < SafeSpace :
        StopAllProcess()
        print("Warning Back.....")
        
        time.sleep(timeSleep)
        GPIO.output(GPIO_TRIGGER4, True)
        time.sleep(timeSleep)
        GPIO.output(GPIO_TRIGGER4, False)
        while GPIO.input(GPIO_ECHO4) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO4) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance = TimeElapsed * 17150
        distance_Left = round(distance, 2)
#         response = requests.get( BaseURL + "SendData?Sensor_4=" + str(distance_Left) + "&Sensor_1=0&Sensor_2=0&Sensor_3=0")
#         print(response.status_code)
        
#     if distance_Left < Safe_Space:
#         Move('s');
#         print("Sensor_4 Warnning.....")
#         for i in range(20):
#             SelfDriveCar(0.8)
#         for x in range(20):
#             Move("B1")
# 


def init():
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)			#disable warnings


    for Item in OutPut_Pins:
        GPIO.setup(Item,GPIO.OUT)

def GetDistance():
    print("GetDistances.......")
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)
        
    GPIO_TRIGGER1 =3 
    GPIO_ECHO1 = 5
    GPIO_TRIGGER2 = 7
    GPIO_ECHO2 = 8
    GPIO_TRIGGER3= 10
    GPIO_ECHO3 = 11
    GPIO_TRIGGER4 = 12
    GPIO_ECHO4 = 13
    
    GPIO.output(GPIO_TRIGGER1 , 1)
    GPIO.output(GPIO_TRIGGER2 , 1)
    GPIO.output(GPIO_TRIGGER3 , 1)
    GPIO.output(GPIO_TRIGGER4 , 1)
    time.sleep(timeSleep);
    GPIO.output(GPIO_TRIGGER1 , 0)
    GPIO.output(GPIO_TRIGGER2 , 0)
    GPIO.output(GPIO_TRIGGER3 , 0)
    GPIO.output(GPIO_TRIGGER4 , 0)
    
    StartTime1 = time.time()
    StopTime1 = time.time()
    StartTime2 = time.time()
    StopTime2 = time.time()
    StartTime3 = time.time()
    StopTime3 = time.time()
    StartTime4 = time.time()
    StopTime4 = time.time()
    
    while GPIO.input(GPIO_ECHO1) == 0 :
        StartTime1 = time.time()
    while GPIO.input(GPIO_ECHO1) == 1 :
        StopTime1 = time.time()
        
    while GPIO.input(GPIO_ECHO2) == 0 :
        StartTime2 = time.time()
    while GPIO.input(GPIO_ECHO2) == 1 :
        StopTime2 = time.time()
    
    while GPIO.input(GPIO_ECHO3) == 0 :
        StartTime3 = time.time()
    while GPIO.input(GPIO_ECHO3) == 1 :
        StopTime3 = time.time()
    
    while GPIO.input(GPIO_ECHO4) == 0 :
        StartTime4 = time.time()
    while GPIO.input(GPIO_ECHO4) == 1 :
        StopTime4 = time.time()
        
    TimeElapsed1 = StopTime1 - StartTime1
    TimeElapsed2 = StopTime2 - StartTime2
    TimeElapsed3 = StopTime3 - StartTime3
    TimeElapsed4 = StopTime4 - StartTime4
    
    distance1 = (TimeElapsed1 * 34300) / 2
    distance2 = (TimeElapsed2 * 34300) / 2
    distance3 = (TimeElapsed3 * 34300) / 2
    distance4 = (TimeElapsed4 * 34300) / 2
    
def TackPic(PicName):
    print("Hello...............................")
    camera= PiCamera();
    camera.start_preview();
    time.sleep(0.3);
    camera.capture(PicName + ".jpg");
    camera.close();

def StepperMotorStop():
    
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)

    init()

    GPIO.setup(35,GPIO.OUT)
    GPIO.setup(36,GPIO.OUT)
    
    GPIO.output(35,1)
    GPIO.output(36,1)
    
    
def StepperMotorRight():
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)
    
    init()
    
    GPIO.setup(35,GPIO.OUT)
    GPIO.setup(36,GPIO.OUT)
    
    GPIO.output(35,1)
    GPIO.output(36,0)
    
    
    #for x in range(10):
        #GPIO.output(36,0)
        #time.sleep(0.001)
        #GPIO.output(36,1)
        #time.sleep(0.001)
   

def StepperMotorLeft():
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)
    
    init()
    
    GPIO.setup(35,GPIO.OUT)
    GPIO.setup(36,GPIO.OUT)
    
    GPIO.output(35,0)
    GPIO.output(36,1)
    
    
def Move(ActionTitle):
    init()
#     altra()
    if ActionTitle == 'B1':
        GPIO.output(15, 1)
        GPIO.output(16, 0)
        GPIO.output(18, 1)
        GPIO.output(19, 1)
        time.sleep(timeSleep)
        GPIO.cleanup()
    elif ActionTitle == 'B2':
        GPIO.output(15, 1)
        GPIO.output(16, 0)
        GPIO.output(18, 0)
        GPIO.output(19, 0)
        time.sleep(timeSleep)
        GPIO.cleanup()
    elif ActionTitle == 'B':
        GPIO.output(15, 0)
        GPIO.output(16, 1)
        GPIO.output(18, 0)
        GPIO.output(19, 0)  
        time.sleep(timeSleep)
        GPIO.cleanup()
    elif ActionTitle == 'F1':
        GPIO.output(15, 0)
        GPIO.output(16, 1)
        GPIO.output(18, 0)
        GPIO.output(19, 0)  
        time.sleep(timeSleep)
        GPIO.cleanup()  
    elif ActionTitle == 'F2':
        GPIO.output(15, 0)
        GPIO.output(16, 1)
        GPIO.output(18, 1)
        GPIO.output(19, 1)
        time.sleep(timeSleep)
        GPIO.cleanup()
    elif ActionTitle == 's':
        GPIO.output(15, 0)
        GPIO.output(16, 0)
        GPIO.output(18, 0)
        GPIO.output(19, 0)
        time.sleep(timeSleep)
        GPIO.cleanup() 
    

def Key_input(event):
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    GPIO.setwarnings(False)
    init()
    
    
    print("Key:" + event.char)
    key_press = event.char
    
    if key_press.lower() == '5':
        Move('F1')
        print("Moving Forward First Speed Level....")
        StopAllProcess()
    elif key_press.lower() == '8':
        Move('F2')
        print("Moving Forward Second Speed Level....")
        StopAllProcess()
    elif key_press.lower() == '2':
        Move('B1')
        print("Moving Backward First Speed Level....")
        StopAllProcess()
    elif key_press.lower() == '0':
        Move('B2')
        print("Moving Backward Second Speed Level....")
        StopAllProcess()
    elif key_press.lower() == 's':
        Move('s')
        print("stop....")
        StopAllProcess()
    elif key_press.lower() == '6':

        StepperMotorRight()
    #         for i in range(20):
    #         print(analog_read())
        print("stepper Motor ClockWise....")
        time.sleep(timeSleep)
        StepperMotorStop()
    elif key_press.lower() == '4':
        StepperMotorLeft()
        print("stepper Motor Unti Clock Wise....")
        time.sleep(timeSleep)
        StepperMotorStop()
    elif key_press.lower() == '.':
        print("Take Photo.....")
        TackPic("CarPic_1");
    elif key_press.lower() == 't':
        altra();
    elif key_press.lower() == 'a':
#         for i in range(10):
        SelfDriveCar(0.7)
        time.sleep(timeSleep)
    else : 
        print("This Action is not exist.....");
    

command = tk.Tk()
command.bind('<KeyPress>' , Key_input)
command.mainloop()

# **********************************Motors*******************8
# Main Control System


# 
# while 1:
#         steering = sum(pyautogui.position(y=-960)) / 960
#         print(steering)
#         # motor move Function
#         # motor steering Function(steering)
