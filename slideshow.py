from itertools import cycle
from PIL import Image, ImageTk
import io
import Tkinter as tk


class App(tk.Tk):
    def photo_image(self, jpg_filename):
        with io.open(jpg_filename, 'rb') as ifh:
            pil_image = Image.open(ifh)
            return ImageTk.PhotoImage(pil_image)

    '''Tk window/label adjusts to size of image'''
    def __init__(self, image_files, x, y, delay):
        try:
            # the root will be self
            tk.Tk.__init__(self)
            # set x, y position only
            #self.geometry('+{}+{}'.format(x, y))
            self.geometry("{0}x{1}+0-20".format(self.winfo_screenwidth(), self.winfo_screenheight()))
            self.delay = delay
            # allows repeat cycling through the pictures
            # store as (img_object, img_name) tuple
            self.pictures = cycle((self.photo_image(image), image) for image in image_files)
            self.picture_display = tk.Label(self)
            self.picture_display.pack()
        except KeyboardInterrupt:
            quit()

    def show_slides(self):
        '''cycle through the images and show them'''
        # next works with Python26 or higher
        img_object, img_name = next(self.pictures)
        self.picture_display.config(image=img_object)
        # shows the image filename, but could be expanded
        # to show an associated description of the image
        self.title(img_name)
        self.after(self.delay, self.show_slides)

    def run(self):
        self.mainloop()


# set milliseconds time between slides
delay = 3500

# get a series of gif images you have in the working folder
# or use full path, or set directory to where the images are
image_files = [
#'/home/pi/fotobox/py-slideshow/images/2.jpg',
'/home/pi/fotobox/py-slideshow/images/1.gif',
'/home/pi/fotobox/py-slideshow/images/3.jpg',
'/home/pi/fotobox/py-slideshow/images/4.jpg',
'/home/pi/fotobox/py-slideshow/images/5.png'
]

# upper left corner coordinates of app window
x = 100
y = 50

app = App(image_files, x, y, delay)
app.show_slides()
app.run()