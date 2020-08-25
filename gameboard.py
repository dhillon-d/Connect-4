"""
Name: Dilraj Dhillon
GameBoard class handles the size and positioning of the board.
"""


class GameBoard:
    def __init__(self, SPACE, ROWS, COLUMNS, SLOT_SIZE):
        self.SPACE = SPACE
        self.ROWS = ROWS
        self.COLUMNS = COLUMNS
        self.SLOT_SIZE = SLOT_SIZE
        self.STROKE_WEIGHT = SLOT_SIZE/10
        self.STROKE_COLOR = (0, 0, 0)

    def display(self):
        """
        Displays the board.
        """
        strokeWeight(self.STROKE_WEIGHT)
        stroke(*self.STROKE_COLOR)
        # Vertical bars
        for i in range(self.COLUMNS + 1):
            step = i * self.SLOT_SIZE
            line(0 + step, self.SLOT_SIZE, 0 + step, self.SPACE['h'])
        # Horizontal bars
        for i in range(self.ROWS + 1):
            step = i * self.SLOT_SIZE
            line(0, self.SLOT_SIZE + step,
                 self.SPACE['w'], self.SLOT_SIZE + step)
        pass
