from Board import Board
import random


class Game:
    def __init__(self):
        self.__selected_cell = None # Keeps the cell the computer is going to select
        self.board = Board()
        self.player = Player("Enter your name please:\n", "X")

    def start_game(self):
        self.board.display_bord()
        turn = random.randint(0, 1)  # turn==1 ->player , turn == 0 -> computer

        if turn == 0:  # computer starts
            self.board.set_computer_choice(random.randint(0, 8)) # chooses a random cell
            print("The computer starts")
            turn = 1 - turn  # switch  player

        while True:
            if turn == 1: # The player's turn
                input_ = self.valid_input(self.player.name)
                while not self.board.is_empty_cell(input_ - 1): # Until the player chooses an empty cell
                    self.board.update_board() # Remove the old output
                    print("Choose an empty cell only\n")
                    input_ = self.valid_input(self.player.name)
                self.board.set_player_choose(self.player.symbol, self.player.name, input_) # Mark the selection in the board

            else: # The computer's turn
                self.next_move() # Next move of the computer

            turn = 1 - turn  # Switch player

            if self.optional_seq("O", "O") or self.optional_seq("X", "X"):  # Someone won - Game over
                break
            if self.board.is_full_board():  # The board is full - Game over
                print("The game ended in a draw")
                return

        if not 1 - turn:
            print("The computer won")
        else:
            print(self.player.name + " won")

    def next_move(self):
        "This function realizes the computer's algorithm for cell selection"

        # choose the middle cell if its empty - In case that player starts
        if self.board.num_of_marked() == 1 and self.board.is_empty_cell(4):
            self.board.set_computer_choice(4)

        # check if computer have sequence of tow "O" and complete it
        elif self.optional_seq(" ", "O"):
            self.board.set_computer_choice(self.__selected_cell)

        # check if player have sequence of tow "X" and blocks it
        elif self.optional_seq(" ", "X"):
            self.board.set_computer_choice(self.__selected_cell)

        # Looking for a cell that its column and its row with single mark and choose it
        elif self.common_cell_seq():
            self.board.set_computer_choice(self.__selected_cell)

        # If this is the fourth turn in the game and the middle cell is "O"
        elif self.board.num_of_marked() == 3 and self.board.is_marked("O", 4):

            # Looking for a corner cell that is in the column or row of "X"
            if self.board.is_marked("X", 0, 8) or self.board.is_marked("X", 2, 6):
                self.choose_empty_cell_from(1, 3, 5, 7)

            elif self.board.is_marked("X", 1, 7) or self.board.is_marked("X", 3, 5):
                self.choose_empty_cell_from(0, 2, 6, 8)

            # Looking for a corner cell that is in the column and row of the X's
            else:
                for it in [0, 2, 6, 8]:
                    if not self.board.is_empty_cell(it):
                        continue
                    if self.board.get_row(it).count("X") == 1 and self.board.get_col(it).count("X") == 1:
                        self.board.set_computer_choice(it)
                        break

        # Looking for a corner whose column and row are empty
        elif self.empty_common_seq_cell():
            self.board.set_computer_choice(self.__selected_cell)

        # If the middle cell is empty - choose it
        elif self.board.is_empty_cell(4):
            self.board.set_computer_choice(4)

        # Looking for an empty row or hypotenuse and choose the corner
        elif self.optional_seq_row(" ", " ") or self.optional_seq_hypotenuse(" ", " "):
            self.board.set_computer_choice(self.__selected_cell)

        elif self.optional_seq_row("O", " ", range(1, 8, 3)) \
                or self.optional_seq_col("O", " ", range(3, 6)) \
                or self.optional_seq_hypotenuse("O", " ", True):
            self.board.set_computer_choice(self.__selected_cell)

        # Looking for an empty corner empty cell
        elif len([it for it in [0, 2, 6, 8] if self.board.is_empty_cell(it)]) > 0:
            self.choose_empty_cell_from(0, 2, 6, 8)
        else:  # mark an empty cell
            self.choose_empty_cell_from(*range(0, 9))


    def common_cell_seq(self):
        "This function looks for an empty cell that its  column and row contain one 'O' "

        counter = 0
        for it in range(9):
            if not self.board.is_empty_cell(it):
                continue
            if self.board.get_row(it).count("O") == 1 and "X" not in self.board.get_row(it):
                counter += 1
            if self.board.get_col(it).count("O") == 1 and "X" not in self.board.get_col(it):
                counter += 1
            if it == 4:  # The middle cell - 2 hypotenuses
                if self.board.get_hypotenuse(it)[0].count("O") == 1 \
                        and "X" not in self.board.get_hypotenuse(it)[0]:
                    counter += 1
                if self.board.get_hypotenuse(it)[1].count("O") == 1 \
                        and "X" not in self.board.get_hypotenuse(it)[1]:
                    counter += 1
            elif it in [0, 2, 6, 8]:
                if self.board.get_hypotenuse(it).count("O") == 1 \
                        and "X" not in self.board.get_hypotenuse(it):
                    counter += 1

            if counter >= 2:
                self.__selected_cell = it
                return True
        return False

    def empty_common_seq_cell(self):
        "This function looks for an empty corner whose its row and column are empty"
        for it in [0, 2, 6, 8]:
            if self.board.get_row(it).count(" ") == 3 and self.board.get_col(it).count(" ") == 3:
                self.__selected_cell = it
                return True
        return False

    def optional_seq(self, single_sym, rest_sym):
        "This function looks for a possible sequence of 1- single_sym and 2- rest_sem"
        return self.optional_seq_row(single_sym, rest_sym) \
               or self.optional_seq_col(single_sym, rest_sym) \
               or self.optional_seq_hypotenuse(single_sym, rest_sym)

    def optional_seq_row(self, single_sym, rest_sym, range_=range(9)):
        "This function looks for a possible sequence of 1- single_sym and 2- rest_sem in row"

        num_of_sym = 3 if single_sym == rest_sym else 2 # If they are equal then we are looking for a sequence of 3

        for it in range_:
            if not self.board.is_marked(single_sym, it):
                continue
            if self.board.get_row(it).count(rest_sym) == num_of_sym:
                self.__selected_cell = it
                return True
        return False

    def optional_seq_col(self, single_sym, rest_sym, range_=range(9)):
        "This function looks for a possible sequence of 1- single_sym and 2- rest_sem in column"

        num_of_sym = 3 if single_sym == rest_sym else 2 # If they are equal then we are looking for a sequence of 3

        for it in range_:
            if not self.board.is_marked(single_sym, it):
                continue
            if self.board.get_col(it).count(rest_sym) == num_of_sym:
                self.__selected_cell = it
                return True
        return False

    def optional_seq_hypotenuse(self, single_sym, rest_sym, only_middle=False):
        "This function looks for a possible sequence of 1- single_sym and 2- rest_sem in hypotenuse"

        num_of_sym = 3 if single_sym == rest_sym else 2 # If they are equal then we are looking for a sequence of 3

        if self.board.is_marked(single_sym, 4):
            if self.board.get_hypotenuse(4)[0].count(rest_sym) == num_of_sym and self.board:
                self.__selected_cell = 4
                return True
            if self.board.get_hypotenuse(4)[1].count(rest_sym) == num_of_sym:
                self.__selected_cell = 4
                return True

        if only_middle: # In case the search is only in the main diagonals
            return False

        for it in [0, 2, 6, 8]:
            if not self.board.is_marked(single_sym, it):
                continue
            if self.board.get_hypotenuse(it).count(rest_sym) == num_of_sym:
                self.__selected_cell = it
                return True

        return False

    def choose_empty_cell_from(self, *options):
        "This function selects the first cell that is empty"
        for it in options:
            if self.board.is_empty_cell(it):
                self.board.set_computer_choice(it)
                return

    def valid_input(self, name):
        "This function is responsible for checking the correctness of the input"
        while True:
            try:
                input_ = input(name + ' ,enter your choice please(1-9):\n ')
                input_ = int(input_)
                if 0 < input_ < 10:
                    return input_
                else:
                    self.board.update_board()
                    print("Choose an empty cell in range 1-9\n")
            except (ValueError, TypeError):
                self.board.update_board()
                print("Not valid input, please try again\n")


class Player:
    def __init__(self, output, symbol_):
        self.name = input(output)
        self.symbol = symbol_
