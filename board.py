from pieces import Pawn, Knight, Bishop, Rook, Queen, King


def make_empty_board():
    return [[None] * 8 for _ in range(8)]


def copy_board(board):
    new = make_empty_board()
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p is not None:
                import copy
                new[r][c] = copy.copy(p)
    return new


def setup_initial_position():
    board = make_empty_board()
    order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    for c, PieceClass in enumerate(order):
        board[0][c] = PieceClass('black')
        board[7][c] = PieceClass('white')

    for c in range(8):
        board[1][c] = Pawn('black')
        board[6][c] = Pawn('white')

    return board


def find_king(board, color):
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p is not None and p.symbol() == 'K' and p.color == color:
                return (r, c)
    return None
