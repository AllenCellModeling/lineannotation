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

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, InstructionGroup
import json
import os


class SarcomereLines(object):
    def __init__(self):
        self.lines = []
        self.add_line()
        self.d = 2
        self.instructions = None

    def add_line(self):
        self.lines.append([])

    def add_point(self, point):
        self.lines[-1].append(point.pos)
        print(str(point.pos))

    def remove_point(self):
        self.lines[-1].pop()

    def remove_line(self, canvas):
        if self.instructions:
            canvas.remove(self.instructions)
        self.instructions = None
        self.lines.pop()
        self.add_line()

    def write_file(self, fname, img_size):
        with open(fname, "w") as fp:
            json.dump(img_size, fp)
            json.dump(self.lines, fp)
        fp.closed

    def draw_points(self, canvas):
        if self.instructions:
            canvas.remove(self.instructions)
        self.instructions = InstructionGroup()
        for line in self.lines:
            if len(line) > 1:
                self.instructions.add(Color(0, 1, 0))
                self.instructions.add(
                    Line(points=[c for p in line for c in p], width=1, dash_length=10, dash_offset=5)
                )
            self.instructions.add(Color(1, 0, 0))
            for p in line:
                self.instructions.add(
                    Ellipse(pos=(p[0] - self.d / 2, p[1] - self.d / 2),
                        size=(self.d, self.d))
                )
        canvas.add(self.instructions)


class Picture(Image):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''
    do_rotation = False
    do_scale = True
    source = StringProperty(None)

    def __init__(self, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.txt_name = kwargs["source"] + ".annot_txt"
        self.keep_points = SarcomereLines()

    def on_touch_down(self, touch):
        self.keep_points.add_point(touch)
        self.keep_points.write_file(self.txt_name, self.size)
        self.keep_points.draw_points(self.canvas)

    def clear_line(self):
        self.keep_points.remove_line(self.canvas)

    def end_line(self):
        self.keep_points.add_line()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    picture = None
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    clearline = ObjectProperty(None)
    Window.size = (1024, 1074)

    def add_picture(self, path):
        filename = path
        #filename = 'resources/Capture 3 - Position 6_XY1543355356_Z0_T000_C0.png'
        try:
            # load the image
            sv = ScrollView(size_hint=(0.9, 0.9), pos_hint={'top': 0.975, 'right': 0.95})  #  ScrollView(size=(1024, 1024))
            lpicture = Picture(source=filename, # pos_hint={'top': 0.98, 'right': 0.98},
                               )  # rotation=randint(-30, 30))
            # add to the main field
            sv.add_widget(lpicture)
            self.add_widget(sv)      # lpicture)
            self.picture = lpicture

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
        if self.picture is None: return
        self.picture.end_line()

    def clear_line(self):
        if self.picture is None: return
        self.picture.clear_line()


class Editor(App):
    pass

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Editor().run()
