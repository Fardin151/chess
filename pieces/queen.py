from .piece import Piece


class Queen(Piece):
    def symbol(self):
        return 'Q'

    def get_moves(self, row, col, board, last_move=None):
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        return self._ray_moves(row, col, board, dirs)
