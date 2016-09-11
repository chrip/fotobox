import RPi.GPIO as GPIO ## Import GPIO library
from time import sleep
from picamera import PiCamera

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(40, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def takePhotos():
  try:
    print "take photos"  
    camera = PiCamera()
    camera.resolution = "1280x800"
    camera.start_preview()
    GPIO.output(40,True)
    sleep(8)
    GPIO.output(40,False)
    camera.stop_preview()
    for i in [0.5, 0.2, 0.1]:
      for j in range(4):
        print i,j
        GPIO.output(40,True)
        sleep(i)
        GPIO.output(40,False)
        sleep(i)
    
    camera.resolution = "2592x1944"
    for ex in ['_a','_b','_c','_d']:
      GPIO.output(33,True)
      filename = 'img_'+str(camera.timestamp)+ex+'.jpg'
      camera.capture(filename)
      print filename
      GPIO.output(33,False)
      sleep(1)
    
  except KeyboardInterrupt:
    # User quit
    GPIO.cleanup()
    camera.close()
  camera.close()

#GPIO.add_event_detect(13, GPIO.FALLING, callback=takePhotos, bouncetime=300)
try:
  print "Waiting for button..."
  while(GPIO.wait_for_edge(13, GPIO.RISING, bouncetime=1000)):      
    takePhotos()
    print "Waiting for button..."

except KeyboardInterrupt:
  GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()
