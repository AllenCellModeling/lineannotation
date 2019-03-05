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

        self.d = 5
        self.lw = 3
        self.instructions = None  # container to hold the lines drawing object
        self.highlight = None  # container to hold the highlight lines object
        self.scale_factor = 1.0

    def set_scale_factor(self, sf):
        self.scale_factor = sf

    def map_point(self, point):
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
        print(str(spos))

    def undo_last(self):
        if len(self.lines[-1]) == 0 and len(self.lines) > 1:
            self.lines.pop()  # undo the end of list
        else:
            if len(self.lines[-1]) > 0:
                self.lines[-1].pop()

    def write_file(self, fname, img_size):
        with open(fname, "w") as fp:
            json.dump(img_size, fp)
            fp.write("\n")
            json.dump(self.lines, fp)
        fp.closed

    def remove_nearest(self, point, canvas):
        if len(self.lines) == 1 and len(self.lines[0]) == 0: return
        spos = self.map_point(point.pos)
        i, r_line = self.select_nearest_line(spos)
        self.lines.remove(r_line)
        canvas.remove(self.highlight)
        self.highlight = None

    def highlight_nearest(self, point, canvas):
        if len(self.lines) == 1 and len(self.lines[0]) == 0:
            return
        spos = self.map_point(point.pos)
        i, r_line = self.select_nearest_line(spos)
        self.draw_highlight(r_line, canvas)

    def draw_highlight(self, line, canvas):
        if self.highlight:
            canvas.remove(self.highlight)
            self.highlight = None
        if line:
            self.highlight = InstructionGroup()
            self.highlight.add(Color(1, 1, 0))
            self.highlight.add(
                Line(points=[c for p in line for c in p],
                     width=self.lw)
            )
            canvas.add(self.highlight)

    def draw(self, canvas):
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
        dx = float(p1[0]) - float(p2[0])
        dy = float(p1[1]) - float(p2[1])
        return math.sqrt(dx * dx + dy * dy)
