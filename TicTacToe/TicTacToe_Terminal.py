class Board():
    def __init__(self):
        '''Creates a TicTacToe board represented with a 2d list'''
        self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def is_winner(self):
        '''Checks if there is a winner based on the state of the board'''
        for row in range(len(self.state)):
            if all([val == self.state[row][0] and val for val in self.state[row]]):
                return True
        for column in range(len(self.state[0])):
            if all([self.state[row][column] == self.state[0][column] and self.state[row][column] for row in range(len(self.state))]):
                return True
        if self.state[1][1] and self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0] or self.state[0][0] == self.state[1][1] and self.state[1][1] == self.state[2][2]:
            return True
        return False

    def is_full(self):
        '''Checks if all spaces on the board have already been selected'''
        for row in range(len(self.state)):
            for column in range(len(self.state[row])):
                if not self.state[row][column]:
                    return False
        return True

    def __str__(self):
        '''Displays the current state of the board'''
        return str(self.state)


class Player():
    def __init__(self, number):
        '''Creates a player'''
        self.number = number

    def __str__(self):
        '''Displays the specific player'''
        return "Player " + str(self.number)


class Game():

    def __init__(self):
        '''Creates a TicTacToe game'''
        self.board = Board()
        self.players = []
        for i in range(1, 3):
            self.players.append(Player(i))
        self.winner = None

    def play(self):
        '''Starts a TicTacToe game that ends when there is a winner or the board is full'''
        num_turns = 0
        while not self.winner and not self.board.is_full():
            current_player = self.players[num_turns % 2]
            print(self.board)
            print(str(current_player) + " turn")
            row = int(input("Which row?: "))
            column = int(input("Which column?: "))
            if not 0 <= row <= 2 or not 0 <= column <= 2:
                print("Invalid spot! Try Again")
            elif self.board.state[row][column]:
                print("This spot is already taken! Try Again")
            else:
                self.board.state[row][column] = current_player.number
                if self.board.is_winner():
                    self.winner = current_player
                num_turns += 1
        print(self.board)
        print(str(self))

    def __str__(self):
        '''Displays the outcome of the game if there is any'''
        if self.winner:
            return str(self.winner) + " won the game."
        if self.board.is_full():
            return "The board is full but there is no winner."
        return "There is no winner yet."
