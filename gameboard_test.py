from gameboard import GameBoard

ROWS = 6
COLUMNS = 7
SLOT_SIZE = 200
SPACE = {'w': COLUMNS * SLOT_SIZE, 'h': (ROWS * SLOT_SIZE) + SLOT_SIZE}
a = GameBoard(SPACE, ROWS, COLUMNS, SLOT_SIZE)


def test_constructor():
    assert a.SPACE == SPACE
    assert a.ROWS == ROWS
    assert a.COLUMNS == COLUMNS
    assert a.SLOT_SIZE == SLOT_SIZE
    assert a.STROKE_WEIGHT == SLOT_SIZE/10
    assert a.STROKE_COLOR == (0, 0, 0)

# The rest of the functions can't be tested for since they contain graphical
# commands.
