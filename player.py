# This has code for human, random, and ai players and calls functions from connect4game.py It should not worry about connections at all

import game

import numpy as np
import random as rand


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number  #This is the id of the player this AI is in the game
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.other_player_number = 1 if player_number == 2 else 2  #This is the id of the other player

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

        move = rand.choice(valid_moves) # Moves randomly...for now
        return move



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







