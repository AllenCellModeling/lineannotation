from .ImagePath import IMAGE_FOLDER
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from .LoadDialog_View import LOADDIALOG_VIEW
import pathlib
from os import path

Builder.load_string(LOADDIALOG_VIEW.format(pathlib.Path(path.expanduser("~")).resolve()))


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
