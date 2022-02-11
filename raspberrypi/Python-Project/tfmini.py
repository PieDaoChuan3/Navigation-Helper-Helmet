# -*- coding: utf-8 -*
import serial
import time

ser = serial.Serial("/dev/ttyAMA0", 115200)

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
                alpha = open('/home/pi/Desktop/command/Distance_meter.txt','w+',encoding='UTF-8')
                beta = open('/home/pi/Desktop/command/Distance_centimeter.txt','w+',encoding='UTF-8')
                alpha.write(str(meter))
                beta.write(str(centimeter))
                alpha.close()
                beta.close()
                ser.reset_input_buffer()
                
            if recv[0] == 'Y' and recv[1] == 'Y':     #python2
                lowD = int(recv[2].encode('hex'), 16)      
                highD = int(recv[3].encode('hex'), 16)
                lowS = int(recv[4].encode('hex'), 16)      
                highS = int(recv[5].encode('hex'), 16)
                distance = lowD + highD * 256
                strength = lowS + highS * 256
                print(distance, strength)
                mile = int(distance/100)
                centimeter = distance-int(distance/100)*100
                print(mile,centimeter)
            
            # you can also distinguish python2 and python3: 
            #import sys
            #sys.version[0] == '2'    #True, python2
            #sys.version[0] == '3'    #True, python3


def run():
#if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        getTFminiData()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()