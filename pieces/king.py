from .piece import Piece
from move import Move


class King(Piece):
    def symbol(self):
        return 'K'

    def get_moves(self, row, col, board, last_move=None):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board[r][c]
                    if target is None or target.color != self.color:
                        moves.append(Move((row, col), (r, c)))

        # Castling — legality (no check through squares) enforced in game.py
        if not self.has_moved:
            # Kingside
            rook = board[row][7]
            if (rook is not None and rook.symbol() == 'R' and not rook.has_moved
                    and board[row][5] is None and board[row][6] is None):
                moves.append(Move((row, col), (row, col + 2), is_castling=True))
            # Queenside
            rook = board[row][0]
            if (rook is not None and rook.symbol() == 'R' and not rook.has_moved
                    and board[row][1] is None and board[row][2] is None and board[row][3] is None):
                moves.append(Move((row, col), (row, col - 2), is_castling=True))

        return moves
