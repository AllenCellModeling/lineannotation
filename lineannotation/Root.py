from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from math import pow
import os

from .LoadDialog import LoadDialog
from .Picture import Picture


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
        self.js_x_size = 2048
        self.js_y_size = 2048
        self.scale_value = 1

    def js_size(self):
        """
        the scaled image size
        """
        sz = (self.js_x_size*self.scale_value, self.js_y_size*self.scale_value)
        return sz

    def js_scale_size(self, sv):
        """
        set the scale value and return the size given that scaling factor
        :param sv: scale value
        :return: scaled size
        """
        self.scale_value = sv
        pos = (self.scale_value*self.js_x_size, self.scale_value*self.js_y_size)
        return pos

    def add_picture(self, path):
        """
        load the Image inside a scrollview and attach it to the root object ( this class)
        :param path: image path
        """
        filename = path
        try:
            # load the image
            sv = ScrollView(size_hint=(0.9, 0.9), pos_hint={'top': 0.975, 'right': 0.95})
            sv.do_scroll_x = True
            sv.do_scroll_y = True
            l_picture = Picture(source=filename, size=(self.js_size()), size_hint=(None, None))
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
        if self.picture is None: return
        self.picture.end_line()

    def undo_last(self):
        if self.picture is None: return
        self.picture.undo_last()

    def toggle_modify(self):
        if self.picture is None: return
        self.picture.toggle_modify()

    def set_remove(self):
        self.picture.set_remove()

    def update_zoom(self):
        cval = self.ids.zoomer.value
        fval = pow(2.0, float(cval))
        if self.picture:
            self.picture.size = self.js_scale_size(fval)
            self.picture.set_scale_factor(fval)

    def zoom_up(self):
        if self.picture:
            self.ids.zoomer.value += 1
            self.update_zoom()

    def zoom_down(self):
        if self.picture:
            self.ids.zoomer.value -= 1
            self.update_zoom()

    def _on_keyboard_handler(self, key, scancode, codepoint, modifier, *args):
        """
        this is a hook which allows keybindings to be added. The keys are mapped to the member function.
        :param modifier: the key that was pressed (all other modifiers / other arguments are ignored)
        """
        ktofunc = {
            'e': self.end_line,
            'z': self.undo_last,
            'm': self.toggle_modify,
            'r': self.set_remove,
            '=': self.zoom_up,
            '-': self.zoom_down
        }
        func = ktofunc.get(modifier, None)
        if func:
            func()

