#!/usr/bin/env python

import RPi.GPIO as GPIO ## Import GPIO library
from time import sleep
from picamera import PiCamera
import io
from Tkinter import *
from PIL import Image, ImageTk
import gc

TAKE_PHOTO_BUTTON_PIN = 13
Relais_1_PIN = 3
Relais_2_PIN = 5
PREVIEW_RESOLUTION = (1280, 800)
PHOTO_RESOLUTION = (2592, 1620)
SHUTTER_SPEED = 1000

class Fotobox():
  def __init__(self):
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(Relais_1_PIN, GPIO.OUT, initial=True)
    GPIO.setup(TAKE_PHOTO_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TAKE_PHOTO_BUTTON_PIN, GPIO.RISING, callback=self.takePhotos, bouncetime=200)
    #init Frame
    self.tk = Tk()
    #self.tk.geometry("=500x500")
    self.tk.attributes('-fullscreen', True)
    self.tk.config(background='white', cursor='none')
    self.pictureDisplay = Label(self.tk, background='white')
    #self.pictureDisplay.config(width=200)
    self.pictureDisplay.config(font=("Courier", 300))
    self.pictureDisplay.pack(expand=True)
    self.tk.bind("<Escape>", self.endFullscreen)
    self.camera = PiCamera() 
    self.camera.resolution = PREVIEW_RESOLUTION
    self.camera.hflip = True
    self.is_ready_for_photo = True
    self.camera.start_preview()


  def endFullscreen(self, event=None):
    GPIO.cleanup()
    self.tk.destroy()
    print "bye"
    return "return"

  def showResult(self, displayTime, filename):
    with io.open(filename, 'rb') as ifh:
      original = Image.open(ifh)
      resized = original.resize(PREVIEW_RESOLUTION) 
      self.pictureDisplay.image = ImageTk.PhotoImage(resized) # Keep a reference, prevent GC
      self.pictureDisplay.config(image=self.pictureDisplay.image)
      sleep(displayTime)
      self.pictureDisplay['text'] = ''
      self.pictureDisplay.config(image="")


  def takePhotos(self, channel):
    if (GPIO.input(TAKE_PHOTO_BUTTON_PIN) and self.is_ready_for_photo == True):
      self.is_ready_for_photo = False
      self.camera.stop_preview()
      self.camera.hflip = False
      #self.pictureDisplay.config(font=("Courier", 300))      

      for ex in ['_a','_b','_c']:
        for t in ['3','2','1']:        
          self.pictureDisplay['text'] = t
          if t == '1':
            GPIO.output(Relais_1_PIN, False)
          sleep(1)
        self.pictureDisplay['text'] = ''
        self.camera.resolution = PHOTO_RESOLUTION
        name = '/home/pi/fotobox/img_'+str(self.camera.timestamp)+ex+'.jpg'
        
        self.camera.capture(name)
        GPIO.output(Relais_1_PIN, True)
        #self.pictureDisplay.config(font=("Courier", 50))
        #self.pictureDisplay['text'] = 'lade...'
        self.showResult(3, name)
      self.camera.resolution = PREVIEW_RESOLUTION
      self.camera.hflip = True
      self.camera.start_preview()
      self.is_ready_for_photo = True
    else:
      print 'not ready yet'
      

  def run(self):
    print "Waiting for button..."
    self.tk.mainloop()

fotobox = Fotobox()
fotobox.run()

