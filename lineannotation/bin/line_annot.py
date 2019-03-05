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
from lineannotation.LoadDialog import LoadDialog
from lineannotation.Root import Root

kivy.require('1.0.6')


class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Editor().run()
