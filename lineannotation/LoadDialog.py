from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout


class LoadDialog(FloatLayout):
    """
    Popup dialog box that loads a fileview. this is all handled by editor.kv (the kivy view file)
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    image_folder = StringProperty('~/')

    def __init__(self, jspath, **kwargs):
        super().__init__(**kwargs)
        assert isinstance(jspath, str)
        self.image_folder = jspath

