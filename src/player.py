from time import sleep
from random import randint

# Another useless class
class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return 'Player({} {})'.format(self.name, self.score)
    
    # IGNORE
    # def __lt__(self, other):
    #     return self.score < other.score
    #
    # def __gt__(self, other):
    #     return self.score > other.score
    #
    # def __eq__(self, other):
    #     return self.score == other.score
    #
    # def __le__(self, other):
    #     return self.score <= other.score
    #
    # def __ne__(self, other):
    #     return self.score != other.score


# AI my foot, it's just an if-else bot. CURRENT STATUS: shitty and defeatable with no clear sence of winning. EDIT: added atleast some sense
class AI:

    def __init__(self):

        # Pre-defined best, possible counter-moves for a win or draw
        self.cheatsheet = {
            (0, 0): (1, 1),
            (0, 2): (1, 1),
            (2, 0): (1, 1),
            (2, 2): (1, 1),

            (1, 1): [(0, 0), (0, 2), (2, 0), (2, 2)],

            (0, 1): [(0, 0), (0, 2), (2, 0), (2, 2)],
            (1, 0): [(0, 0), (0, 2), (2, 0), (2, 2)],
            (1, 2): [(0, 0), (0, 2), (2, 0), (2, 2)],
            (2, 1): [(0, 0), (0, 2), (2, 0), (2, 2)],
        }

        self.cheatsheet_2 = {
            (0, 0): (1, 1),
            (0, 2): (1, 1),
            (2, 0): (1, 1),
            (2, 2): (1, 1),
        }

        # For moves played by the player and the ai. currently pointless but it will make the ai powerfull in future. EDIT: Now is the future
        self.record = {
            'player': [],
            'ai': [],
        }

        self.counter = 0
        self.char = None    # Am i 'X' or am i 'O'. Stay tuned to find out

    # 'AI' str will be return when you cast the class into a string i.e. str(AI)
    def __str__(self):
        return 'AI'

    def play(self, turn, board: list, last_played: dict):
        r, c = last_played['row'], last_played['col']
        self.counter = turn // 2        # Number of times AI has played
        # sleep(2)

        if self.counter == 0:
            # 9,9 is used here for handling many exceptional cases here. in this instance, its used if ai is the first one to play.
            if (r,c) == (9,9):
                r,c = (1,1)
                self.char = 'X'
            else:
                self.record['player'].append((r, c))
                self.char = 'O'

            # Ask the fkin cheatsheet for help. Guranteed result.
            matches = self.cheatsheet[(r, c)]
            if type(matches) == list and matches:
                matches = self.randomize(matches)
                # If match is found check for valid cords in those matches
                for item in matches:
                    if item not in self.record['player'] and item not in self.record['ai']:
                        self.record['ai'].append(item)
                        # sleep(1)
                        return item

            elif type(matches) == tuple:
                self.record["ai"].append(matches)
                return matches
            else:
                print('got fked sideways')      # no, i mean, really. what the heck just happened here
                raise LookupError

        elif self.counter == 1:

            twocorners = False

            # First use logic else use the cheatsheet
            self.record['player'].append((r, c))
            if (turn%2 == 1): twocorners = self.twocorner()
            r, c = self.win_check(board)
            rc = None
            # Check if we wanna use the cheatsheet function
            if not (r, c) == (9, 9):
                rc = (r, c)
                self.record['ai'].append(rc)
                return rc

            else:
                if self.record:
                    pmove = self.record['player'][-1]
                    print(pmove)
                    print(self.cheatsheet[pmove])

                    if (twocorners): matches = [ (0,1), (1,0), (1,2), (2, 1) ]

                    # Check in cheatsheet first
                    else: matches = self.cheatsheet[pmove]
                    print(matches)

                    # If we got multiple matched from the cheatsheet
                    if matches and type(matches) == list:
                        # This is just for randomness
                        matches = self.randomize(matches)
                        
                        # If match is found check if the chords are playable
                        for item in matches:
                            # Check if its not already played
                            if item not in self.record['player'] and item not in self.record['ai']:
                                self.record['ai'].append(item)
                                # self.counter += 1
                                # sleep(1)
                                return item
                    
                    elif type(matches) == tuple:
                        # If only one match is found, check if its actually been played before. If yes, just do a random mov.
                        # (which further get checked again)
                        if matches in self.record['player'] or matches in self.record['ai']:
                            while True:
                                r = randint(0, 2)
                                c = randint(0, 2)

                                rc = (r, c)

                                if rc not in self.record['player'] and rc not in self.record['ai']:
                                    self.record['ai'].append(rc)
                                    # sleep(1)
                                    return rc
                        else:
                            self.record['ai'].append(matches)
                            return matches
                    
                    # Shouldn't really happen. it will definately find a match. but still here to prevent the hiesenbug
                    else:
                        while True:
                            r = randint(0, 2)
                            c = randint(0, 2)

                            rc = (r, c)

                            if rc not in self.record['player'] and rc not in self.record['ai']:
                                self.record['ai'].append(rc)
                                # sleep(1)
                                return rc                    
                        else:
                            print('got fked sideways')
                            raise LookupError

        # Use logic for 3rd turn onwards
        elif self.counter >= 2:
            self.record['player'].append((r, c))
            r, c = self.win_check(board)
            # print(r, c)
            # sleep(5)
            if not (r, c) == (9, 9):
                rc = (r, c)
            else:
                while True:
                    r = randint(0, 2)
                    c = randint(0, 2)

                    rc = (r, c)

                    if rc not in self.record['player'] and rc not in self.record['ai']:
                        self.record['ai'].append(rc)
                        # sleep(1)
                        return rc

            return rc
        else:
            # Um idk
            return None

    def win_check(self, board) -> (int, int):

        defence = None

        # Check both diagonals first
        for row in range(3):
            col = row
            # if there are 2 matching consecutive in each diagonal with empty space
            # thank god they let reading an array with negatives
            if board[row][col] == board[row-1][col-1] != ' ' and board[row-2][col-2] == ' ':
                # This lets my bot uhm ai to accidentally win
                if board[row][col] == self.char:
                    return row - 2, col - 2
                else:
                    defence = (row - 2, col - 2)
                    continue

        for row in range(3):
            col = 2 - row
            # print('\nin dia check')
            # print(row, col)
            # print(board[row][col], board[row - 1][col - 2], board[row - 2][col - 1])

            # if there are 2 matching consecutive in each diagonal with empty space
            if board[row][col] == board[row - 1][col - 2] != ' ' and board[row - 2][col - 1] == ' ':
                # This lets my bot uhm ai actually accidentally win
                if board[row][col] == self.char:
                    return row - 2, col - 1
                else:
                    defence = (row-2, col-1)
                    # I know i don't need to write this hear but it just makes the code readable
                    continue

        # Check row-wise
        for row in range(3):
            # print('\n in row check')
            # print(row)
            # print(board[row])
            for col in range(3):
                # print(f'{col=}')
                if board[row][col] == board[row][col - 1] != ' ' and board[row][col - 2] == ' ':
                    if board[row][col] == self.char:
                        return row, col - 2
                    else:
                        defence = (row, col - 2)
                        continue

        # Check column-wise
        for col in range(3):
            for row in range(3):
                if board[row][col] == board[row - 1][col] != ' ' and board[row - 2][col] == ' ':
                    # return the winning character with the blank space
                    return row - 2, col

        if defence:
            return defence
        # return an OoB(Out of bound) tuple which will tell the ai to use random values
        return 9, 9

    def cheat(self):
        pass
    
    # Shuffle the matches list
    def randomize(self, matches):
        _matches = []
        for counter in range(len(matches)):
            i = randint(0,len(matches)-1)
            _matches.append(matches[i])
            matches.pop(i)

        return _matches


    # An Early game trick to win
    def twocorner(self) -> bool:
        m1, m2 = self.record['player'][0], self.record['player'][1]
        if (m1[0]-m2[0] == m1[1] - m2[1]): return True
