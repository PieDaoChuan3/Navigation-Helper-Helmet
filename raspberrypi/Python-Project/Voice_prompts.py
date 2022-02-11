import time
import pygame
import os
from mutagen.mp3 import MP3
import vlc
import serial
import time

ser = serial.Serial("/dev/ttyAMA0", 115200)

def recognition(meter,centimeter):
  f = open('/home/pi/Desktop/command/Object_recognition_result.txt','r',encoding='UTF-8')#Open the object recognition.txt file 
  lines_1 = f.readlines()#Branch the object recognition.txt file
  f = open('/home/pi/Desktop/command/Face_recognition_result.txt','r',encoding='UTF-8')#Open the face recognition.txt file 
  lines_2 = f.readlines()#Branch the face recognition.txt file 
  f = open('/home/pi/Desktop/command/Project_Data/direction.txt','r',encoding='UTF-8')#Open the distance.txt file 
  lines_3 = f.readline()#Branch the face recognition.txt file 


  #Start to recognize the type of object 
  audio=MP3('/home/pi/Desktop/Python-Project/audio/key_world/There_are_obstacles.mp3')
  os.system("mplayer /home/pi/Desktop/Python-Project/audio/key_world/There_are_obstacles.mp3")
  #time_1=audio.info.length 
  #print(time_1)       
  
  os.system('mplayer /home/pi/Desktop/Python-Project/audio/direction/%s.mp3'%(lines_3))
  
  audio=MP3('/home/pi/Desktop/Python-Project/audio/distance/meter/%d.mp3'%(meter)) 
  os.system('mplayer /home/pi/Desktop/Python-Project/audio/distance/meter/%d.mp3'%(meter))
  #time_1=audio.info.length 
  #print(time_1)       

  audio=MP3('/home/pi/Desktop/Python-Project/audio/distance/centimeter/%d.mp3'%(centimeter)) 
  os.system('mplayer /home/pi/Desktop/Python-Project/audio/distance/centimeter/%d.mp3'%(centimeter))
  #time_1=audio.info.length 
  #print(time_1)       

  audio=MP3('/home/pi/Desktop/Python-Project/audio/key_world/away_from_you.mp3') 
  os.system('mplayer /home/pi/Desktop/Python-Project/audio/key_world/away_from_you.mp3')
  #time_1=audio.info.length 
  #print(time_1)       

  for line_1 in lines_1:
    #Determine whether the object is human 
    if 'person' in line_1:
        #Describe the object 
        audio = MP3('/home/pi/Desktop/Python-Project/audio/key_world/There_is_a_person.mp3')
        os.system("mplayer /home/pi/Desktop/Python-Project/audio/key_world/There_is_a_person.mp3")
        time_1=audio.info.length 
        print(time_1)       
        #if time_1<5:
         #   time.sleep(int(time_1+2)) 
        #else:
         #   time.sleep(int(time_1+(time_1/12)))
        #p.stop()
        #Describe the distance 
        #audio=MP3('C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_3)) 
        #os.system('start C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_3))
        #time_1=audio.info.length 
        #print(time_1)       
        #if time_1<5:
            #time.sleep(int(time_1)) 
        #else:
            #time.sleep(int(time_1+(time_1/12)))

        #Describe the location 
        #for  line_4 in lines_4:
         #   if 'left'or'right'or'front'or'behand' in line_4:
          #      audio=MP3('C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_4)) 
           #     os.system('start C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_4))
            #    time_1=audio.info.length 
             #   print(time_1)       
              #  if time_1<5:
               #     time.sleep(int(time_1)) 
                #else:
                 #   time.sleep(int(time_1+(time_1/12)))
               
        for line_2 in lines_2:
            #The result is a familiar person 
            if 'Junlin' or 'Jingwei' or 'Bo' in line_2:
                print(line_2)
                audio = MP3('/home/pi/Desktop/Python-Project/audio/familiarpeople/%s.mp3'%(line_2))
                os.system("mplayer /home/pi/Desktop/Python-Project/audio/familiarpeople/%s.mp3"%(line_2))
                time_1=audio.info.length 
                print(time_1)
                
                #if time_1<5:#Build delay 
                    #time.sleep(int(time_1+4)) 
                #else:
                    #time.sleep(int(time_1+(time_1/10)))                
                #p.stop()
            #结果为不熟悉的人
            else:
               audio = MP3('/home/pi/Desktop/Python-Project/audio/Unknown.mp3')
               os.system("mplayer /home/pi/Desktop/Python-Project/audio/Unknown.mp3")
               time_1=audio.info.length #Define the duration parameter of the voice file 
               print(time_1)
               #if time_1<5:#Build delay 
                    #time.sleep(int(time_1+2)) 
               #else:
                    #time.sleep(int(time_1+(time_1/12)))
               #p.stop()
    elif 'car' in line_1:
        audio = MP3('/home/pi/Desktop/Python-Project/audio/object/%s.mp3'%(line_1))
        os.system("mplayer /home/pi/Desktop/Python-Project/audio/object/%s.mp3"%(line_1))
        time_1=audio.info.length #Define the duration parameter of the voice file 
        print(time_1)
                    
        #if time_1<5:#Build delay 
            #time.sleep(int(time_1+3)) 
        #else:
            #time.sleep(int(time_1+(time_1/12)))
        #p.stop()
        #Describe the distance 
        #for line_3 in lines_3:
         #   if 'one'or'two'or'three'or'four' in line_3:
          #      audio=MP3('C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_3)) 
           #     os.system('start C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_3))
            #    time_1=audio.info.length 
             #   print(time_1)       
              #  if time_1<5:
               #     time.sleep(int(time_1+2)) 
                #else:
                 #   time.sleep(int(time_1+(time_1/12)))

        #Describe the location 
        #for  line_4 in lines_4:
         #   if 'left'or'right'or'front'or'behand' in line_4:
          #      audio=MP3('C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_4)) 
           #     os.system('start C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_4))
            #    time_1=audio.info.length 
             #   print(time_1)       
              #  if time_1<5:
               #     time.sleep(int(time_1+2)) 
                #else:
                 #   time.sleep(int(time_1+(time_1/12)))
               
    else:
        audio = MP3('/home/pi/Desktop/Python-Project/audio/object/%s.mp3'%(line_1))
        os.system("mplayer /home/pi/Desktop/Python-Project/audio/object/%s.mp3"%(line_1))
        time_1=audio.info.length #Define the duration parameter of the voice file 
        print(time_1)
                    
        #if time_1<5:#Build delay 
            #time.sleep(int(time_1+3)) 
        #else:
            #time.sleep(int(time_1+(time_1/12)))
        #p.stop()

        #Describe the distance 
        #for line_3 in lines_3:
         #   if 'one'or'two'or'three'or'four' in line_3:
          #      audio=MP3('C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_3)) 
           #     os.system('start C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_3))
            #    time_1=audio.info.length 
             #   print(time_1)       
              #  if time_1<5:
               #     time.sleep(int(time_1+2)) 
                #else:
                 #   time.sleep(int(time_1+(time_1/12)))

        #Describe the location 
        #for  line_4 in lines_4:
         #   if 'left'or'right'or'front'or'behand' in line_4:
          #      audio=MP3('C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_4)) 
           #     os.system('start C:/Users/75018/Desktop/Python-Project/audio/key_world/%s.mp3'%(line_4))
            #    time_1=audio.info.length 
             #   print(time_1)       
              #  if time_1<5:
               #     time.sleep(int(time_1+2)) 
                #else:
                 #   time.sleep(int(time_1+(time_1/12)))

   #os.system("TASKKILL /F /IM QQMusic.exe") #关闭相应播放器
  #time.sleep(10)
  print('The Application Has Been Successfully Closed')
  #time.sleep(10)

def getTFminiData():
    while True:
        time.sleep(0.3)
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)   
            ser.reset_input_buffer() 
            # type(recv), 'str' in python2(recv[0] = 'Y'), 'bytes' in python3(recv[0] = 89)
            # type(recv[0]), 'str' in python2, 'int' in python3 
            
            if recv[0] == 0x59 and recv[1] == 0x59:     #python3
                distance = recv[2] + recv[3] * 256
                strength = recv[4] + recv[5] * 256
                #print('(', distance, ',', strength, ')')
                meter = int(distance/100)
                centimeter = distance-int(distance/100)*100
                print('(', meter, ',', centimeter, ')')
                ser.reset_input_buffer()
                return meter,centimeter

def run():
    for i in range(30):
      try:
          if ser.is_open == False:
             ser.open()
          meter,centimeter=getTFminiData()
      except KeyboardInterrupt:   # Ctrl+C
          if ser != None:
             ser.close()
    
    k = -1
    while True:
      try:
          if ser.is_open == False:
             ser.open()
          meter,centimeter=getTFminiData()
      except KeyboardInterrupt:   # Ctrl+C
          if ser != None:
             ser.close()
      f = open('/home/pi/Desktop/command/User_distance.txt','r')
      user_distance = f.readline()
      f.close()
      fw = open('/home/pi/Desktop/command/motor_run.txt','r')
      situation = fw.readline()
      fw.close()
      c = open('/home/pi/Desktop/command/Object_recognition_result.txt','r',encoding='UTF-8')#打开object recognition.txt文件
      objection = c.readline()
      if user_distance == '':
          print('sb python')
          continue
      if meter < int(user_distance) and k < 0 and situation == '0' and objection != '' :
        #print('sadlihasliodhjkawiuhdkliahuslidhaliwdh')
        #meter = 2
        situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
        situation.write('1')
        situation.close()
        k = 7
        recognition(meter,centimeter)
        situation = open('/home/pi/Desktop/command/motor_run.txt', 'w+')
        situation.write('0')
        situation.close()
        time.sleep(15)
        meter = 2
      else:
          #print('32136541685468413213654684')
        print(k)
        k = k-1
        if k<-50:
          k = -1
        continue