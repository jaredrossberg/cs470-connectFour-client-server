# This has code for human, random, and ai players and calls functions from connect4game.py It should not worry about connections at all

from cgitb import small
from time import sleep
import game

import numpy as np
import random as rand


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number  #This is the id of the player this AI is in the game
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.other_player_number = 1 if player_number == 2 else 2  #This is the id of the other player

        self.board_height = 6
        self.board_width = 7

    def make_move(self, state):
        '''
        This is the only function that needs to be implemented for the lab!
        The bot should take a game state and return a move. (0-6)

        The 'state' parameter has two useful member variables. 
        The first is 'board', which is an 6x7 array of 0s, 1s, and 2s. 
        If a spot has a 0 that means it is unoccupied. If there is a 1 that 
        means the spot has one of player 1's pieces. If there is a 2 on the 
        spot that means that spot has one of player 2's pieces. The other 
        useful member variable is "turn", which is 1 if it's player 1's turn 
        and 2 if it's player 2's turn.

        The 'state' object also has a nice method called get_valid_moves.
        It returns a list of valid moves from that state.

        Move should be an integer of the column to drop the piece in.
        '''
        
        valid_moves = state.get_valid_moves()
        
        if len(valid_moves) == 1:
            print('Choosing only move {}'.format(move))
            return valid_moves[0]
        
        for move in valid_moves:
            if self.can_win(move, state, state.turn):
                print('Choosing winning move {}. Valid moves: {}'.format(move, valid_moves))
                return move

        
        for move in range(0,self.board_width):
            subset = []
            if self.can_win(move, state, 2 / state.turn):
                subset.append(move)
                print('Preventing winning move {}. Valid moves: {}. Losing moves: {}'.format(move, valid_moves, subset))
                return self.search(state, state.turn, 1, subset)[1]

                #print('Preventing winning move {}. Valid moves: {}'.format(move, valid_moves))
                #return move

        #move = rand.choice(valid_moves) # Moves randomly...for now
        #print('Choosing random move {}. Valid moves: {}'.format(move, valid_moves))
        #return move'''

        move = self.search(state, state.turn, 1)[1]
        print('Choosing random move {}. Valid moves: {}'.format(move, valid_moves))
        return move


    def search(self, state, player, depth, valid_moves=None):
        #print('Searching depth', depth)
        if valid_moves == None:
            valid_moves = state.get_valid_moves()
        if len(valid_moves) == 0:
            return (None,None)
        m = {}
        for move in valid_moves:
            #print('\tSearching move', move)
            if self.can_win(move, state, player):
                m[move] = depth

            if depth >= 4:
                m[move] = None
            else:
                row = 0
                while row < self.board_height and state.board[row,move] != 0:
                    row += 1
                state.board[row,move] = player
                m[move] = self.search(state, 2 / player, depth+1)[0]
                if m[move] != None:
                    m[move] *= -1
                state.board[row,move] = 0

        smallest_positive = None
        greatest_negative = None
        tie = []
        for move in valid_moves:
            if m[move] == None:
                tie.append(move)
            elif m[move] > 0 and (smallest_positive == None or m[move] < m[smallest_positive]):
                smallest_positive = move
            elif m[move] < 0 and (greatest_negative == None or m[move] < m[greatest_negative]):
                greatest_negative = move
        if smallest_positive != None:
            return (m[smallest_positive], move)
        if len(tie) > 0:
            move = rand.choice(tie)
            return (None, move)
            #return (m[tie], move)
        return (m[greatest_negative], move)

            


    
    def can_win(self, move, state, player):
        row = 0
        while row < self.board_height and state.board[row,move] != 0:
            row += 1
        state.board[row,move] = player
        cw = self.is_winning_state(state, player) == player
        state.board[row,move] = 0
        return cw

    def is_winning_state(self, state, player_num=None):
        # check rows for 4 in a row
        for row in range(0,self.board_height):
            curr = 0
            count = 0
            for col in range(0,self.board_width):
                if state.board[row][col] == 0:
                    count = 0
                elif state.board[row][col] == curr:
                    count += 1
                    if count >= 4:
                        return curr
                else:
                    curr = state.board[row][col]
                    count = 1
        # check cols for 4 in a row
        for col in range(0,self.board_width):
            curr = 0
            count = 0
            for row in range(0,self.board_height):
                if state.board[row][col] == 0:
                    count = 0
                elif state.board[row][col] == curr:
                    count += 1
                    if count >= 4:
                        return curr
                else:
                    curr = state.board[row][col]
                    count = 1
        #  check diagonals
        diags = [
            [(3,0), (2,1), (1,2), (0,3)],
            [(4,0), (3,1), (2,2), (1,3), (0,4)],
            [(5,0), (4,1), (3,2), (2,3), (1,4), (0,5)],
            [(5,1), (4,2), (3,3), (2,4), (1,5), (0,6)],
            [(5,2), (4,3), (3,4), (2,5), (1,6)],
            [(5,3), (4,4), (3,5), (2,6)],
            [(2,0), (3,1), (4,2), (5,3)],
            [(1,0), (2,1), (3,2), (4,3), (5,4)],
            [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5)],
            [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6)],
            [(0,2), (1,3), (2,4), (3,5), (4,6)],
            [(0,3), (1,4), (2,5), (3,6)]
        ]
        for diag in diags:
            curr = 0
            count = 0
            for spot in diag:
                row = spot[0]
                col = spot[1]
                if state.board[row][col] == 0:
                    count = 0
                elif state.board[row][col] == curr:
                    count += 1
                    if count >= 4:
                        return curr
                else:
                    curr = state.board[row][col]
                    count = 1
        return 0


        """
        This function will tell if the player_num player is
        winning in the board that is input
        """
        '''if player_num is None:
            player_num = state.turn

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

        return (check_horizontal(state.board) or
                check_vertical(state.board) or
                check_diagonal(state.board))'''

        
        





# This is the code for the interface for you to play against your ai
class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def make_move(self, state):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = state.get_valid_moves()

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move







