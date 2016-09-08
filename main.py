from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = "1280x800"
camera.start_preview()
# Camera warm-up time
sleep(8)
camera.stop_preview()
sleep(3)
camera.resolution = "2592x1944"
camera.capture('foo.jpg')

try:
  print "Starting photo sequence"
  for ex in ['_a','_b','_c','_d']:
    filename = 'img_'+str(camera.timestamp)+ex+'.jpg'
    camera.capture(filename)
    print filename  
    sleep(1)
  
except KeyboardInterrupt:
  # User quit
  print "\nGoodbye!"
