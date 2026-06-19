from .piece import Piece
from move import Move


class Pawn(Piece):
    def symbol(self):
        return 'P'

    def get_moves(self, row, col, board, last_move=None):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        promo_row = 0 if self.color == 'white' else 7

        # One step forward
        r = row + direction
        if 0 <= r < 8 and board[r][col] is None:
            if r == promo_row:
                for p in ['Q', 'R', 'B', 'N']:
                    moves.append(Move((row, col), (r, col), promotion=p))
            else:
                moves.append(Move((row, col), (r, col)))
            # Two steps from start
            if row == start_row and board[row + 2 * direction][col] is None:
                moves.append(Move((row, col), (row + 2 * direction, col)))

        # Diagonal captures
        for dc in [-1, 1]:
            r, c = row + direction, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is not None and target.color != self.color:
                    if r == promo_row:
                        for p in ['Q', 'R', 'B', 'N']:
                            moves.append(Move((row, col), (r, c), promotion=p))
                    else:
                        moves.append(Move((row, col), (r, c)))

        # En passant
        if last_move is not None:
            (fr, fc), (tr, tc) = last_move.from_sq, last_move.to_sq
            moved_piece = board[tr][tc]
            if (moved_piece is not None
                    and moved_piece.symbol() == 'P'
                    and moved_piece.color != self.color
                    and abs(fr - tr) == 2
                    and tr == row
                    and abs(tc - col) == 1):
                ep_row = row + direction
                moves.append(Move((row, col), (ep_row, tc), is_en_passant=True))

        return moves
