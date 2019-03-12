'''
Basic Picture Viewer
====================

This simple image annotator uses an Image widget inside a ScrollView.
You can click adding new points that join to form lines (annotations).
Scrolling moves the image around the visible window. Annotations are in
the context of the native image coordinates (0,0) is lower left corner.

'''
import os
os.environ["KIVY_NO_ARGS"] = "1"

from argparse import ArgumentParser
import kivy
from kivy.app import App
from kivy.factory import Factory
from lineannotation.LoadDialog import LoadDialog
from lineannotation.Root import Root

kivy.require('1.0.6')



class Editor(App):
    pass

    # def run(self, ip):
    #     super.run()
    def take_image_path(self, ip):
        self.root.add_picture(ip)


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

parser = ArgumentParser()
parser.add_argument("-ip", "--image_path", help="path to image to open")
parser.add_argument("-df", "--default_folder", help="folder to use for folder loading", default="~/img_res/")

if __name__ == '__main__':
    js_args = parser.parse_args()
    if js_args.image_path:
        os.environ["JS_FILEPATH"] = js_args.image_path

    os.environ["JS_DEFAULT_FOLDER"] = js_args.default_folder

    Editor().run()
