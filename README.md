# cs-470-reversi-python-client

A Python 3 client for the BYU CS 470 Reversi lab. All that you need to change for your project is the `make_move` function in the AIPlayer class in the player.py script. See comment there for information on useful functionality.

To run, enter directory where this code is located and type `python gameServer.py 10`. This starts the server and the GUI. Then open another terminal in the same folder and type `python gameClient.py localhost 1` (if you want this running on localhost and for it to be first player). You can do 2 for second player or specify a different host ip address as well. The gameClient.py also accepts an additional parameter `human` if you want a human player. The human player types their moves as the index of the column to put the piece in.

## PULL REQUESTS ARE WELCOME

![Connect4 Board Image](https://upload.wikimedia.org/wikipedia/commons/a/ad/Connect_Four.gif)
