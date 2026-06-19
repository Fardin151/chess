from .piece import Piece


class Rook(Piece):
    def symbol(self):
        return 'R'

    def get_moves(self, row, col, board, last_move=None):
        return self._ray_moves(row, col, board, [(-1,0),(1,0),(0,-1),(0,1)])
