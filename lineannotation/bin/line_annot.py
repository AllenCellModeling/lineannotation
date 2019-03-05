'''
Basic Picture Viewer
====================

This simple image annotator uses an Image widget inside a ScrollView.
You can click adding new points that join to form lines (annotations).
Scrolling moves the image around the visible window. Annotations are in
the context of the native image coordinates (0,0) is lower left corner.

'''

import kivy
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from lineannotation.LoadDialog import LoadDialog
from lineannotation.Root import Root

kivy.require('1.0.6')

Builder.load_string("""
#:kivy 1.0
#:import kivy kivy
#:import win kivy.core.window

Root:
    canvas:
        Color:
            rgb: 1, 1, 1
    BoxLayout:
        orientation: 'vertical'
        canvas:
        BoxLayout:
            size_hint_y: None
            height: 30
            #padding: [0, 0, 0, 1054]
            Button:
                pos: 0, 0
                text: 'Load'
                on_release: root.show_load()
            Button:
                text: 'Save'
                on_release: root.show_save()
            Button:
                text: 'Start Line'
                on_release: root.start_line()
            Button:
                text: 'End Line'
                on_release: root.end_line()
            Button:
                text: 'Clear Line'
                on_release: root.toggle_modify()
""")


class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Editor().run()
