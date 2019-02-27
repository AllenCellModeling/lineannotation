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

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.core.window import Window
import json
import os


class SarcomereLines(object):
    def __init__(self):
        self.lines = []
        self.add_line()

    def add_line(self):
        self.lines.append([])

    def add_point(self, point):
        self.lines[-1].append(point.pos)
        print(str(point.pos))

    def remove_point(self):
        self.lines[-1].pop()

    def write_file(self, fname):
        with open(fname, "w") as fp:
            json.dump(self.lines, fp)
        fp.closed



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
        self.txt_name = kwargs["source"] + ".txt"
        self.keep_points = SarcomereLines()

    def on_touch_down(self, touch):
        self.keep_points.add_point(touch)
        self.keep_points.write_file(self.txt_name)

# class PicturesApp(App):
#
#     def build_config(self, config):
#         pass
#
#     def build(self):
#
#         # the root is created in pictures.kv
#         root = self.root
#
#         # get any files into images directory
#         # curdir = dirname(__file__)
#         # for filename in glob(join(curdir, 'images', '*')):
#
#         filename = 'resources/Capture 3 - Position 6_XY1543355356_Z0_T000_C0.png'
#         try:
#             # load the image
#             picture = Picture(source=filename)  # rotation=randint(-30, 30))
#             # add to the main field
#             root.add_widget(picture)
#         except Exception as e:
#             Logger.exception('Pictures: Unable to load <%s>' % filename)
#
#     def on_pause(self):
#         return True


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

# FloatLayout):


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

        except Exception as e:
            Logger.exception('Pictures: Unable to load <%s>' % filename)
            exit(-1)
        self.picture = sv

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
        #self.canvas.clear()
        self.dismiss_popup()

    def clear_line(self):
        if self.picture is None: return
        self.remove_widget(self.picture)
        self.picture = None


class Editor(App):
    pass
    # def build(self):
    #
    #     # the root is created in pictures.kv
    #     root = self.root
    #
    #     # get any files into images directory
    #     # curdir = dirname(__file__)
    #     # for filename in glob(join(curdir, 'images', '*')):
    #
    #     filename = 'resources/Capture 3 - Position 6_XY1543355356_Z0_T000_C0.png'
    #     try:
    #         # load the image
    #         picture = Picture(source=filename)  # rotation=randint(-30, 30))
    #         # add to the main field
    #         root.add_widget(picture)
    #     except Exception as e:
    #         Logger.exception('Pictures: Unable to load <%s>' % filename)
    #
    # def on_pause(self):
    #     return True


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Editor().run()
    #PicturesApp().run()
