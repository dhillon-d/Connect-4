"""
Name: Dilraj Dhillon
Disk class handles the size and color of the disk. Also handles the various
states of the disk including whether it is hovering, falling, or has settled.
"""


class Disk:
    def __init__(self, SPACE, SLOT_SIZE, COLOR):
        self.SPACE = SPACE
        self.hover = 0
        self.fall = 0
        self.settled = 0
        self.COLOR = COLOR
        self.x = 0
        self.y = 0
        self.width = SLOT_SIZE
        self.height = SLOT_SIZE
        self.SPEED = 100

    def hovering(self):
        """
        Set the disk state to hover.
        """
        self.hover = 1
        self.fall = 0
        self.settled = 0

    def falling(self):
        """
        Set the disk state to fall.
        """
        self.hover = 0
        self.fall = 1
        self.settled = 0

    def settling(self):
        """
        Set the disk state to settled.
        """
        self.hover = 0
        self.fall = 0
        self.settled = 1

    def display(self):
        fill(*self.COLOR)
        strokeWeight(0)
        ellipse(self.x, self.y, self.width, self.height)
