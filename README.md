This is my Pyhton portfolio project for CS162 at OSU. 

This program implements a chess variant named "King of th Hill". All normal rules of chess are followed, except there is no 
pawn upgrading, no en passant, and no check or check mate. The game runs until a player's king is captured or a player's king
reaches one of the four central squares. 

I spent a lot of time designing the program before getting into implementation because
there are a lot of small details that are hard to keep track of while coding on the go. 

First, I thought of how to implement the chess board, pieces, and game rules. Initially, I thought of creating a chess board
class, chess piece classes for all the different types of pieces, and a class for the game itself. After writing out some pseudo-code,
I didn't see benefit in creating a separate class for the chess board. Implementing the board within the chess game class reduced 
unnecessary code clutter created by having methods within each class to call each other. 

I created a chess game class (ChessVar), a general parent chess piece class (Piece), and specific sub classes for each type of chess piece (Pawn, Rook, Knight, etc). 

The ChessVar class initializes the chess board as a list of 8 lists, with each sublist having 
8 members to represent an 8x8 chess board. Chess pieces are instances of their respective
classes and are stored in the board as objects. I wrote a get_board method that goes
through the chess board and returns a printable version, replacing chess piece objects with 
their character tags, ex: 'K', 'p', 'q', etc, to make it easier to visualize the board while
playing. 

Implementing the board and placing the pieces was relatively simple, the harder part was
implementing the piece movement rules. Pawns can move two spaces forward on their first move,
rooks can move any number of spaces horizontally or vertically but cannot jump over pieces, 
and so on. 

The ChessVar make_move method validates the general movement rules for any attempted move, 
such as a player cannot capture their own piece, a piece cannot move outside the board, etc.
After validating general movement rules, the make_move method calls the validate_move method
of the specific piece being moved. The validate_move method validates the piece specific 
movement rules, ex: king can move one step in any direction, knight can move in a specific 
pattern, etc. If the validate_move method returns True, the make_move method calls the
move_piece method, which takes care of the specific of moving a piece object on the board.


