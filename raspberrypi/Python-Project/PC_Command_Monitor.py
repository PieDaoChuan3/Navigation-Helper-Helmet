import threading
import raspberrypi_camera
import raspberrypi_camera_record
import Voice_prompts
import motor
import tfmini
import os
import time
import sys
from mutagen.mp3 import MP3


if __name__ == "__main__":
    
    audio = MP3('/home/pi/Desktop/Python-Project/audio/start.mp3')
    os.system("mplayer /home/pi/Desktop/Python-Project/audio/start.mp3")
    time_1=audio.info.length 
    print(time_1)       
    if time_1<5:
        time.sleep(int(time_1+2)) 
    else:
        time.sleep(int(time_1+(time_1/12)))
    #time.sleep(40)
    camera = threading.Thread(target=raspberrypi_camera.run)
    voice = threading.Thread(target=Voice_prompts.run)
    record = threading.Thread(target=raspberrypi_camera_record.run)
    revolve = threading.Thread(target=motor.main)
    #measure = threading.Thread(target=tfmini.run)
    camera.setDaemon(True)
    voice.setDaemon(True)
    record.setDaemon(True)
    revolve.setDaemon(True)
    #measure.setDaemon(True)
    #command='sudo shutdown -h now'%('file')
    f = open('/home/pi/Desktop/command/PC_Command.txt','w')
    f.write('0')
    f.close()
    Reset = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
    Reset.write('0')
    Reset.close()
    while True:
        #print('the program is running')
        f = open('/home/pi/Desktop/command/PC_Command.txt','r',encoding='UTF-8')#Open the object recognition.txt file 
        situation = f.readlines()#Branch the object recognition.txt file 
        #print(situation)
        if '0' in situation:
            #print('Waiting for order...')
            continue
        elif '1' in situation:
            if camera.is_alive() or voice.is_alive():
                #print('ststem is working properly.')
                continue
            else:
              camera.start()
              revolve.start()
              time.sleep(5)
              voice.start()
        elif '2' in situation:
            if record.is_alive():
                #print('ststem is working properly.')
                continue
            else:
              record.start()
        elif '-1' in situation:
            f = open('/home/pi/Desktop/command/User_rotation.txt', 'r',encoding='UTF-8')
            delay = f.readline()
            delay = int(delay)
            motor.reset(delay)
            f = open('/home/pi/Desktop/command/PC_Command.txt','w')
            f.write('0')
            f.close()
            os.system("mplayer /home/pi/Desktop/Python-Project/audio/sutdown.mp3")
            time.sleep(1)
            os.system('sudo shutdown -h now')
        elif '-2' in situation:
            f = open('/home/pi/Desktop/command/User_rotation.txt', 'r',encoding='UTF-8')
            delay = f.readline()
            delay = int(delay)
            motor.reset(delay)
            sys.exit(0)
        elif '-3' in situation:
            f = open('/home/pi/Desktop/command/User_rotation.txt', 'r',encoding='UTF-8')
            delay = f.readline()
            delay = int(delay)
            motor.reset(delay)
            f = open('/home/pi/Desktop/command/PC_Command.txt','w')
            f.write('0')
            f.close()
            os.system("mplayer /home/pi/Desktop/Python-Project/audio/reboot.mp3")
            time.sleep(1)
            os.system('sudo reboot')
            
        time.sleep(0.5)    