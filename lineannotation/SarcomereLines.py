import json
from kivy.graphics import Color, Ellipse, InstructionGroup, Line
import math


class SarcomereLines(object):
    """SarcomereLines

    This class is a queue. It holds on to the list of points that have been clicked.
    It also constructs the drawn lines that get added to the Picture Canvas and handles
    the logic of when to clear the lines from the canvas etc.

    """

    def __init__(self, fname):
        """
        Initialize SarcomereLines with a file name
        :param fname: name of file with lines, if file doesn't exist it is created.
        """
        try:
            with open(fname, 'r') as fp:
                fp.readline()  # Discard the image size for now
                self.lines = json.load(fp=fp)
            fp.closed
        except FileNotFoundError:
            self.lines = [[]]

        self.d = 5  # diameter of any point drawn
        self.lw = 2 # the width of drawn lines
        self.instructions = None  # container to hold the lines drawing object
        self.highlight = None  # container to hold the highlight lines object
        self.scale_factor = 1.0  # how many fold the image is zoomed from native.

    def set_scale_factor(self, sf):
        """
        set the scale factor so the coordinates can be scaled to the scaled image size.
        :param sf: scale factor, if the image is 2x native size then sf = 2
        """
        self.scale_factor = sf

    def map_point(self, point):
        """
        the coordinate system of the point is that of the scaled image. Thus it needs to be transformed to the
        native image size which is the coordinate system used within the class.
        :param point: point.pos is are the coordinates in the scaled image
        :return: the coordinates in the native resolution
        """
        pos = point
        pos_x = pos[0] / self.scale_factor
        pos_y = pos[1] / self.scale_factor
        pos = (pos_x, pos_y)
        return pos

    def end_line(self):
        """
        end the current line.
        """
        if len(self.lines[-1]) > 0:
            self.lines.append([])

    def add_point(self, point):
        """
        add point.pos to the end of the last line in the end of the list.
        :param point: this is a kivy point object, pos contains the
        global coordinates in the image frame
        """
        spos = self.map_point(point.pos)
        self.lines[-1].append(spos)

    def undo_last(self):
        """
        undo the last operation, specifically remove an empty list or remove the last point added.
        it can be performed repeatably until there are no points in the structure.
        """
        if len(self.lines[-1]) == 0 and len(self.lines) > 1:
            self.lines.pop()  # undo the end of list
        else:
            if len(self.lines[-1]) > 0:
                self.lines[-1].pop()

    def write_file(self, fname, img_size):
        """
        write out all the points to the file and include the image_size as a header
        :param fname: the file name / same as the image but with the extension .annot_txt
        :param img_size: the (x,y) size of the local coordinate system used.
        """
        with open(fname, "w") as fp:
            json.dump(img_size, fp)
            fp.write("\n")
            json.dump(self.lines, fp)
        fp.closed

    def remove_nearest(self, point, canvas):
        """
        remove the line nearest to the selected point
        :param point: the point nearest the line to remove
        :param canvas: the drawing canvas that displays the image
        """
        if len(self.lines) == 1 and len(self.lines[0]) == 0: return
        spos = self.map_point(point.pos)
        i, r_line = self.select_nearest_line(spos)
        self.lines.remove(r_line)
        canvas.remove(self.highlight) if canvas else None
        self.highlight = None

    def highlight_nearest(self, point, canvas):
        canvas.remove(self.highlight)
        self.highlight = None

    def highlight_nearest(self, point, canvas):
        """
        highlight the line nearest the point clicked
        :param point: the point selected
        :param canvas: where the image and lines are displayed
        """
        if len(self.lines) == 1 and len(self.lines[0]) == 0:
            return
        spos = self.map_point(point.pos)
        i, r_line = self.select_nearest_line(spos)
        self.draw_highlight(r_line, canvas)

    def draw_highlight(self, line, canvas):
        """
        draw the selected line in yellow to highlight it and allow the user to decide if they want to remove it.
        :param line: the line that was selected
        :param canvas: the drawing canvas
        """
        if self.highlight:
            canvas.remove(self.highlight)
            self.highlight = None
        if line:
            self.highlight = InstructionGroup()
            self.highlight.add(Color(1, 1, 0))
            self.highlight.add(
                Line(points=[c*self.scale_factor for p in line for c in p],
                     width=self.lw)
            )
            canvas.add(self.highlight)

    def draw(self, canvas):
        """
        redraw all the lines and points
        :param canvas: the image canvas to draw on
        """
        if self.instructions:
            canvas.remove(self.instructions)
        self.instructions = InstructionGroup()
        for line in self.lines:
            if len(line) > 1:
                self.instructions.add(Color(0, 1, 0))
                self.instructions.add(
                    Line(points=[c * self.scale_factor for p in line for c in p],
                         width=self.lw)
                )
            self.instructions.add(Color(1, 0, 0))
            for p in line:
                self.instructions.add(
                    Ellipse(pos=(p[0] * self.scale_factor - self.d / 2, p[1] * self.scale_factor - self.d / 2),
                            size=(self.d, self.d))
                )
        canvas.add(self.instructions)

    def select_nearest_line(self, p):
        """
        Select the line nearest the point submitted
        :param p: the selected point in native coordinates
        :return: the (index, line) of the selected line in the list of lines
        """
        line_idx = 0
        p_dist = 100000.0
        for idx, line in enumerate(self.lines):
            for pxy in line:
                d = self.dist(p, pxy)
                if d < p_dist:
                    line_idx = idx
                    p_dist = d
        return line_idx, self.lines[line_idx]

    def dist(self, p1, p2):
        """
        compute the distance between the points.
        :param p1: point 1 (x1, y1)
        :param p2: point 2 (x2, y2)
        :return: distance between p1 and p2
        """
        dx = float(p1[0]) - float(p2[0])
        dy = float(p1[1]) - float(p2[1])
        return math.sqrt(dx * dx + dy * dy)
