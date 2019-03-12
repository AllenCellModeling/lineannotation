'''
Basic Picture Viewer
====================

This simple image annotator uses an Image widget inside a ScrollView.
You can click adding new points that join to form lines (annotations).
Scrolling moves the image around the visible window. Annotations are in
the context of the native image coordinates (0,0) is lower left corner.

'''
import os
os.environ["KIVY_NO_ARGS"] = "1"  # has to be here or kivy will parse the args rather than argparse
from argparse import ArgumentParser
import kivy
from kivy.app import App
from kivy.factory import Factory
from lineannotation.LoadDialog import LoadDialog
from lineannotation.Root import Root


class Editor(App):
    pass


def main():
    parser = ArgumentParser()
    parser.add_argument("-ip", "--image_path", help="path to image to open")
    parser.add_argument("-df", "--default_folder", help="folder to use for folder loading", default="~/")

    js_args = parser.parse_args()
    if js_args.image_path:
        os.environ["JS_FILEPATH"] = js_args.image_path

    os.environ["JS_DEFAULT_FOLDER"] = js_args.default_folder

    kivy.require('1.0.6')

    Factory.register('Root', cls=Root)
    Factory.register('LoadDialog', cls=LoadDialog)
    Editor().run()


if __name__ == '__main__':
    main()
