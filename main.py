import RPi.GPIO as GPIO ## Import GPIO library
from time import sleep
from picamera import PiCamera
import io
from Tkinter import *
from PIL import Image, ImageTk
import gc

TAKE_PHOTO_BUTTON_PIN = 13

class Fotobox():
  def __init__(self):
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(40, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TAKE_PHOTO_BUTTON_PIN, GPIO.FALLING, callback=self.takePhotos, bouncetime=1000)
    #init Frame
    self.tk = Tk()
    self.tk.attributes('-fullscreen', True)
    self.tk.config(background='white',  cursor='none')
    self.pictureDisplay = Label(self.tk, background='white')
    self.pictureDisplay.pack()        
    self.tk.bind("<Escape>", self.endFullscreen)

  def endFullscreen(self, event=None):
    GPIO.cleanup()
    self.tk.destroy()
    print "bye"
    return "return"

  def showResult(self, displayTime, filename):
    with io.open(filename, 'rb') as ifh:
      original = Image.open(ifh)
      resized = original.resize((1067, 800),Image.ANTIALIAS) 
      #self.pictureDisplay.image = ImageTk.PhotoImage(resized) # Keep a reference, prevent GC
      #self.pictureDisplay.config(image=self.pictureDisplay.image)
      sleep(displayTime)
      #self.pictureDisplay.config(image="")
    
  def ledOnOff(self, gpioPin, sleepTime):
    GPIO.output(gpioPin,True)
    sleep(sleepTime)
    GPIO.output(gpioPin,False)

  def takePhotos(self, channel):
    GPIO.remove_event_detect(TAKE_PHOTO_BUTTON_PIN)
    print "take photos"
    for ex in ['_a','_b','_c']:
      with PiCamera() as camera:
        camera.resolution = (1067, 800)
        camera.start_preview()
        #self.ledOnOff(40, 5)
        for i in [0.5, 0.2, 0.1]:
          for j in range(4):
            self.ledOnOff(40, i)
            sleep(i)
        camera.stop_preview()
        camera.resolution = "2592x1944"
        GPIO.output(33,True)
        name = 'img_'+str(camera.timestamp)+ex+'.jpg'
        camera.capture(name)
        print name
        GPIO.output(33,False)
        camera.close()
        #self.showResult(5, name)
    GPIO.add_event_detect(TAKE_PHOTO_BUTTON_PIN, GPIO.FALLING, callback=self.takePhotos, bouncetime=1000)
    print "take photos done"
    
      

  def run(self):
    print "Waiting for button..."
    self.tk.mainloop()

fotobox = Fotobox()
fotobox.run()

