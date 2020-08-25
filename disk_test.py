from disk import Disk

ROWS = 6
COLUMNS = 7
SLOT_SIZE = 200
SPACE = {'w': COLUMNS * SLOT_SIZE, 'h': (ROWS * SLOT_SIZE) + SLOT_SIZE}
COLOR = (0, 0, 0)
a = Disk(SPACE, SLOT_SIZE, COLOR)


def test_constructor():
    assert a.hover == 0
    assert a.fall == 0
    assert a.settled == 0
    assert a.x == 0
    assert a.y == 0
    assert a.width == SLOT_SIZE
    assert a.height == SLOT_SIZE
    assert a.SPEED == 100


def test_hovering():
    a.hovering()
    assert a.hover == 1


def test_falling():
    a.falling()
    assert a.fall == 1


def test_settling():
    a.settling()
    assert a.settled == 1

# The rest of the functions can't be tested for since they contain graphical
# commands.
