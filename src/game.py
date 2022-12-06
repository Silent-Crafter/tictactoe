from os import system
from src.player import Player, AI
from time import sleep

# Creating a useless class
class Game:

    def __init__(self, names: tuple):

        self.board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]

        self.names = names

    def run(self):

        # Check if you wanna play against the AI
        if 'AI' in self.names:
            index = self.names.index('AI')
            if index == 0:
                p1 = AI()
                p2 = Player(self.names[1])
                enemy = 'p2'
            else:
                p1 = Player(self.names[0])
                p2 = AI()
                enemy = 'p1'
        else:
            p1 = Player(self.names[0])
            p2 = Player(self.names[1])

        # Assign the 'X' to first player and 'O' to second
        symbol = {
            'X': str(p1),
            'O': str(p2),
            str(p1): 'X',
            str(p2): 'O',
        }

        turn = 0
        result = ''

        player = p1
        r, c = 9, 9
        char = symbol[str(player)]

        while True:
            system('clear')
            # Draw the game board
            counter = 1
            print()
            print('    1   2   3  ')
            print('  |---|---|---|')
            for row in self.board:
                print('{} |'.format(counter), end='')
                for col in row:
                    print(' ' + col + ' ', end='')
                    print('|', end='')
                print()
                print('  |---|---|---|')
                counter += 1

            if turn % 2 == 0:
                player = p1
            else:
                player = p2

            # Handler for AI
            if str(player) == 'AI':
                r, c = player.play(turn, self.board, last_played={'row': r, 'col': c})
                # print(f'({r}, {c})')
                # sleep(1)
                char = symbol[str(player)]
            else:
                command = input('\n{}> '.format(player))
                try:
                    r, c = command.split(',')
                    r, c = int(r)-1, int(c)-1
                    char = symbol[str(player)]
                except (ValueError, IndexError):
                    continue

            try:
                self.update_board(int(r), int(c), char.upper())
            except (TypeError, ValueError):
                continue

            # Check if someone won
            result = self.win_check()

            if result:
                break

            turn += 1

        system('clear')

        counter = 1
        print()
        print('    1   2   3  ')
        print('  |---|---|---|')
        for row in self.board:
            print('{} |'.format(counter), end='')
            for col in row:
                print(' ' + col + ' ', end='')
                print('|', end='')
            print()
            print('  |---|---|---|')
            counter += 1

        if result == 'Draw':
            print('\nIt is a Draw')
        else:
            print('\nThe Winner is', symbol[result])

    def win_check(self):

        # Check both diagonals first
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0].strip()

        elif self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2].strip()

        else:
            # Check row-wise
            for row in range(3):
                if self.board[row][0] == self.board[row][1] == self.board[row][2] != ' ':
                    return self.board[row][0]

            # Check column-wise
            for col in range(3):
                if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                    return self.board[0][col]

            for row in self.board:
                if row[0] == ' ' or row[1] == ' ' or row[2] == ' ':
                    return None

            return 'Draw'

    def update_board(self, row: int, col: int, char: str):
        try:
            if self.board[row][col] == ' ':
                self.board[row][col] = '{}'.format(char)
            else:
                print('Invalid Move !')
                sleep(0.5)
                raise TypeError
        except (IndexError, ValueError, TypeError, KeyError):
            raise TypeError
