from kivy.properties import StringProperty
from kivy.uix.image import Image

from .SarcomereLines import SarcomereLines


class Picture(Image):
    """
    Picture is the class that will show the image.
    It subclasses Image in order to be able to respond to events with
    the defined functions as well as to configure behavior internally.

    The source property will be the filename to show.

    The canvas is the object that takes drawing instructions, it's inherited from Image.
    """
    do_rotation = False
    do_scale = True
    source = StringProperty(None)

    def __init__(self, **kwargs):
        """
        Construct Picture, and pass the working args to Image to load the image.
        Initialize things like the line annotations class that's associated with the image.
        :param kwargs:
        """
        super(Picture, self).__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True
        self.txt_name = kwargs["source"] + ".annot_txt"
        self.keep_points = SarcomereLines(self.txt_name)
        self.draw()
        self._modify = False  # this toggles the edit state
        self.magic_point = None

    def draw(self):
        """
        Draw the annotation lines on the image (canvas)
        """
        self.keep_points.draw(self.canvas)

    def on_touch_down(self, touch):
        """
        This is a kivy hook. By defining this function on the Picture the picture
        responds to mouse clicks
        :param touch: this is the mouse down point, touch.pos are the image coordinates.
        """
        print("p:in on_touch_down")
        if self._modify:
            self.magic_point = touch
            self.keep_points.highlight_nearest(self.magic_point, self.canvas)
        else:
            self.keep_points.add_point(touch)
            self.keep_points.write_file(self.txt_name, self.size)
            self.draw()
        return True

    def undo_last(self):
        """
        undo_last clears the last action be it ending the line or a point added to the last line.
        """
        self.keep_points.undo_last()
        self.draw()

    def end_line(self):
        """
        end the line by inserting an empty line at the end of the list.
        """
        self.keep_points.end_line()

    def toggle_modify(self):
        """
        In modify mode a mouse down selects the nearest line. If 'r' is struck after selecting
        it will remove the line from the annotation list. If 'm' or the modify button are struck
        then it cancels out of the mode.
        """
        self._modify = not self._modify
        self.keep_points.draw_highlight(None, self.canvas)
        self.draw()

    def set_remove(self):
        """
        Removes the line nearest the point selected, exits edit mode, and redraws the canvas.
        """
        if self._modify:
            self.keep_points.remove_nearest(self.magic_point, self.canvas)
            self.keep_points.draw(self.canvas)
            self.toggle_modify()
        self.draw()

    def set_scale_factor(self, sf):
        """
        pass the scale factor through to the line annotations class so that it can scale the lines appropriately to
        the figure scaling.
        :param sf: scale factor, ie if the figure is 2x larger than the native image then sf=2
        """
        self.keep_points.set_scale_factor(sf)
        self.draw()
