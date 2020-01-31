
import tkinter as tk
import PIL
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import PIL.ImageTk

class ImageFeed(tk.Frame):
    '''
    A widgets that easily allows showing a camerafeed (or any PIL
    image feed) if the object has a method callled get, which returns
    a PIL image.
    '''

    def __init__(self, tk_master, size='original', feed_object=None, fallback_size=(800,600)):
        '''
        feed_object     Any object having get method that returns a PIL image
        size            Tuple of (x, y) in pixels or "original" or a float scaling
                        factor where values larger than 1 incease feed's size.
        '''
        tk.Frame.__init__(self, tk_master)
        self.tk_master = tk_master

        self.feed_object = feed_object
        
        if type(size) == type(('tuple',2)) and len(size) == 2:
            self.size = size
        elif type(size) == type(4.2) or type(size) == type(42):
            try:
                w, h = self.feed_object.get().size
            except:
                w, h = fallback_size
            self.size = (int(w*size), int(h*size))
        elif size == 'original':
            try:
                w, h = self.feed_object.get().size
            except:
                w, h = fallback_size
            self.size = (w, h)
        else:
            raise ValueError('Given size invalid: {}'.format(size))
    
        self.update_interval = 0

        self.imagelabel = tk.Label(self)
        self.imagelabel.grid()

    def set_source(self, feed_object):
        '''
        See __init__ method
        '''
        self.feed_object = feed_object

    def set_update_interval(self, milliseconds):
        '''
        If milliseconds. If 0 then no udpate.
        '''
        self.update_interval = milliseconds
        if self.update_interval:
            self.update_feed()

    def update_feed(self, img=None):
        if img is None:
            try:
                image = self.feed_object.get()
                image = image.resize(self.size)
                self.photoimage = PIL.ImageTk.PhotoImage(image)
            except Exception as e:
                image = PIL.Image.new('RGB', self.size)
                draw = PIL.ImageDraw.Draw(image)
                font = PIL.ImageFont.load_default()
                draw.text((0,0), "Error while retriving the image\n{}".format(str(e)), (255,255,255), font=font)
                
                self.photoimage = PIL.ImageTk.PhotoImage(image)
        else:
            self.photoimage = PIL.ImageTk.PhotoImage(img)

        self.imagelabel.configure(image=self.photoimage)
        
        if self.update_interval:
            self.after(self.update_interval, self.update_feed)

    def show_image(image):
        '''
        Instead of getting the image from the source, show any
        PIL object image.


        image       A PIL (pillow) image
        '''
        return self.update_feed(img=image)
