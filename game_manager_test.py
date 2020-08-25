from game_manager import GameManager

ROWS = 6
COLUMNS = 7
SLOT_SIZE = 200
SPACE = {'w': COLUMNS * SLOT_SIZE, 'h': (ROWS * SLOT_SIZE) + SLOT_SIZE}
a = GameManager(SPACE, ROWS, COLUMNS, SLOT_SIZE)


def test_constructor():
    assert a.SPACE == SPACE
    assert a.ROWS == ROWS
    assert a.COLUMNS == COLUMNS
    assert a.SLOT_SIZE == SLOT_SIZE
    assert a.game_end == 0
    assert a.game_counter == 0
    assert a.player_turn == 0
    assert a.disk_list == []
    assert a.column_index == 0
    assert a.row_index == 0
    assert a.empty_slots == [0, 0, 0, 0, 0, 0, 0]
    assert a.disk_stack_height == 0


def test_handle_mouspress():
    a.handle_mousepress()
    assert a.disk_list != []
    assert a.disk_list[-1].hover == 1


def test_announce_player_turn():
    a.announce_player_turn()
    assert a.game_counter != 0


def test_check_empty_slots():
    a.check_empty_slots()
    assert a.empty_slots != [0, 0, 0, 0, 0, 0, 0]
    assert a.empty_slots_counter == [0, 0, 0, 0, 0, 0, 0]

# The rest of the functions can't be tested for since they contain graphical
# commands.
