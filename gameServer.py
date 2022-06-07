# This will handle the connection from the two clients 
# as well as instantiating the game

import game

import socket
import sys
import time


class ClientConnection:
    def __init__(self, player_num, min_per_player):
        self.player_num = player_num
        server_address = ('', 3333 + player_num)

        # https://realpython.com/python-sockets/
        # socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind
        self.sock.bind(server_address)
        # listen
        self.sock.listen()
        # accept
        print('accepting player ' + str(player_num))
        self.conn, addr = self.sock.accept()
        print('accepted player ' + str(player_num))

        self.sendToClient(str(player_num) + " " + str(min_per_player))

    def sendToClient(self, strToSend):
        strToSend += '\n'
        bytesToSend = str.encode(strToSend)
        self.conn.sendall(bytesToSend)
    
    def getFromClient(self, len):
        return self.conn.recv(len)

    def takeTurn(self, roundNum, state, timesLeft):
        self.update(roundNum, state, timesLeft)
        response = self.getFromClient(1024)
        respStr = response.decode()
        move = int(str(respStr[-2]))
        return move

    def gameOver(self, state):
        self.sendToClient('-999')

    def update(self, roundNum, state, timesLeft):
        status = str(self.player_num) + '\n' + str(roundNum) + '\n' 
        status += str(timesLeft[0]) + '\n' + str(timesLeft[1]) + '\n'
        status += game.boardToMessage(state)

        self.sendToClient(status)

    def finale(self, winner, state, timesLeft):
        status = str(winner) + '\n' + str(timesLeft[0]) + '\n' + str(timesLeft[1]) + '\n'
        status += game.boardToMessage(state)
        self.sendToClient(status)


class GameInstance:
    def __init__(self, min_per_player):
        self.timeLeft = [min_per_player * 60, min_per_player * 60]
        self.state = game.GameState(game.generateNewBoard(), 1)
        self.gui = game.GameGUI()
        self.players = [ClientConnection(1, min_per_player), ClientConnection(2, min_per_player)]
        time.sleep(0.05)

    def play(self):
        round = 0
        while True:
            player_num = self.state.turn
            self.gui.changeTurn(player_num)

            startTime = time.time()

            time.sleep(0.05)
            move = self.players[player_num - 1].takeTurn(round, self.state, self.timeLeft)
            time.sleep(0.05)

            endTime = time.time()
            self.timeLeft[player_num - 1] -= (endTime - startTime)

            if self.timeLeft[player_num - 1] <= 0:
                time.sleep(0.1)
                self.players[0].gameOver(self.state)
                self.players[1].gameOver(self.state)
                winner = 1 if player_num == 2 else 2
                break

            # FIXME: This bit needs to be changed to make it truly generic
            update_row = self.state.make_move(move)
            self.gui.placePiece(move, update_row, player_num)
            round += 1

            self.players[0].update(round, self.state, self.timeLeft)
            self.players[1].update(round, self.state, self.timeLeft)
            time.sleep(0.1)

            if self.state.is_game_over():
                winner = 1 if self.state.is_winning_state(1) else 2
                break
        
        if self.timeLeft[0] <= 0:
            self.timeLeft[0] = 0
        if self.timeLeft[1] <= 0:
            self.timeLeft[1] = 0
        
        self.gui.set_winner(winner)
        self.players[0].finale(winner, self.state, self.timeLeft)
        self.players[1].finale(winner, self.state, self.timeLeft)

        while True:
            self.gui.updateGUI()



if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append('10')
    minutes_per_player = int(sys.argv[1])

    currGame = GameInstance(minutes_per_player)
    try:
        currGame.play()
    except Exception as err:
        print(err)
        while True:
            pass
