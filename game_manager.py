"""
Name: Dilraj Dhillon
Contains the update loop for the draw function in the .pyde file. Handles
the game state, player turn, and events.
"""

from gameboard import GameBoard
from disk import Disk
import re
import random


class GameManager:
    def __init__(self, SPACE, ROWS, COLUMNS, SLOT_SIZE):
        self.SPACE = SPACE
        self.ROWS = ROWS
        self.COLUMNS = COLUMNS
        self.SLOT_SIZE = SLOT_SIZE
        self.game_end = 0
        self.game_counter = 0
        self.player_turn = 0
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.gameboard = GameBoard(self.SPACE, self.ROWS, self.COLUMNS,
                                   self.SLOT_SIZE)
        self.disk_list = []
        self.disk_array = [[0] * self.COLUMNS for i in range(self.ROWS)]
        self.column_index = 0
        self.row_index = 0
        self.empty_slots_counter = [0] * self.COLUMNS
        # List of how many empty slots in each column
        self.empty_slots = [0] * self.COLUMNS
        self.disk_stack_height = 0
        # random int for computer
        self.r1 = 0

    def update(self):
        """
        Main loop of the game that is constantly called.
        """
        # Display board at beginning of game
        if self.disk_list == [] and self.game_end == 0:
            self.gameboard.display()

        # Announcing player turn and incrementing game counter
        self.announce_player_turn()

        # Array empty slots
        self.check_empty_slots()

        # If Computer players turn, let the computer drop a disk
        IDLE_TIME = 100
        if self.player_turn == 1 and self.game_counter == IDLE_TIME:
            self.computer_turn()
            # Skip to next iteration of draw loop by returning out of loop
            return

        # Drop and display disk_list, reset game counter when last disk
        # has settled, switch players when last disk settled
        self.show_disks()

        # Display board after disk_list have fallen
        self.gameboard.display()

        # Check for 4 disks in a row of the same color if last disk settled
        self.check_hor_vert()

        # Checking diagonally from up and left to down and right for 4 of the
        # same color in a row if last disk settled
        self.check_diag_ul_dr()

        # Checking diagonally from up and right to down and left for 4 of the
        # same color in a row if last disk settled
        self.check_diag_ur_dl()

        # Check for win
        self.check_for_win()

    def input(self, message=''):
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)

    def handle_mousepress(self):
        """
        When the mouse is clicked a disk is appended to the disk list and
        enters the hovering state. Only possible when there are no disks
        on the board or the previous disk has already settled down to ensure
        that the previous disk has landed.
        """
        if self.disk_list == [] or self.disk_list[-1].settled == 1:
            # Player 0 has red chip
            if self.player_turn == 0:
                self.disk_list.append(Disk(self.SPACE, self.SLOT_SIZE,
                                           self.RED))
                self.disk_list[-1].hovering()
            # Player 1 has yellow chip
            if self.player_turn == 1:
                self.disk_list.append(Disk(self.SPACE, self.SLOT_SIZE,
                                           self.YELLOW))
                self.disk_list[-1].hovering()

    def handle_mouserelease(self, mouse_X=None):
        """
        When the mouse button is released the disk enters the falling state
        and the players switch turns. Only possible when the current disk
        is in a hover state and the current column is not full of disks.
        """
        # Use the cursor for the x position if no input parameter
        if mouse_X is None:
            mouse_X = mouseX

        if (self.disk_list[-1].hover == 1 and
           self.empty_slots[mouse_X//self.SLOT_SIZE] != 0):
            self.disk_list[-1].falling()

    def announce_player_turn(self):
        """"
        Announce player turn and increment the game controller.
        """
        if (self.game_counter == 0 and self.player_turn == 0 and
           len(self.disk_list) != 0 and self.disk_list[-1].settled == 1):
            print('It is red player\'s turn!')
            self.game_counter += 1
        elif (self.game_counter == 0 and self.player_turn == 1 and
              len(self.disk_list) != 0 and self.disk_list[-1].settled == 1):
            print('It is yellow player\'s turn!')
            self.game_counter += 1
        else:
            self.game_counter += 1

    def check_empty_slots(self):
        """
        Checks for empty slots in each column in the disk array.
        """
        for row in self.disk_array:
            for column in range(len(row)):
                if type(row[column]) == int:
                    self.empty_slots_counter[column] += 1
        self.empty_slots = self.empty_slots_counter
        self.empty_slots_counter = [0] * self.COLUMNS

    def computer_turn(self):
        """
        A simulated player turn that runs through a typical update loop with
        predetermined values for where to drop the disk.
        """
        # computer AI dropping randomly
        self.r1 = random.randint(0, self.COLUMNS - 1)
        while (self.empty_slots[self.r1] == 0):
            self.r1 = random.randint(0, self.COLUMNS - 1)
        # set mouse_X
        mouse_X = self.r1 * self.SLOT_SIZE + self.SLOT_SIZE/2
        self.handle_mousepress()
        self.disk_list[-1].x = mouse_X
        self.handle_mouserelease(mouse_X)
        self.show_disks(mouse_X)
        self.gameboard.display()
        self.check_hor_vert()
        self.check_diag_ul_dr()
        self.check_diag_ur_dl()
        self.check_for_win()

    def show_disks(self, mouse_X=None):
        """
        Positions and displays the disks on the screen. When the last disk has
        settled the game counter is reset and the player turn switches.
        """
        # Use the cursor for the x position if no input parameter
        if mouse_X is None:
            mouse_X = mouseX

        for disk in self.disk_list:

            # Hover triggered by mouse click
            if disk.hover == 1:
                # Disk positioning
                disk.x = mouse_X
                disk.y = self.SLOT_SIZE/2

            # Falling triggered by mouse release
            elif disk.fall == 1:
                # Array indexes
                self.column_index = disk.x//self.SLOT_SIZE
                self.row_index = self.empty_slots[self.column_index] - 1
                # Disk positioning
                disk.x = ((disk.x//self.SLOT_SIZE) * self.SLOT_SIZE
                          + self.SLOT_SIZE/2)
                disk.y = disk.y + disk.SPEED
                # Stop moving the disk at certain height and add to array
                self.disk_stack_height = (self.empty_slots[self.column_index]
                                          * self.SLOT_SIZE
                                          + self.SLOT_SIZE/2)
                # Condition from falling to settled, add disk to disk array,
                # reset game counter to 0, and switch players
                if disk.y == self.disk_stack_height:
                    disk.settling()
                    self.disk_array[self.row_index][self.column_index] = disk
                    self.game_counter = 0
                    if self.player_turn == 0:
                        self.player_turn = 1
                    else:
                        self.player_turn = 0

            # Display current disk in disk list regardless of state
            disk.display()

    def check_hor_vert(self):
        """
        Check for 4 disks of the same color in a row horizontally and
        vertically after the last disk has settled.
        """
        if len(self.disk_list) >= 1 and self.disk_list[-1].settled == 1:
            count_red = 0
            count_yellow = 0
            # Checking horizontally for 4 of the same color in a row
            for i in range(self.COLUMNS):
                if (self.disk_array[self.row_index][i] != 0 and
                   self.disk_array[self.row_index][i].COLOR == self.RED):
                    count_red += 1
                    count_yellow = 0
                elif (self.disk_array[self.row_index][i] != 0 and
                      self.disk_array[self.row_index][i].COLOR == self.YELLOW):
                    count_yellow += 1
                    count_red = 0
                # Encounter an empy space reset counter
                else:
                    count_red = 0
                    count_yellow = 0
                # 4 in a row
                if count_red >= 4 or count_yellow >= 4:
                    self.game_end = 1
                    break
            # Checking vertially for 4 of the same color in a row
            for i in range(self.ROWS):
                if (self.disk_array[i][self.column_index] != 0 and
                   self.disk_array[i][self.column_index].COLOR == self.RED):
                    count_red += 1
                    count_yellow = 0
                elif (self.disk_array[i][self.column_index] != 0 and
                      self.disk_array[i][self.column_index].COLOR ==
                      self.YELLOW):
                    count_yellow += 1
                    count_red = 0
                # Encounter an empy space reset counter
                else:
                    count_red = 0
                    count_yellow = 0
                # 4 in a row
                if count_red >= 4 or count_yellow >= 4:
                    self.game_end = 1
                    break

    def check_diag_ul_dr(self):
        """
        Check for 4 disks of the same color consecutively diagonally after
        the last disk has settled. Checks from up and left to down and right.
        """
        if len(self.disk_list) >= 1 and self.disk_list[-1].settled == 1:
            close_edge = min(self.row_index, self.column_index)
            up_left_r = self.row_index - close_edge
            up_left_c = self.column_index - close_edge
            # While loop iterator and color counter
            i = 0
            count_red = 0
            count_yellow = 0
            while True:
                try:
                    if (self.disk_array[up_left_r + i][up_left_c + i] != 0
                        and
                        self.disk_array[up_left_r + i][up_left_c + i].COLOR
                       == self.RED):
                        count_red += 1
                        count_yellow = 0
                    elif (self.disk_array[up_left_r + i][up_left_c + i] != 0
                            and
                            self.disk_array[up_left_r + i][up_left_c + i].COLOR
                            == self.YELLOW):
                        count_yellow += 1
                        count_red = 0
                    # Encounter an empy space reset counter
                    else:
                        count_red = 0
                        count_yellow = 0
                    # 4 in a row
                    if count_red >= 4 or count_yellow >= 4:
                        self.game_end = 1
                        break
                # Index out of range error, since in an infinite while loop
                except Exception:
                    break
                # Increase while loop iterator
                i += 1

    def check_diag_ur_dl(self):
        """
        Check for 4 disks of the same color consecutively diagonally after
        the last disk has settled. Checks from up and right to down and left.
        """
        if len(self.disk_list) >= 1 and self.disk_list[-1].settled == 1:
            close_edge = min(self.row_index, self.COLUMNS - self.column_index
                             - 1)
            up_right_r = self.row_index - close_edge
            up_right_c = self.column_index + close_edge
            # While loop iterator and color counter
            i = 0
            count_red = 0
            count_yellow = 0
            while True:
                try:
                    if (self.disk_array[up_right_r + i][up_right_c - i] != 0
                        and
                        self.disk_array[up_right_r + i][up_right_c - i].COLOR
                       == self.RED):
                        count_red += 1
                        count_yellow = 0
                    elif (self.disk_array[up_right_r + i][up_right_c - i] != 0
                            and
                            self.disk_array[up_right_r + i][up_right_c - i].
                            COLOR == self.YELLOW):
                        count_yellow += 1
                        count_red = 0
                    # Encounter an empy space reset counter
                    else:
                        count_red = 0
                        count_yellow = 0
                    # 4 in a row
                    if count_red >= 4 or count_yellow >= 4:
                        self.game_end = 1
                        break
                # Index out of range error, since in an infinite while loop
                except Exception:
                    break
                # Increase while loop iterator
                i += 1

    def check_for_win(self):
        """
        Check for a win by either no more empty spots remaining or the
        game end state turning true. Prompts the user for name and the wins
        are saved to a text file.
        """
        if self.empty_slots == [0] * self.COLUMNS:
            print("Game Over!")
            print("Tie!")
            noLoop()
        if self.game_end == 1:
            print("Game Over!")
            name = self.input('enter your name')
            # Previous player has just won before player switch
            if name and self.player_turn == 1:
                print(name + ' has won!')
                # Write text file
                self.user_score_text(name)
            # Previous player has just won before player switch
            elif name and self.player_turn == 0:
                print('Computer has won!')
            else:
                print(name)  # Canceled dialog will print None
            noLoop()

    def user_score_text(self, name):
        """
        Update the text file with the correct wins or create the text file
        if one doesn't already exist.
        """
        # grab dictionary from file
        try:
            f = open('scores.txt', 'r')
            text = f.read()
            # names as list where each index is a string name
            names_from_text = re.findall(r"([\w ]*(?= \d))[^'']", text)
            # wins as list where each index is a string number
            wins_from_text = re.findall(r"\d", text)
            # dictionary with keys as names and values as integers counts
            dict_wins = {}
            for i in range(len(names_from_text)):
                dict_wins[names_from_text[i]] = int(wins_from_text[i])
            f.close()
        # File doesn't exist create empty dictionary
        except Exception:
            dict_wins = {}
        # if dict exists from file then increment, otherwise add dictionary
        # list to text
        finally:
            # increment win if name exists in dictionary
            try:
                dict_wins[name] += 1
            # otherwise create dictionary
            except Exception:
                dict_wins[name] = 1
            # order the dictionary into a list
            dict_list = list(dict_wins.items())
            dict_list = sorted(dict_list, key=lambda x: x[1], reverse=True)
            f = open('scores.txt', 'w')
            # put updated list into text
            for i in dict_list:
                f.write(i[0] + ' ' + str(i[1]) + '\n')
            f.close()
