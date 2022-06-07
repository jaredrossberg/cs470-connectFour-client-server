# This will hold code for connecting to the server and calling the AI code.
# It should not be game specific.

import player
import game

import numpy as np
import socket
import sys
import time


class ServerConnection:
    def __init__(self, host, bot_move_num):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, 3333 + bot_move_num)
        self.sock.connect(server_address)
        self.sock.recv(1024)

    def get_game_state(self):
        server_msg = self.sock.recv(1024).decode('utf-8').split('\n')

        # print('Message:\n' + str(server_msg))
        turn = int(str(server_msg[0]))

        # If the game is over
        if turn == -999:
            return game.GameState(None, turn)

        # Flip is necessary because of the way the server does indexing
        board = game.messageToBoard(server_msg)
        return game.GameState(board, turn)

    def send_move(self, move):
        move_str = str(move) + '\n'
        self.sock.send(move_str.encode('utf-8'))


class GameInstance:
    def __init__(self, host, bot_move_num, player_type):
        self.bot_move_num = bot_move_num
        self.server_conn = ServerConnection(host, bot_move_num)
        if player_type.lower() == 'human':
            self.bot = player.HumanPlayer(bot_move_num)
        else:
            self.bot = player.AIPlayer(bot_move_num)

    def play(self):
        while True:
            state = self.server_conn.get_game_state()

            # If the game is over
            if state.turn == -999:
                time.sleep(1)
                sys.exit()

            # If it is the bot's turn
            if state.turn == self.bot_move_num:
                move = self.bot.make_move(state)
                self.server_conn.send_move(move)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append('localhost')
        sys.argv.append('1')

    server_address = sys.argv[1]
    bot_move_number = int(sys.argv[2])
    if len(sys.argv) > 3:
        player_type = sys.argv[3]
    else:
        player_type = 'ai'

    currGame = GameInstance(server_address, bot_move_number, player_type)
    currGame.play()