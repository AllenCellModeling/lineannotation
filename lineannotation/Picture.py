from copy import deepcopy
from kivy.graphics import Color, Ellipse, InstructionGroup, Line
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
        self._modify = False  # this toggles the edit state
        self.magic_point = None
        self.instructions = None
        self.highlight = None
        self.d = 5  # diameter of any point drawn
        self.lw = 2  # the width of drawn lines
        self.draw()

    def draw(self):
        """
           redraw all the lines and points
           :param canvas: the image canvas to draw on
           """
        if self.instructions:
            self.canvas.remove(self.instructions)
        self.instructions = InstructionGroup()
        for line in self.keep_points.lines:
            if len(line) > 1:
                self.instructions.add(Color(0, 1, 0))
                self.instructions.add(
                    Line(points=[c * self.keep_points.scale_factor for p in line for c in p],
                         width=self.lw)
                )
            self.instructions.add(Color(1, 0, 0))
            for p in line:
                self.instructions.add(
                    Ellipse(pos=(p[0] * self.keep_points.scale_factor - self.d / 2, p[1] *
                                 self.keep_points.scale_factor - self.d / 2),
                            size=(self.d, self.d))
                )
        self.canvas.add(self.instructions)

    def on_touch_down(self, touch):
        """
        This is a kivy hook. By defining this function on the Picture the picture
        responds to mouse clicks
        :param touch: this is the mouse down point, touch.pos are the image coordinates.
        """
        if self._modify:
            self.magic_point = deepcopy(touch)
            self.highlight_nearest(self.magic_point)
        else:
            self.keep_points.add_point(touch)
            self.draw()
            self.write()
        return True

    def write(self):
        self.keep_points.write_file(self.txt_name, self.size)

    def highlight_nearest(self, point):
        """
        highlight the line nearest the point clicked
        :param point: the point selected
        """
        if len(self.keep_points.lines) == 1 and len(self.keep_points.lines[0]) == 0:
            return
        i, r_line = self.keep_points.select_nearest_line(point)
        self.draw_highlight(r_line)

    def draw_highlight(self, line):
        """
        draw the selected line in yellow to highlight it and allow the user to decide if they want to remove it.
        :param line: the line that was selected
        """
        if self.highlight:
            self.canvas.remove(self.highlight)
            self.highlight = None
        if line:
            self.highlight = InstructionGroup()
            self.highlight.add(Color(1, 1, 0))
            self.highlight.add(
                Line(points=[c * self.keep_points.scale_factor for p in line for c in p],
                     width=self.lw)
            )
            self.canvas.add(self.highlight)

    def undo_last(self):
        """
        undo_last clears the last action be it ending the line or a point added to the last line.
        """
        self.keep_points.undo_last()
        self.draw()
        self.write()

    def end_line(self):
        """
        end the line by inserting an empty line at the end of the list.
        """
        self.keep_points.end_line()
        self.write()

    def toggle_modify(self):
        """
        In modify mode a mouse down selects the nearest line. If 'r' is struck after selecting
        it will remove the line from the annotation list. If 'm' or the modify button are struck
        then it cancels out of the mode.
        """
        self._modify = not self._modify
        self.draw_highlight(None)
        self.draw()

    def set_remove(self):
        """
        Removes the line nearest the point selected, exits edit mode, and redraws the canvas.
        """
        if self._modify:
            self.keep_points.remove_nearest(self.magic_point, self.canvas)
            self.canvas.remove(self.highlight)
            self.highlight = None
            self.toggle_modify()
        self.draw()
        self.write()

    def set_scale_factor(self, sf):
        """
        pass the scale factor through to the line annotations class so that it can scale the lines appropriately to
        the figure scaling.
        :param sf: scale factor, ie if the figure is 2x larger than the native image then sf=2
        """
        self.keep_points.set_scale_factor(sf)
        self.draw()
