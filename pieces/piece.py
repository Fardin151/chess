class Piece:
    def __init__(self, color):
        self.color = color  # 'white' or 'black'
        self.has_moved = False

    def get_moves(self, row, col, board, last_move=None):
        raise NotImplementedError

    def symbol(self):
        raise NotImplementedError

    def _ray_moves(self, row, col, board, directions):
        from move import Move
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append(Move((row, col), (r, c)))
                elif target.color != self.color:
                    moves.append(Move((row, col), (r, c)))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves
