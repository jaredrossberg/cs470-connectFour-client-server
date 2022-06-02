# This holds all relevant functions of the game. 
# (calculating possible moves, a player taking a turn, 
# keeping track of game state, GUI, etc.)
import numpy as np
import tkinter as tk

class GameState:
    def __init__(self, board, turn):
        self.board_height = 6
        self.board_width = 7
        self.board = board
        self.turn = turn # Whose turn is it
        self.game_over = False

    def make_move(self, move):
        """
        This function will execute the move (integer column number) on the given board, 
        where the acting player is given by player_number
        """
        if not self.game_over:
            valid_moves = self.get_valid_moves()
            if move in valid_moves:
                row = 0
                while row < self.board_height and self.board[row,move] == 0:
                    row += 1
                self.board[row-1,move] = self.turn

                if self.is_winning_state():
                    self.game_over = True
                self.turn = 1 if self.turn != 1 else 2

                return row - 1

            else:
                err = 'Invalid move by player {}. Column {}'.format(self.turn, move)
                raise Exception(err)

    def is_game_over(self):
        return self.is_winning_state(1) or self.is_winning_state(2)

    def get_valid_moves(self):
        valid_moves = []

        for col in range(self.board_width):
            for row in range(self.board_height):
                if self.board[row][col] == 0:
                    valid_moves.append(col)
                    break

        return valid_moves
    
    def is_winning_state(self, player_num=None):
        """
        This function will tell if the player_num player is
        winning in the board that is input
        """
        if player_num is None:
            player_num = self.turn

        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_vertical(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(self.board) or
                check_vertical(self.board) or
                check_diagonal(self.board))


class GameGUI:
    def __init__(self):
        self.colors = ['yellow', 'red']
        self.gui_board = []

        #https://stackoverflow.com/a/38159672
        self.root = tk.Tk()
        self.root.title('Connect 4')
        self.player_string = tk.Label(self.root, text="Player 1")
        self.player_string.pack()
        self.c = tk.Canvas(self.root, width=700, height=600)
        self.c.pack()

        for row in range(0, 700, 100):
            column = []
            for col in range(0, 700, 100):
                column.append(self.c.create_oval(row, col, row+100, col+100, fill=''))
            self.gui_board.append(column)

        # FIXME: get rid of this
        # tk.Button(root, text='Next Move', command=self.make_move).pack()

        # self.root.mainloop()
        self.updateGUI()

    def updateGUI(self):
        self.root.update_idletasks()
        self.root.update()

    def placePiece(self, move, update_row, player_num):
        self.c.itemconfig(self.gui_board[move][update_row], fill=self.colors[player_num - 1])
        self.updateGUI()
    
    def changeTurn(self, player_num):
        turnText = "Player " + str(player_num)
        self.player_string.configure(text=turnText)
        self.updateGUI()
    
    def set_winner(self, player_num):
        self.player_string.configure(text='Player ' + str(player_num) + ' wins!')
        self.updateGUI()



def messageToBoard(server_msg):
    return np.flip(np.array([int(x) for x in server_msg[4:46]]).reshape(6, 7), 0)

def boardToMessage(state):
    message = ''
    for row in state.board:
        for cellVal in row:
            message += str(cellVal) + '\n'

    return message

def generateNewBoard():
    return np.zeros([6,7]).astype(np.uint8)

