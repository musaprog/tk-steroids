
import tkinter as tk


CALLBACK_FORMATS = ['rgb', 'hex']

class _ColorMap(tk.Frame):
    '''
    A colorpicker part: Pick colors from a colormap.
    '''   

    def __init__(self, tk_parent, callback=None,
            callback_format='rgb'):
        '''
        callback : None or callable
            Callback on click on the colormap that takes in one positional
            argument that is the selected color.
        callback_format : string
            'rgb' or 'hex'
        '''
        tk.Frame.__init__(self, tk_parent)
        self.callback = callback

        if callback_format in ['rgb', 'hex']:
            self.callback_format = callback_format
        else:
            raise ValueError("Unkown callback format {}. Use {}".format(
                callback_format, CALLBACK_FORMATS))

        self.mouse_down = False

        self.map_width = 100
        self.map_height = 100
        self.colormap = tk.PhotoImage(height=self.map_height,
                width=self.map_width)
        
        red, green, blue = self._hsv()
        for j in range(0, self.map_height):
            saturation = 1-j/(self.map_height-1)
            for i in range(0, self.map_width):
                color = '#{0:02x}{1:02x}{2:02x}'.format(
                        int(saturation*red[i]+(1-saturation)*255),
                        int(saturation*green[i]+(1-saturation)*255),
                        int(saturation*blue[i]+(1-saturation)*255))
                self.colormap.put(color, to=(i,j))
        
        
        self.canvas = tk.Canvas(self, width=self.map_width, height=self.map_height)
        self.canvas.create_image(0, 0, image=self.colormap,
                anchor=tk.NW)
        self.canvas.grid(row=1, column=1)
            
        self.canvas.scale('all', 0, 0 ,4, 4)

        self.canvas.bind('<Button-1>', self._on_click)
       

    def _on_click(self, event):
        color = self.colormap.get(event.x, event.y)
        
        if self.callback_format == 'hex':
            color = '#{0:02x}{1:02x}{2:02x}'.format(*color)
        elif self.callback_format == 'rgb':
            pass

        if callable(self.callback):
            self.callback(color)
        

    def _hsv(self):
        '''
        Crete hsv colors.

        Returns three lists of intensity values (0-255)
        for the red, green and blue channels.
        '''
        # _   _
        #  \_/
        hsv_red = []
        for h_i in range(0, self.map_width):
            h = h_i * 360 / self.map_width
            if 0<=h< 60 or 300<=h<360: 
                value = 1
            elif 120<=h<240:
                value = 0
            elif 60<=h<120:
                value = (60-(h-60))/60
            elif 240<=h< 300:
                value = (h-240)/60

            hsv_red.append(int(255*value))
        
        # Blue
        h_cut = int(120/360*len(hsv_red))
        hsv_blue = hsv_red[h_cut:] + hsv_red[:h_cut]
        
        # Green
        h_cut = int(240/360*len(hsv_red))
        hsv_green = hsv_red[h_cut:] + hsv_red[:h_cut]
 
        return hsv_red, hsv_green, hsv_blue


class ColorPicker(tk.Frame):
    '''
    Pick colors from a colormap, show the picked color,
    and call callback on exit.
    
    Colors are common 8-bit 3-channel.
    '''

    def __init__(self, tk_parent, callback=None):
        tk.Frame.__init__(self, tk_parent)

        self.colormap = _ColorMap(self, callback=self.set_color,
                callback_format='hex')
        self.colormap.grid(row=1, column=1)
        
        self.preview = tk.Canvas(self, width=100, height=100)
        self.preview.grid(row=1, column=2)

    def set_color(self, color):
        '''
        Sets the currently selected color
        '''
        self.preview.config(bg=color)


class MultiPicker(tk.Frame):
    '''
    Displays the selected colors, and by pressing
    one of the colors, opens a ColorPicker instance.
    '''
    def __init__(self, tk_parent, color_names,
            callback=None):
        '''
        color_n
        callback : None or callable or list of callables
            Called when a color is set. If list
        '''
        tk.Frame.__init__(self, tk_parent)
        
        #for 
        #tk.Label(self, text=)

    

