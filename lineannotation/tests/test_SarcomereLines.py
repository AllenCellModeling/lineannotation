from kivy.tests.common import UnitTestTouch
import pathlib
import pytest
from random import random
from ..SarcomereLines import SarcomereLines

TEST_FILE = "testme.annot_txt"


@pytest.fixture
def create_class():
    test_file = pathlib.PosixPath(TEST_FILE)
    test_file.unlink() if test_file.exists() else None
    return test_file, SarcomereLines(TEST_FILE)


@pytest.fixture
def create_window():  # window defaults to be 800x600
    from kivy.base import EventLoop
    EventLoop.ensure_window()
    window = EventLoop.window
    return window


@pytest.fixture
def segment_maker():

    def _add_line(sl, x1, y1, x2, y2):
        a = UnitTestTouch(x1, y1)
        a.pos = (x1, y1)  # not sure why pos isn't assigned but I can force it.
        b = UnitTestTouch(x2, y2)
        b.pos = (x2, y2)  # not sure why pos isn't assigned but I can force it.
        sl.add_point(a)
        sl.add_point(b)
        sl.end_line()
        return sl

    return _add_line


def check_line_eq(a, b):
    # for i in range(0, 2):
    #         print("(", a[i][0], ", ", a[i][1], ") =?= (", b[i][0], ", ", b[i][1], ")")
    return a[0][0] == b[0][0] and a[0][1] == b[0][1] and a[1][0] == b[1][0] and a[1][1] == b[1][1]


def test_no_file(create_class):
    test_file, sl = create_class
    assert test_file.exists() is False


def test_file_exists(create_class):
    test_file, sl = create_class
    sl.write_file(TEST_FILE, (2048, 2048))
    assert test_file.exists() is True


def test_add_point(create_class, create_window):
    test_file, sl = create_class
    window = create_window

    touch = UnitTestTouch(*[s*random() for s in window.size])
    sl.add_point(touch)
    assert len(sl.lines[0]) == 1


def test_remove(create_class, create_window):
    test_file, sl = create_class
    window = create_window
    print("size: ", window.size)
    for i in range(0, 10):
        touch = UnitTestTouch(*[s*random() for s in window.size])
        sl.add_point(touch)
    sl.undo_last()
    assert len(sl.lines[0]) == 9


def test_4_lines(create_class, create_window, segment_maker):
    test_file, sl = create_class
    window = create_window

    #draw segments making a box that doesn't connect on the corners
    segment_maker(sl, 200, 100, 400, 100)
    segment_maker(sl, 500, 200, 500, 400)
    segment_maker(sl, 400, 500, 200, 500)
    segment_maker(sl, 100, 400, 100, 200)

    test_touch = UnitTestTouch(510, 210)
    test_touch.pos = (510, 210)
    n_idx, n_line = sl.select_nearest_line(test_touch.pos)
    assert n_idx == 1


def test_remove_line(create_class, create_window, segment_maker):
    test_file, sl = create_class
    window = create_window

    #draw segments making a box that doesn't connect on the corners
    segment_maker(sl, 200, 100, 400, 100)
    segment_maker(sl, 500, 200, 500, 400)
    segment_maker(sl, 400, 500, 200, 500)
    segment_maker(sl, 100, 400, 100, 200)

    test_touch = UnitTestTouch(510, 210)
    test_touch.pos = (510, 210)

    sl.remove_nearest(test_touch, None)

    assert check_line_eq(sl.lines[0], [(200, 100), (400, 100)])
    assert check_line_eq(sl.lines[1], [(400, 500), (200, 500)])
    assert check_line_eq(sl.lines[2], [(100, 400), (100, 200)])
    assert len(sl.lines[3]) == 0

