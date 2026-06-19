from .piece import Piece


class Bishop(Piece):
    def symbol(self):
        return 'B'

    def get_moves(self, row, col, board, last_move=None):
        return self._ray_moves(row, col, board, [(-1,-1),(-1,1),(1,-1),(1,1)])
