'''
Basic Picture Viewer
====================

This simple image browser demonstrates the scatter widget. You should
see three framed photographs on a background. You can click and drag
the photos around, or multi-touch to drop a red dot to scale and rotate the
photos.

The photos are loaded from the local images directory, while the background
picture is from the data shipped with kivy in kivy/data/images/background.jpg.
The file pictures.kv describes the interface and the file shadow32.png is
the border to make the images look like framed photographs. Finally,
the file android.txt is used to package the application for use with the
Kivy Launcher Android application.

For Android devices, you can copy/paste this directory into
/sdcard/kivy/pictures on your Android device.

The images in the image directory are from the Internet Archive,
`https://archive.org/details/PublicDomainImages`, and are in the public
domain.

'''

import json
import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.graphics import Color, Ellipse, InstructionGroup, Line
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

import os
import math


class SarcomereLines(object):
    """SarcomereLines

    This class is a queue. It holds on to the list of points that have been clicked.
    It also constructs the drawn lines that get added to the Picture Canvas and handles
    the logic of when to clear the lines from the canvas etc.

    """
    def __init__(self, fname):
        """
        Initialize SarcomereLines with a file name
        :param fname: name of file with lines, if file doesn't exist it is created.
        """
        try:
            with open(fname, 'r') as fp:
                fp.readline()  # Discard the image size for now
                self.lines = json.load(fp=fp)
            fp.closed
        except FileNotFoundError:
            self.lines = [[]]

        self.d = 5
        self.lw = 3
        self.instructions = None  # container to hold the lines drawing object
        self.highlight = None     # container to hold the highlight lines object

    def end_line(self):
        """
        end the current line.
        """
        if len(self.lines[-1]) > 0:
            self.lines.append([])

    def add_point(self, point):
        """
        add point.pos to the end of the last line in the end of the list.
        :param point: this is a kivy point object, pos contains the
        global coordinates in the image frame
        """
        self.lines[-1].append(point.pos)
        print(str(point.pos))

    def undo_last(self):
        if len(self.lines[-1]) == 0 and len(self.lines) > 1:
            self.lines.pop()  # undo the end of list
        else:
            if len(self.lines[-1]) > 0:
                self.lines[-1].pop()

    def write_file(self, fname, img_size):
        with open(fname, "w") as fp:
            json.dump(img_size, fp)
            fp.write("\n")
            json.dump(self.lines, fp)
        fp.closed

    def remove_nearest(self, point, canvas):
        if len(self.lines) == 1 and len(self.lines[0]) == 0: return
        i, r_line = self.select_nearest_line(point)
        self.lines.remove(r_line)
        canvas.remove(self.highlight)
        self.highlight = None

    def highlight_nearest(self, point, canvas):
        if len(self.lines) == 1 and len(self.lines[0]) == 0:
            return
        i, r_line = self.select_nearest_line(point)
        self.draw_highlight(r_line, canvas)

    def draw_highlight(self, line, canvas):
        if self.highlight:
            canvas.remove(self.highlight)
        self.highlight = InstructionGroup()
        self.highlight.add(Color(1, 1, 0))
        self.highlight.add(
            Line(points=[c for p in line for c in p],
                 width = self.lw, dash_length=10,
                 dash_offset=5)
        )
        canvas.add(self.highlight)

    def draw(self, canvas):
        if self.instructions:
            canvas.remove(self.instructions)
        self.instructions = InstructionGroup()
        for line in self.lines:
            if len(line) > 1:
                self.instructions.add(Color(0, 1, 0))
                self.instructions.add(
                    Line(points=[c for p in line for c in p],
                         width=self.lw, dash_length=10,
                         dash_offset=5)
                )
            self.instructions.add(Color(1, 0, 0))
            for p in line:
                self.instructions.add(
                    Ellipse(pos=(p[0] - self.d / 2, p[1] - self.d / 2),
                        size=(self.d, self.d))
                )
        canvas.add(self.instructions)

    def select_nearest_line(self, p):
        line_idx = 0
        p_dist = 100000.0
        for idx, line in enumerate(self.lines):
            for pxy in line:
                d = self.dist(p, pxy)
                if d < p_dist:
                    line_idx = idx
                    p_dist = d
        return line_idx, self.lines[line_idx]

    def dist(self, p1, p2):
        dx = float(p1[0]) - float(p2[0])
        dy = float(p1[1]) - float(p2[1])
        return math.sqrt(dx*dx + dy*dy)


class Picture(Image):
    """
    Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    """
    do_rotation = False
    do_scale = True
    source = StringProperty(None)

    def __init__(self, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.txt_name = kwargs["source"] + ".annot_txt"
        self.keep_points = SarcomereLines(self.txt_name)
        self.draw()
        self._modify = False  # this toggles the edit state
        self.magic_point = None

    def draw(self):
        self.keep_points.draw(self.canvas)

    def on_touch_down(self, touch):
        """
        This is a kivy hook. By defining this function on the Picture the picture
        responds to mouse clicks
        :param touch: this is the mouse down point, touch.pos are the image coordinates.
        """
        print("p:in on_touch_down")
        if self._modify:
            self.magic_point = touch.pos
            self.keep_points.highlight_nearest(self.magic_point, self.canvas)
        else:
            self.keep_points.add_point(touch)
            self.keep_points.write_file(self.txt_name, self.size)
            self.draw()

    def clear_line(self):
        print("p:clear_line")
        self.keep_points.undo_last()
        self.draw()

    def end_line(self):
        print("p:end_line")
        self.keep_points.end_line()

    def toggle_modify(self):
        print("p:toggle_modify")
        self._modify = not self._modify

    def set_remove(self):
        print("p:set_remove")
        if self._modify:
            self.keep_points.remove_nearest(self.magic_point, self.canvas)
            self.keep_points.draw(self.canvas)
            self.toggle_modify()
        self.draw()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    """
    Root is the object that get's created in the application window.
    It's the master object from which others get created.
    This object is tied to the editor.kv as well where view parameters get set.
    """
    picture = None
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    clearline = ObjectProperty(None)
    Window.size = (1024, 1074)

    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        Window.bind(on_keyboard=self._on_keyboard_handler)  # this binds the keyboard input to the member function

    def add_picture(self, path):
        filename = path
        try:
            # load the image
            sv = ScrollView(size_hint=(0.9, 0.9), pos_hint={'top': 0.975, 'right': 0.95})  #  ScrollView(size=(1024, 1024))
            lpicture = Picture(source=filename)
            # add to the main field
            sv.add_widget(lpicture)  # add the picture to the scrollview
            self.add_widget(sv)      # add the scrollview to the Root Canvas
            self.picture = lpicture  # hold on to picture object to pass messages

        except Exception as e:
            Logger.exception('Pictures: Unable to load <%s>' % filename)
            self.picture = None

    def on_pause(self):
        return True

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.add_picture(os.path.join(path, filename[0]))
        self.dismiss_popup()

    def end_line(self):
        print("r:in end_line")
        if self.picture is None: return
        self.picture.end_line()

    def clear_line(self):
        print("r:in clear_line")
        if self.picture is None: return
        self.picture.clear_line()

    def toggle_modify(self):
        print("r:in toggle_modify")
        if self.picture is None: return
        self.picture.toggle_modify()

    def set_remove(self):
        print("r:in set_remove")
        self.picture.set_remove()

    def _on_keyboard_handler(self, key, scancode, codepoint, modifier, *args):
        print("modifier=", modifier)
        ktofunc = {
            'e': self.end_line,
            'z': self.clear_line,
            'm': self.toggle_modify,
            'r': self.set_remove,
            '=': lambda: print('zoom in'),
            '-': lambda: print('zoom out')
        }
        func = ktofunc.get(modifier, None)
        if func:
            func()


class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Editor().run()
