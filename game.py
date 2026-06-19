import copy
from board import setup_initial_position, copy_board, find_king
from pieces import Pawn, Queen, Rook, Bishop, Knight


class GameState:
    def __init__(self):
        self.board = setup_initial_position()
        self.turn = 'white'
        self.last_move = None
        self.move_history = []
        self.status = 'playing'  # 'playing', 'checkmate', 'stalemate', 'draw'
        self.winner = None
        self.halfmove_clock = 0  # for 50-move rule

    # ------------------------------------------------------------------
    # Attack / check helpers
    # ------------------------------------------------------------------

    def square_attacked_by(self, row, col, color, board):
        """Return True if (row,col) is attacked by any piece of `color`."""
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p is None or p.color != color:
                    continue
                # Use pseudo-legal moves (no last_move needed for attack check)
                for m in p.get_moves(r, c, board, last_move=None):
                    if m.to_sq == (row, col):
                        return True
        return False

    def is_in_check(self, color, board):
        king_pos = find_king(board, color)
        if king_pos is None:
            return False
        opponent = 'black' if color == 'white' else 'white'
        return self.square_attacked_by(king_pos[0], king_pos[1], opponent, board)

    # ------------------------------------------------------------------
    # Move simulation
    # ------------------------------------------------------------------

    def apply_move_to_board(self, move, board):
        """Apply move to a board copy and return it (does not change game state)."""
        b = copy_board(board)
        piece = b[move.from_sq[0]][move.from_sq[1]]

        if move.is_en_passant:
            b[move.to_sq[0]][move.to_sq[1]] = piece
            b[move.from_sq[0]][move.from_sq[1]] = None
            # Remove the captured pawn
            captured_row = move.from_sq[0]
            b[captured_row][move.to_sq[1]] = None
        elif move.is_castling:
            b[move.to_sq[0]][move.to_sq[1]] = piece
            b[move.from_sq[0]][move.from_sq[1]] = None
            # Move the rook
            if move.to_sq[1] == 6:  # kingside
                rook = b[move.from_sq[0]][7]
                b[move.from_sq[0]][5] = rook
                b[move.from_sq[0]][7] = None
            else:  # queenside
                rook = b[move.from_sq[0]][0]
                b[move.from_sq[0]][3] = rook
                b[move.from_sq[0]][0] = None
        else:
            b[move.to_sq[0]][move.to_sq[1]] = piece
            b[move.from_sq[0]][move.from_sq[1]] = None
            if move.promotion:
                promo_map = {'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight}
                new_piece = promo_map[move.promotion](piece.color)
                new_piece.has_moved = True
                b[move.to_sq[0]][move.to_sq[1]] = new_piece

        # Mark has_moved
        moved = b[move.to_sq[0]][move.to_sq[1]]
        if moved is not None:
            moved.has_moved = True

        return b

    # ------------------------------------------------------------------
    # Legal move generation
    # ------------------------------------------------------------------

    def get_pseudo_moves(self, color, board):
        moves = []
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p is not None and p.color == color:
                    moves.extend(p.get_moves(r, c, board, self.last_move))
        return moves

    def get_legal_moves(self, color, board=None):
        if board is None:
            board = self.board
        legal = []
        for move in self.get_pseudo_moves(color, board):
            # Extra check: castling must not pass through attacked squares
            if move.is_castling:
                if not self._castling_legal(move, color, board):
                    continue
            new_board = self.apply_move_to_board(move, board)
            if not self.is_in_check(color, new_board):
                legal.append(move)
        return legal

    def _castling_legal(self, move, color, board):
        if self.is_in_check(color, board):
            return False
        opponent = 'black' if color == 'white' else 'white'
        row = move.from_sq[0]
        king_col = move.from_sq[1]
        target_col = move.to_sq[1]
        step = 1 if target_col > king_col else -1
        c = king_col + step
        while c != target_col + step:
            if self.square_attacked_by(row, c, opponent, board):
                return False
            c += step
        return True

    # ------------------------------------------------------------------
    # Execute move
    # ------------------------------------------------------------------

    def make_move(self, move):
        piece = self.board[move.from_sq[0]][move.from_sq[1]]
        captured = self.board[move.to_sq[0]][move.to_sq[1]]

        # 50-move clock
        if piece.symbol() == 'P' or captured is not None:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        self.board = self.apply_move_to_board(move, self.board)
        self.last_move = move
        self.move_history.append(move)
        self.turn = 'black' if self.turn == 'white' else 'white'
        self._update_status()

    def _update_status(self):
        legal = self.get_legal_moves(self.turn)
        in_check = self.is_in_check(self.turn, self.board)

        if not legal:
            if in_check:
                self.status = 'checkmate'
                self.winner = 'black' if self.turn == 'white' else 'white'
            else:
                self.status = 'stalemate'
        elif self.halfmove_clock >= 100:
            self.status = 'draw'
        elif self._insufficient_material():
            self.status = 'draw'

    def _insufficient_material(self):
        pieces = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p is not None:
                    pieces.append(p.symbol())
        # Only kings left
        if all(s == 'K' for s in pieces):
            return True
        # King + bishop/knight vs king
        non_kings = [s for s in pieces if s != 'K']
        if len(non_kings) == 1 and non_kings[0] in ('B', 'N'):
            return True
        return False

    def get_legal_moves_for_square(self, row, col):
        piece = self.board[row][col]
        if piece is None or piece.color != self.turn:
            return []
        return [m for m in self.get_legal_moves(self.turn) if m.from_sq == (row, col)]
