from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout


class LoadDialog(FloatLayout):
    """
    Popup dialog box that loads a fileview. this is all handled by editor.kv (the kivy view file)
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
