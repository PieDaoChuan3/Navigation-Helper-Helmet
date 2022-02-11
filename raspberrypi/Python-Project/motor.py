import RPi.GPIO as GPIO
import time
import os

f = open('/home/pi/Desktop/command/User_rotation.txt', 'w+')
f.write('2')
f.close()
f = open('/home/pi/Desktop/command/User_rotation.txt', 'r',encoding='UTF-8')
delay = f.readline()
delay = int(delay) #delay unit is ms
pin_18 = 18
pin_17 = 17
pin_22 = 22
pin_24 = 27



GPIO.setmode(GPIO.BCM) #Set the coding method of the pin 
    
def init():
    GPIO.setwarnings(False)
    GPIO.setup(pin_18, GPIO.OUT)
    GPIO.setup(pin_17, GPIO.OUT)
    GPIO.setup(pin_22, GPIO.OUT)
    GPIO.setup(pin_24, GPIO.OUT)
 

def reset(delay):
    f = open('/home/pi/Desktop/command/Project_Data/angle.txt', 'r',encoding='UTF-8')
    angle = f.readline()    
    angle = int(angle)
    delay = delay/1000
    
    
    if angle != 0:
        print(angle)
        while angle < 0:
            if angle != 0:
                setStep(1, 0, 0, 0)
                time.sleep(delay)
                setStep(1, 1, 0, 0)
                angle = angle +1
                time.sleep(delay)
                
                if angle != 0:
                    setStep(0, 1, 0, 0)
                    time.sleep(delay)
                    setStep(0, 1, 1, 0)
                    angle = angle +1
                    time.sleep(delay)
                    
                    if angle != 0:
                        setStep(0, 0, 1, 0)
                        time.sleep(delay)
                        setStep(0, 0, 1, 1)
                        angle = angle +1
                        time.sleep(delay)
                        
                        if angle != 0:
                            setStep(0, 0, 0, 1)
                            time.sleep(delay)
                            setStep(1, 0, 0, 1)
                            angle = angle +1
                            time.sleep(delay)
                            
        while angle > 0:
            if angle != 0:
                setStep(1, 0, 0, 1)
                time.sleep(delay)
                setStep(0, 0, 0, 1)
                angle = angle -1
                time.sleep(delay)
                
                if angle != 0:
                    setStep(0, 0, 1, 1)
                    time.sleep(delay)
                    setStep(0, 0, 1, 0)
                    angle = angle -1
                    time.sleep(delay)
                    
                    if angle != 0:
                        setStep(0, 1, 1, 0)
                        time.sleep(delay)
                        setStep(0, 1, 0, 0)
                        angle = angle -1
                        time.sleep(delay)
                        
                        if angle != 0:
                            setStep(1, 1, 0, 0)
                            time.sleep(delay)
                            setStep(1, 0, 0, 0)
                            angle = angle -1
                            time.sleep(delay)
          
    with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:
        f.write(str(angle))
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
        f.write("in_front_of")   
    #time.sleep(2)
    print("Resetted")
    
        
    
def forward45(delay):
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('1')
    situation.close()
    i =0
    angle =0  
    while i < 64 :
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        angle = angle +1
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle)) 
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle)) 
        angle = angle +1
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle)) 
        angle = angle +1
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
             f.write(str(angle)) 
        angle = angle +1
        time.sleep(delay)
        i=i+1
    print(angle)
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
             f.write("front_left")
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('0')
    situation.close()
    time.sleep(20)

def forward90(delay):
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('1')
    situation.close()
    i =0
    angle =256 
    while i < 64 :
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        i=i+1
    print(angle)
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
             f.write("left")
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('0')
    situation.close()
    time.sleep(20)

    
def backward45(delay):
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('1')
    situation.close()
    i =0
    angle = 512
    while i < 64 :
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        time.sleep(delay)
        setStep(1, 0, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        i=i+1
    print(angle)
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
             f.write("front_left")
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('0')
    situation.close()
    time.sleep(20)


def backward0(delay):
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('1')
    situation.close()
    i =0
    angle = 256
    while i < 64 :
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        time.sleep(delay)
        setStep(1, 0, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        i=i+1
    print(angle)
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
             f.write("in_front_of")
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('0')
    situation.close()
    time.sleep(20)


def backward_45(delay):
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('1')
    situation.close()
    i =0
    angle = 0
    while i < 64 :
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        time.sleep(delay)
        setStep(1, 0, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        i=i+1        
    print(angle)
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
             f.write("front-right")
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('0')
    situation.close()
    time.sleep(20)

    
def backward_90(delay):
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('1')
    situation.close()
    i =0
    angle = -256
    while i < 64 :
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        time.sleep(delay)
        setStep(1, 0, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle -1
        time.sleep(delay)
        i=i+1
    print(angle)
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
             f.write("right")
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('0')
    situation.close()
    time.sleep(20)


def forward_45(delay):
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('1')
    situation.close()
    i =0
    angle =-512 
    while i < 64 :
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        i=i+1
    print(angle)
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
             f.write("front_right")
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('0')
    situation.close()
    time.sleep(20)


def forward0(delay):
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('1')
    situation.close()
    i =0
    angle =-256 
    while i < 64 :
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        angle = angle +1
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        angle = angle +1
        with open('/home/pi/Desktop/command/Project_Data/angle.txt','w') as f:    
            f.write(str(angle))
        time.sleep(delay)
        i=i+1
    print(angle)
    with open('/home/pi/Desktop/command/Project_Data/direction.txt','w') as f:    
             f.write("in_front_of")
    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    situation.write('0')
    situation.close()
    time.sleep(20)

    
def setStep(w1, w2, w3, w4):
  GPIO.output(pin_18, w1)
  GPIO.output(pin_17, w2)
  GPIO.output(pin_22, w3)
  GPIO.output(pin_24, w4)
  
def main():
    init()
    reset(delay)
    os.system("mplayer /home/pi/Desktop/Python-Project/audio/direction/reset.mp3")
    time.sleep(2)
    while True:
        f = open('/home/pi/Desktop/command/User_control_motor.txt','r',encoding='UTF-8')
        user_control = f.readline()
        if user_control == '1':
            for i in range(8):
                situation = open('/home/pi/Desktop/command/motor_run.txt', 'r',encoding='UTF-8')
                user_situation = situation.readline()
                f = open('/home/pi/Desktop/command/User_control_motor.txt','r',encoding='UTF-8')
                user_control = f.readline()
                if user_situation == '1':
                    while 1:
                       situation = open('/home/pi/Desktop/command/motor_run.txt', 'r',encoding='UTF-8')
                       user_situation = situation.readline()
                       print("waiting")
                       if user_situation == '0':
                          break
                if user_control == '0':
                    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
                    situation.write('1')
                    situation.close()
                    reset(delay)
                    os.system("mplayer /home/pi/Desktop/Python-Project/audio/direction/reset.mp3")
                    situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
                    situation.write('0')
                    situation.close()
                    break
                else:
                    if i == 0 :
                       forward45(delay/1000) 
                    elif i == 1 :
                       forward90(delay/1000)
                    elif i == 2 :
                       backward45(delay/1000)
                    elif i == 3 :
                       backward0(delay/1000)
                    elif i == 4 :
                       backward_45(delay/1000)
                    elif i == 5 :
                       backward_90(delay/1000)
                    elif i == 6 :
                       forward_45(delay/1000)
                    elif i == 7 :
                       forward0(delay/1000) 
        
#main() # 调用main