import pathlib
import pytest
from random import random
from .helper_classes import Pointpos
from ..SarcomereLines import SarcomereLines

TEST_FILE = "testme.annot_txt"


@pytest.fixture
def create_class():
    test_file = pathlib.PosixPath(TEST_FILE)
    test_file.unlink() if test_file.exists() else None
    return test_file, SarcomereLines(TEST_FILE)


@pytest.fixture
def segment_maker():

    def _add_line(sl, x1, y1, x2, y2):
        a = Pointpos(x1, y1)
        b = Pointpos(x2, y2)
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


def test_add_point(create_class):
    test_file, sl = create_class

    touch = Pointpos(*[s*random() for s in (1024, 1024)])
    sl.add_point(touch)
    assert len(sl.lines[0]) == 1


def test_remove(create_class):
    test_file, sl = create_class
    for i in range(0, 10):
        touch = Pointpos(*[s*random() for s in (1024, 1024)])
        sl.add_point(touch)
    sl.undo_last()
    assert len(sl.lines[0]) == 9


def test_4_lines(create_class, segment_maker):
    test_file, sl = create_class

    #draw segments making a box that doesn't connect on the corners
    segment_maker(sl, 200, 100, 400, 100)
    segment_maker(sl, 500, 200, 500, 400)
    segment_maker(sl, 400, 500, 200, 500)
    segment_maker(sl, 100, 400, 100, 200)

    test_touch = Pointpos(510, 210)
    n_idx, n_line = sl.select_nearest_line(test_touch)
    assert n_idx == 1


def test_remove_line(create_class, segment_maker):
    test_file, sl = create_class

    #draw segments making a box that doesn't connect on the corners
    segment_maker(sl, 200, 100, 400, 100)
    segment_maker(sl, 500, 200, 500, 400)
    segment_maker(sl, 400, 500, 200, 500)
    segment_maker(sl, 100, 400, 100, 200)

    test_touch = Pointpos(510, 210)

    sl.remove_nearest(test_touch, None)

    assert check_line_eq(sl.lines[0], [(200, 100), (400, 100)])
    assert check_line_eq(sl.lines[1], [(400, 500), (200, 500)])
    assert check_line_eq(sl.lines[2], [(100, 400), (100, 200)])
    assert len(sl.lines[3]) == 0

def test_true():
    assert True
