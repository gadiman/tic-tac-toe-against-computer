import os


class Board:
    def __init__(self):

        self.__board = [" ", " ", " ",
                        " ", " ", " ",
                        " ", " ", " "]

    def display_bord(self):
        "This function prints the board"
        print(" %s | %s | %s " % (self.__board[0], self.__board[1], self.__board[2]))
        print("--------------")
        print(" %s | %s | %s " % (self.__board[3], self.__board[4], self.__board[5]))
        print("--------------")
        print(" %s | %s | %s " % (self.__board[6], self.__board[7], self.__board[8]))

    def update_board(self):
        "This function deletes the old board and prints the new one"
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        self.display_bord()

    def set_player_choose(self, symbol, name, choice):
        choice -= 1
        self.__board[choice] = symbol
        self.update_board()

    def set_computer_choice(self, index):
        self.__board[index] = "O"
        self.update_board()

    def is_full_board(self):
        return self.__board.count(" ") == 0

    def is_empty_cell(self, *index):
        "The function returns true if the indexes it received are empty"
        for it in index:
            if self.__board[it] != " ":
                return False
        return True

    def num_of_marked(self):
        return 9 - self.__board.count(" ")

    def is_marked(self, symbol, *index,):
        "The function returns true if the indexes it received are marked at the symbol"
        for it in index:
            if self.__board[it] != symbol:
                return False
        return True

    def get_row(self, cell_index):
        "This function returns the row that belongs to the index it received"
        if cell_index in range(3):
            return self.__board[0:3]
        if cell_index in range(3, 6):
            return self.__board[3:6]
        if cell_index in range(6, 9):
            return self.__board[6:9]

    def get_col(self, cell_index):
        "This function returns the column that belongs to the index it received"
        if cell_index in range(0, 7, 3):
            return self.__board[0:7:3]
        if cell_index in range(1, 8, 3):
            return self.__board[1:8:3]
        if cell_index in range(2, 9, 3):
            return self.__board[2:9:3]

    def get_hypotenuse(self, cell_index):
        "This function returns the hypotenuse that belongs to the index it received"
        if cell_index in [0, 8]:
            return self.__board[0:9:4]
        elif cell_index in [2, 6]:
            return self.__board[2:7:2]
        else: # Case that cell_index == 4
            return self.__board[0:9:4], self.__board[2:7:2]
