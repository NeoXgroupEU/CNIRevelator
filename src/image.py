"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Image calculation for CNI printing                              *
*                                                                              *
*  Copyright © 2018-2019 Adrien Bourmault (neox95)                             *
*                                                                              *
*  This file is part of CNIRevelator.                                          *
*                                                                              *
*  CNIRevelator is free software: you can redistribute it and/or modify        *
*  it under the terms of the GNU General Public License as published by        *
*  the Free Software Foundation, either version 3 of the License, or           *
*  any later version.                                                          *
*                                                                              *
*  CNIRevelator is distributed in the hope that it will be useful,             *
*  but WITHOUT ANY WARRANTY*without even the implied warranty of               *
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               *
*  GNU General Public License for more details.                                *
*                                                                              *
*  You should have received a copy of the GNU General Public License           *
* along with CNIRevelator. If not, see <https:*www.gnu.org/licenses/>.         *
********************************************************************************
"""

class CanvasImage:

    def __init__(self, placeholder, file, type):
        """ Initialize the ImageFrame """
        self.type = type
        self.angle = 0
        self.imscale = 1.0
        self._CanvasImage__delta = 1.3
        self._CanvasImage__filter = Image.ANTIALIAS
        self._CanvasImage__previous_state = 0
        self.path = file
        self._CanvasImage__imframe = ttk.Frame(placeholder)
        self.placeholder = placeholder
        hbar = AutoScrollbar((self._CanvasImage__imframe), orient='horizontal')
        vbar = AutoScrollbar((self._CanvasImage__imframe), orient='vertical')
        hbar.grid(row=1, column=0, sticky='we')
        vbar.grid(row=0, column=1, sticky='ns')
        self.canvas = Canvas((self._CanvasImage__imframe), highlightthickness=0, xscrollcommand=(hbar.set),
          yscrollcommand=(vbar.set))
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()
        hbar.configure(command=(self._CanvasImage__scroll_x))
        vbar.configure(command=(self._CanvasImage__scroll_y))
        self.canvas.bind('<Configure>', lambda event: self._CanvasImage__show_image())
        self.canvas.bind('<ButtonPress-1>', self._CanvasImage__move_from)
        self.canvas.bind('<B1-Motion>', self._CanvasImage__move_to)
        self.canvas.bind('<MouseWheel>', self._CanvasImage__wheel)
        self._CanvasImage__huge = False
        self._CanvasImage__huge_size = 14000
        self._CanvasImage__band_width = 1024
        Image.MAX_IMAGE_PIXELS = 1000000000
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            self._CanvasImage__image = Image.open(self.path)
        self.imwidth, self.imheight = self._CanvasImage__image.size
        if self.imwidth * self.imheight > self._CanvasImage__huge_size * self._CanvasImage__huge_size:
            if self._CanvasImage__image.tile[0][0] == 'raw':
                self._CanvasImage__huge = True
                self._CanvasImage__offset = self._CanvasImage__image.tile[0][2]
                self._CanvasImage__tile = [self._CanvasImage__image.tile[0][0],
                 [
                  0, 0, self.imwidth, 0],
                 self._CanvasImage__offset,
                 self._CanvasImage__image.tile[0][3]]
        self._CanvasImage__min_side = min(self.imwidth, self.imheight)
        self._CanvasImage__pyramid = [self.smaller()] if self._CanvasImage__huge else [Image.open(self.path)]
        self._CanvasImage__ratio = max(self.imwidth, self.imheight) / self._CanvasImage__huge_size if self._CanvasImage__huge else 1.0
        self._CanvasImage__curr_img = 0
        self._CanvasImage__scale = self.imscale * self._CanvasImage__ratio
        self._CanvasImage__reduction = 2
        w, h = self._CanvasImage__pyramid[(-1)].size
        while w > 512 and h > 512:
            w /= self._CanvasImage__reduction
            h /= self._CanvasImage__reduction
            try:
                self._CanvasImage__pyramid.append(self._CanvasImage__pyramid[(-1)].resize((int(w), int(h)), self._CanvasImage__filter))
            except TypeError:
                showerror(title='Erreur de fichier', message="Image incompatible. Merci d'utiliser une autre image ou de la convertir dans un format standard accepté!", parent=(self.placeholder))
                self.placeholder.parent.openerrored = True
                self.placeholder.destroy()
                self.destroy()
                return

        self.container = self.canvas.create_rectangle((0, 0, self.imwidth, self.imheight), width=0)
        self._CanvasImage__show_image()
        self.canvas.focus_set()

    def rotatem(self):
        self.angle += 1
        self._CanvasImage__show_image()

    def rotatep(self):
        self.angle -= 1
        self._CanvasImage__show_image()

    def rotatemm(self):
        self.angle += 90
        self._CanvasImage__show_image()

    def rotatepp(self):
        self.angle -= 90
        self._CanvasImage__show_image()

    def smaller(self):
        """ Resize image proportionally and return smaller image """
        w1, h1 = float(self.imwidth), float(self.imheight)
        w2, h2 = float(self._CanvasImage__huge_size), float(self._CanvasImage__huge_size)
        aspect_ratio1 = w1 / h1
        aspect_ratio2 = w2 / h2
        if aspect_ratio1 == aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(h2)))
            k = h2 / h1
            w = int(w2)
        else:
            if aspect_ratio1 > aspect_ratio2:
                image = Image.new('RGB', (int(w2), int(w2 / aspect_ratio1)))
                k = h2 / w1
                w = int(w2)
            else:
                image = Image.new('RGB', (int(h2 * aspect_ratio1), int(h2)))
                k = h2 / h1
                w = int(h2 * aspect_ratio1)
        i, j, n = 0, 1, round(0.5 + self.imheight / self._CanvasImage__band_width)
        while i < self.imheight:
            band = min(self._CanvasImage__band_width, self.imheight - i)
            self._CanvasImage__tile[1][3] = band
            self._CanvasImage__tile[2] = self._CanvasImage__offset + self.imwidth * i * 3
            self._CanvasImage__image.close()
            self._CanvasImage__image = Image.open(self.path)
            self._CanvasImage__image.size = (self.imwidth, band)
            self._CanvasImage__image.tile = [self._CanvasImage__tile]
            cropped = self._CanvasImage__image.crop((0, 0, self.imwidth, band))
            image.paste(cropped.resize((w, int(band * k) + 1), self._CanvasImage__filter), (0, int(i * k)))
            i += band
            j += 1

        return image

    def redraw_figures(self):
        """ Dummy function to redraw figures in the children classes """
        pass

    def grid(self, **kw):
        """ Put CanvasImage widget on the parent widget """
        (self._CanvasImage__imframe.grid)(**kw)
        self._CanvasImage__imframe.grid(sticky='nswe')
        self._CanvasImage__imframe.rowconfigure(0, weight=1)
        self._CanvasImage__imframe.columnconfigure(0, weight=1)

    def __scroll_x(self, *args, **kwargs):
        """ Scroll canvas horizontally and redraw the image """
        (self.canvas.xview)(*args)
        self._CanvasImage__show_image()

    def __scroll_y(self, *args, **kwargs):
        """ Scroll canvas vertically and redraw the image """
        (self.canvas.yview)(*args)
        self._CanvasImage__show_image()

    def __show_image(self):
        """ Show image on the Canvas. Implements correct image zoom almost like in Google Maps """
        box_image = self.canvas.coords(self.container)
        box_canvas = (self.canvas.canvasx(0),
         self.canvas.canvasy(0),
         self.canvas.canvasx(self.canvas.winfo_width()),
         self.canvas.canvasy(self.canvas.winfo_height()))
        box_img_int = tuple(map(int, box_image))
        box_scroll = [
         min(box_img_int[0], box_canvas[0]), min(box_img_int[1], box_canvas[1]),
         max(box_img_int[2], box_canvas[2]), max(box_img_int[3], box_canvas[3])]
        if box_scroll[0] == box_canvas[0]:
            if box_scroll[2] == box_canvas[2]:
                box_scroll[0] = box_img_int[0]
                box_scroll[2] = box_img_int[2]
        if box_scroll[1] == box_canvas[1] and box_scroll[3] == box_canvas[3]:
            box_scroll[1] = box_img_int[1]
            box_scroll[3] = box_img_int[3]
        self.canvas.configure(scrollregion=(tuple(map(int, box_scroll))))
        x1 = max(box_canvas[0] - box_image[0], 0)
        y1 = max(box_canvas[1] - box_image[1], 0)
        x2 = min(box_canvas[2], box_image[2]) - box_image[0]
        y2 = min(box_canvas[3], box_image[3]) - box_image[1]
        if int(x2 - x1) > 0:
            if int(y2 - y1) > 0:
                if self._CanvasImage__huge:
                    if self._CanvasImage__curr_img < 0:
                        h = int((y2 - y1) / self.imscale)
                        self._CanvasImage__tile[1][3] = h
                        self._CanvasImage__tile[2] = self._CanvasImage__offset + self.imwidth * int(y1 / self.imscale) * 3
                        self._CanvasImage__image.close()
                        self._CanvasImage__image = Image.open(self.path)
                        self._CanvasImage__image.size = (self.imwidth, h)
                        self._CanvasImage__image.tile = [self._CanvasImage__tile]
                        image = self._CanvasImage__image.crop((int(x1 / self.imscale), 0, int(x2 / self.imscale), h))
                    image = self._CanvasImage__pyramid[max(0, self._CanvasImage__curr_img)].crop((
                     int(x1 / self._CanvasImage__scale), int(y1 / self._CanvasImage__scale),
                     int(x2 / self._CanvasImage__scale), int(y2 / self._CanvasImage__scale)))
                self.resizedim = image.resize((int(x2 - x1), int(y2 - y1)), self._CanvasImage__filter).rotate((self.angle), resample=(Image.BICUBIC), expand=1)
                imagetk = ImageTk.PhotoImage((self.resizedim), master=(self.placeholder))
                imageid = self.canvas.create_image((max(box_canvas[0], box_img_int[0])), (max(box_canvas[1], box_img_int[1])),
                  anchor='nw',
                  image=imagetk)
                self.canvas.lower(imageid)
                self.canvas.imagetk = imagetk

    def __move_from(self, event):
        """ Remember previous coordinates for scrolling with the mouse """
        self.canvas.scan_mark(event.x, event.y)

    def __move_to(self, event):
        """ Drag (move) canvas to the new position """
        self.canvas.scan_dragto((event.x), (event.y), gain=1)
        self._CanvasImage__show_image()

    def outside(self, x, y):
        """ Checks if the point (x,y) is outside the image area """
        bbox = self.canvas.coords(self.container)
        if bbox[0] < x < bbox[2]:
            if bbox[1] < y < bbox[3]:
                pass
            return False
        else:
            return True

    def __wheel(self, event):
        """ Zoom with mouse wheel """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if self.outside(x, y):
            return
        scale = 1.0
        if event.delta == -120:
            if round(self._CanvasImage__min_side * self.imscale) < int(self.placeholder.winfo_screenheight()):
                return
            self.imscale /= self._CanvasImage__delta
            scale /= self._CanvasImage__delta
        if event.delta == 120:
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height()) >> 1
            if i < self.imscale:
                return
            self.imscale *= self._CanvasImage__delta
            scale *= self._CanvasImage__delta
        k = self.imscale * self._CanvasImage__ratio
        self._CanvasImage__curr_img = min(-1 * int(math.log(k, self._CanvasImage__reduction)), len(self._CanvasImage__pyramid) - 1)
        self._CanvasImage__scale = k * math.pow(self._CanvasImage__reduction, max(0, self._CanvasImage__curr_img))
        self.canvas.scale('all', x, y, scale, scale)
        self.redraw_figures()
        self._CanvasImage__show_image()

    def crop(self, bbox):
        """ Crop rectangle from the image and return it """
        if self._CanvasImage__huge:
            band = bbox[3] - bbox[1]
            self._CanvasImage__tile[1][3] = band
            self._CanvasImage__tile[2] = self._CanvasImage__offset + self.imwidth * bbox[1] * 3
            self._CanvasImage__image.close()
            self._CanvasImage__image = Image.open(self.path)
            self._CanvasImage__image.size = (self.imwidth, band)
            self._CanvasImage__image.tile = [self._CanvasImage__tile]
            return self._CanvasImage__image.crop((bbox[0], 0, bbox[2], band))
        else:
            return self._CanvasImage__pyramid[0].crop(bbox)

    def destroy(self):
        """ ImageFrame destructor """
        self._CanvasImage__image.close()
        map(lambda i: i.close, self._CanvasImage__pyramid)
        del self._CanvasImage__pyramid[:]
        del self._CanvasImage__pyramid
        self.canvas.destroy()