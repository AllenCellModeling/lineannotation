from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from sarcomereannotation.LoadDialog import LoadDialog
from sarcomereannotation.Picture import Picture
import os


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
        self.__popup = None

    def add_picture(self, path):
        filename = path
        try:
            # load the image
            sv = ScrollView(size_hint=(0.9, 0.9), pos_hint={'top': 0.975, 'right': 0.95})
            l_picture = Picture(source=filename)
            # add to the main field
            sv.add_widget(l_picture)  # add the picture to the scrollview
            self.add_widget(sv)      # add the scrollview to the Root Canvas
            self.picture = l_picture  # hold on to picture object to pass messages

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
