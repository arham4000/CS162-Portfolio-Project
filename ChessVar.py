# Author: Armam Ahmed
# GitHub username: arham4000
# Date: 03/06/2025
# Description: A program that simulates the "King of the Hill" chess variant

class Piece:
    """
    Parent class of chess piece classes
    """
    def __init__(self, tag):
        self._tag = tag
        if tag.islower():
            self._color = "black"
        else:
            self._color = "white"

    def get_tag(self):
        """ returns tag of piece """
        return self._tag

    def get_color(self):
        """ returns color of piece """
        return self._color

class Pawn(Piece):
    """
    Pawn pieces with special attribute first move and pawn movement validation method
    """
    def __init__(self, tag):
        super().__init__(tag)
        self._first_move = True

    def validate_move(self, board, orig_x, orig_y, dest_x, dest_y):
        """
        Validates specific movement of piece, returns True if valid, else return False
        """
        y = dest_y - orig_y
        x = dest_x - orig_x

        # Absolute value of x movement must be 0, 1 regardless of color
        if abs(x) not in [0, 1]:
            return False

        # Cannot move diagonal if moving two steps forward
        if abs(y) == 2 and x != 0:
            return False

        # Can only move diagonal to capture
        if abs(x) == 1 and board[dest_y][dest_x] == ' ':
            return False

        # Validating forwards movement for white and black needs reversed coordinates as pawns can only move forwards
        if self._color == "white":
            # Y movement for white can be -1, -2
            if y not in [-1, -2]:
                return False
            # Y can only be -1 if not first move
            if not self._first_move and y != -1:
                return False

            # Can only move forward if path is clear (cannot jump, can only capture diagonally)
            if x == 0:
                path = []
                for i in range(dest_y, orig_y):
                    path.append(board[i][orig_x])
            # If forward path is not empty, move is invalid
                for element in path:
                    if element != ' ':
                        return False

        # Code for white and black needs reversed coordinates as pawns can only move forwards
        if self._color == "black":
            # Y movement for white can be 1, 2
            if y not in [1, 2]:
                return False
            # Y can only be 1 if not first move
            if not self._first_move and y != 1:
                return False

            # Can only move forward if path is clear (cannot jump, can only capture diagonally)
            if x == 0:
                path = []
                for i in range(orig_y+1, dest_y+1):
                    path.append(board[i][orig_x])
                # If forward path is not empty, move is invalid
                for element in path:
                    if element != ' ':
                        return False

        # If first move validated, update first_move to False
        if self._first_move:
            self._first_move = False

        return True

class Rook(Piece):
    """
    Rook pieces with rook movement validation method
    """
    def __init__(self, tag):
        super().__init__(tag)

    def validate_move(self, board, orig_x, orig_y, dest_x, dest_y):
        """
        Validates specific movement of piece, returns True if valid, else return False
        """
        y = dest_y - orig_y
        x = dest_x - orig_x

        # Can move forwards, backwards, left, or right.
        # No diagonal movement
        # Can move any number of spaces as long as path is clear (no jumps)

        path = []
        if abs(x) > 0:
            # Cannot have y movement if there is x movement
            if y != 0:
                return False

            # Path calculation for moving right
            if x > 0:
                for i in range(orig_x+1, dest_x):
                    path.append(board[orig_y][i])
                for element in path:
                    if element != ' ':
                        return False

            # Path calculation for moving left
            if x < 0:
                for i in range(dest_x+1, orig_x):
                    path.append(board[orig_y][i])
                for element in path:
                    if element != ' ':
                        return False

        if abs(y) > 0:
            # Cannot have x movement if there is y movement
            if x != 0:
                return False

            # Path calculation for moving up
            if y < 0:
                for i in range(dest_y+1, orig_y):
                    path.append(board[i][orig_x])
                for element in path:
                    if element != ' ':
                        return False

            # Path calculation for moving down
            if y > 0:
                for i in range(orig_y+1, dest_y):
                    path.append(board[i][orig_x])
                for element in path:
                    if element != ' ':
                        return False

        return True

class Knight(Piece):
    """
    Knight piece with knight move validation method
    """
    def __init__(self, tag):
        super().__init__(tag)

    def validate_move(self, board, orig_x, orig_y, dest_x, dest_y):
        """
        Validates specific movement of piece, returns True if valid, else return False
        """
        # Can move 1, 2 or 2, 1 spaces in any direction
        # Can jump over pieces
        # (x^2 + y^2 )^(1/2) must equal 5^(1/2)
        y = dest_y - orig_y
        x = dest_x - orig_x

        hyp = 5
        xy_hyp = x**2 + y**2
        sqrt_xy_hyp = xy_hyp**(1/2)
        sqrt_hyp = hyp**(1/2)

        if abs(sqrt_xy_hyp - sqrt_hyp) > 0.01:
            return False

        return True

class Bishop(Piece):
    """
    Bishop pieces with special attributes valid x, valid y.
    """
    def __init__(self, tag):
        super().__init__(tag)
        self._valid_x = 1
        self._valid_y = 1

    def validate_move(self, board, orig_x, orig_y, dest_x, dest_y):
        """
        Validates specific movement of piece, returns True if valid, else return False
        """
        y = dest_y - orig_y
        x = dest_x - orig_x

        # Can move diagonal in any direction, abs(x) must equal abs(y)
        if abs(x) != abs(y):
            return False

        # Cannot move straight in any direction, x or y cannot be 0
        if x == 0 or y == 0:
            return False

        # If abs(x), abs(y) both equal 1, no need to validate path
        if abs(x) == 1 and abs(y) == 1:
            return True

        path = []
        # Cannot jump, path must be empty up to destination
        # +x, +y path validation
        if x > 0 and y < 0:
            for i in range(1, x):
                path.append(board[orig_y - i][orig_x + i])
            for element in path:
                if element != ' ':
                    return False

        # +x, -y path validation
        if x > 0 and y > 0:
            for i in range(1, x):
                path.append(board[orig_y + i][orig_x + i])
            for element in path:
                if element != ' ':
                    return False

        # -x, +y path validation
        if x < 0 and y < 0:
            for i in range(1, abs(x)):
                path.append(board[orig_y - i][orig_x - i])
            for element in path:
                if element != ' ':
                    return False

        # -x, -y path validation
        if x < 0 and y > 0:
            for i in range(1, abs(x)):
                path.append(board[orig_y + i][orig_x - i])
            for element in path:
                if element != ' ':
                    return False

        return True

class Queen(Piece):
    """
    Queen pieces with queen movement validation method
    """
    def __init__(self, tag):
        super().__init__(tag)

    def validate_move(self, board, orig_x, orig_y, dest_x, dest_y):
        """
        Validates specific movement of piece, returns True if valid, else return False
        """
        y = dest_y - orig_y
        x = dest_x - orig_x
        path = []

        # Can move diagonal any number of spaces (Bishop), abs(x) must equal abs(y)
        if abs(x) == abs(y):

            # If abs(x), abs(y) equal 1, no need to validate path
            if abs(x) == 1 and abs(y) == 1:
                return True

            # Diagonal path verification, cannot jump over pieces
            # +x, +y path validation
            if x > 0 and y < 0:
                for i in range(1, x):
                    path.append(board[orig_y - i][orig_x + i])
                for element in path:
                    if element != ' ':
                        return False
                return True

            # +x, -y path validation
            if x > 0 and y > 0:
                for i in range(1, x):
                    path.append(board[orig_y + i][orig_x + i])
                for element in path:
                    if element != ' ':
                        return False
                return True

            # -x, +y path validation
            if x < 0 and y < 0:
                for i in range(1, abs(x)):
                    path.append(board[orig_y - i][orig_x - i])
                for element in path:
                    if element != ' ':
                        return False
                return True

            # -x, -y path validation
            if x < 0 and y > 0:
                for i in range(1, abs(x)):
                    path.append(board[orig_y + i][orig_x - i])
                for element in path:
                    if element != ' ':
                        return False
                return True

        # Can move left/right, up/down any number of spaces (Rook)
        if abs(x) > 0:
            # Cannot have y movement if there is x movement
            if y != 0:
                return False

            # No need to calculate path if moving one step
            if abs(x) == 1:
                return True

            # Path calculation for moving right
            if x > 0:
                for i in range(orig_x + 1, dest_x):
                    path.append(board[orig_y][i])
                for element in path:
                    if element != ' ':
                        return False

            # Path calculation for moving left
            if x < 0:
                for i in range(dest_x + 1, orig_x):
                    path.append(board[orig_y][i])
                for element in path:
                    if element != ' ':
                        return False

        if abs(y) > 0:
            # Cannot have x movement if there is y movement
            if x != 0:
                return False

            # No need to calculate path if moving one step
            if abs(y) == 1:
                return True

            # Path calculation for moving up
            if y < 0:
                for i in range(dest_y + 1, orig_y):
                    path.append(board[i][orig_x])
                for element in path:
                    if element != ' ':
                        return False

            # Path calculation for moving down
            if y > 0:
                for i in range(orig_y + 1, dest_y):
                    path.append(board[i][orig_x])
                for element in path:
                    if element != ' ':
                        return False

        return True

class King(Piece):
    """
    King pieces with king movement validation method
    """
    def __init__(self, tag):
        super().__init__(tag)

    def validate_move(self, board, orig_x, orig_y, dest_x, dest_y):
        """
        Validates specific movement of piece, returns True if valid, else return False
        """
        y = dest_y - orig_y
        x = dest_x - orig_x

        # Can move one space in any direction
        # No need for path validation
        if abs(x) not in [0, 1]:
            return False
        if abs(y) not in [0, 1]:
            return False

        return True

class ChessVar:
    """
    Implements 'King of the Hill' chess variant using Piece objects
    """
    def __init__(self):
        self._board = [[" " for i in range(8)] for i in range(8)]
        self.initialize_board()
        # game_state = UNFINISHED, WHITE_WON, BLACK_WON
        self._game_state = "UNFINISHED"
        self._current_player = "white"

    def initialize_board(self):
        self._board[0] = [Rook('r'), Knight('n'), Bishop('b'), Queen('q'), King('k'), Bishop('b'), Knight('n'), Rook('r')]
        self._board[1] = [Pawn('p') for i in range(8)]
        self._board[6] = [Pawn('P') for i in range(8)]
        self._board[7] = [Rook('R'), Knight('N'), Bishop('B'), Queen('Q'), King('K'), Bishop('B'), Knight('N'), Rook('R')]

    def get_board(self):
        """
        Returns printable board
        """
        printable_board = [[" " for i in range(8)] for i in range(8)]

        for i in range(8):
            for j in range(8):
                if self._board[i][j] != " ":
                    printable_board[i][j] = self._board[i][j].get_tag()

        return printable_board

    def get_game_state(self):
        """
        Returns game state
        """
        return self._game_state

    def make_move(self, orig, dest):
        """
        Move piece at orig from orig to dest. If illegal move, return False, if successful, return True
        """
        # Preparing Coordinates
        letter_map = {'a': 0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

        # Validating x coordinates, move invalid if out of board bounds
        if orig[0] not in letter_map or dest[0] not in letter_map:
            return False

        orig_x = letter_map[orig[0]]
        orig_y = int(orig[1:])-1
        # Inverting y coordinates to match representation
        orig_y = (orig_y * -1) + 7

        dest_x = letter_map[dest[0]]
        dest_y = int(dest[1:])-1
        # Inverting y coordinates to match representation
        dest_y = (dest_y * -1) + 7

        # Validating y coordinates, move invalid if out of board bounds
        if orig_y > 7 or orig_y < 0 or dest_y > 7 or dest_y < 0:
            return False

        # Moves are only allowed when game state is UNFINISHED
        if self._game_state != "UNFINISHED":
            return False

        # Move is invalid if orig coordinate is empty
        if self._board[orig_y][orig_x] == ' ':
            return False

        # Move is invalid if orig piece color does not match current player
        if self._board[orig_y][orig_x].get_color() != self._current_player:
            return False

        # Move is invalid if destination contains piece of same color
        if self._board[dest_y][dest_x] != ' ':
            capture_color = self._board[dest_y][dest_x].get_color()
            if self._current_player == capture_color:
                return False

        # Validating the specific movement of the piece being moved
        if not self._board[orig_y][orig_x].validate_move(self._board, orig_x, orig_y, dest_x, dest_y):
            return False

        # Moving piece if all validations are complete
        self.move_piece(orig_x, orig_y, dest_x, dest_y)
        return True

    def move_piece(self, orig_x, orig_y, dest_x, dest_y):
        """
        Invoked by make_move if move is valid, moves piece from orig to dest, checks winning conditions
        """
        # Picking up a piece in hand, empty space left behind
        in_hand = self._board[orig_y][orig_x]
        self._board[orig_y][orig_x] = ' '

        # If king in hand, check if king going to hill (d4, e4, d5, e5), update game state
        if in_hand.get_tag() == "k":
            if dest_x == 3 or dest_x == 4:
                if dest_y == 3 or dest_y == 4:
                    self._game_state = "BLACK_WON"

        if in_hand.get_tag() == "K":
            if dest_x == 3 or dest_x == 4:
                if dest_y == 3 or dest_y == 4:
                    self._game_state = "WHITE_WON"

        # Moving in hand piece to destination
        capture = self._board[dest_y][dest_x]
        self._board[dest_y][dest_x] = in_hand

        # Checking if captured piece is King, updating game state
        if capture != ' ':
            if capture.get_tag() == 'k':
                self._game_state = "WHITE_WON"

            if capture.get_tag() == 'K':
                self._game_state = "BLACK_WON"

        # Changing current player
        if self._current_player == "white":
            self._current_player = "black"
        else:
            self._current_player = "white"

def main():
    game = ChessVar()
    inp1 = ''
    inp2 = ''

    while inp1 != 'q':
        print(game._current_player)
        board = game.get_board()
        for row in board:
            print(row)
        print()
        inp1 = input("Enter orig: ")
        inp2 = input("Enter dest: ")

        print(game.make_move(inp1, inp2))
        print(game.get_game_state())

if __name__ == "__main__":
    main()






