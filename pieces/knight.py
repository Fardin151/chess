from .piece import Piece
from move import Move


class Knight(Piece):
    def symbol(self):
        return 'N'

    def get_moves(self, row, col, board, last_move=None):
        moves = []
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append(Move((row, col), (r, c)))
        return moves
