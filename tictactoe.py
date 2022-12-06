# TicTacToe in Python
from time import sleep
from sys import exit
from os import system
from src.game import Game

if __name__ == '__main__':
    while(True):
        try:
            system('clear')
            print(f"""

{'='*80}
{' '*35}Welcome!!!
{'='*80}
Start the game now by providing two names for two players.
First inputed name gets first chance to play.

The gameplay consist of you and your opponent providing the co-ordinates,
seperated by a comma eg. (1,2), of the boxes to place 
your symbol i.e. X or O in a 3x3 grid

First to have 3 respective symbols in a row, column or diagonal wins.

To play against the computer type 'AI' (without quotes) as a player name.

Press Ctrl+C to Quit

{'='*80}

            """)

            names = input('Input names separated by space: ')
            names = tuple(names.split(' '))

            if (len(names) != 2): raise IndexError

            game = Game(names)
            game.run()

            sleep(5)

        except KeyboardInterrupt:
            system('clear')
            exit()

        # except IndexError:
            # print("\nPlease provide sufficient player names")
            # sleep(2)
            # continue
