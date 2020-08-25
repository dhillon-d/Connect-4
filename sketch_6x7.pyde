"""
Name: Dilraj Dhillon
Main .pyde file which calls upon the draw loop and sets up the mouse press
and mouse release events.
"""

from game_manager import GameManager

LIGHT_GREY = (211, 211, 211)
ROWS = 6
COLUMNS = 7
SLOT_SIZE = 200
SPACE = {'w': COLUMNS * SLOT_SIZE, 'h': (ROWS * SLOT_SIZE) + SLOT_SIZE}

game_manager = GameManager(SPACE, ROWS, COLUMNS, SLOT_SIZE)


def setup():
    size(SPACE['w'], SPACE['h'])
    print('Game start!')
    print('It is red player\'s turn!')


# Draw loop being called once per frame
def draw():
    background(*LIGHT_GREY)
    game_manager.update()


# Only allow manual mouse presses if player turn
def mousePressed():
    if game_manager.player_turn == 0:
        game_manager.handle_mousepress()


# Only allow manual mouse release if player turn
def mouseReleased():
    if game_manager.player_turn == 0:
        game_manager.handle_mouserelease()
