import time
import pygame
import os
from mutagen.mp3 import MP3
from gtts import gTTS

language = 'en'
fh = open("C:/Users/75018/Desktop/Python-Project/audio/word/test.txt","r")

myText_1 = fh.read().replace("\n","")

output_1 = gTTS(text=myText_1, lang=language)

output_1.save("C:/Users/75018/Desktop/Python-Project/audio/output1.mp3")
fh.close()