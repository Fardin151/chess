import pygame
import os

SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
STATUS_HEIGHT = 50
WINDOW_WIDTH = BOARD_SIZE
WINDOW_HEIGHT = BOARD_SIZE + STATUS_HEIGHT

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT_SEL = (246, 246, 105, 180)
HIGHLIGHT_MOVE = (106, 135, 77)
CHECK_COLOR = (200, 50, 50, 160)
STATUS_BG = (40, 40, 40)
WHITE_TEXT = (255, 255, 255)
PROMO_BG = (50, 50, 50)
PROMO_BORDER = (200, 200, 200)


UNICODE_PIECES = {
    ('white', 'K'): '♔', ('white', 'Q'): '♕', ('white', 'R'): '♖',
    ('white', 'B'): '♗', ('white', 'N'): '♘', ('white', 'P'): '♙',
    ('black', 'K'): '♚', ('black', 'Q'): '♛', ('black', 'R'): '♜',
    ('black', 'B'): '♝', ('black', 'N'): '♞', ('black', 'P'): '♟',
}


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 18, bold=True)
        self.big_font = pygame.font.SysFont('Arial', 28, bold=True)
        # Use a font that has chess unicode glyphs
        self.piece_font = pygame.font.SysFont('Segoe UI Symbol', 54)
        self.piece_images = {}
        self._load_images()

    def _load_images(self):
        asset_dir = os.path.join(os.path.dirname(__file__), 'assets', 'pieces')
        names = {
            ('white', 'K'): 'wK', ('white', 'Q'): 'wQ', ('white', 'R'): 'wR',
            ('white', 'B'): 'wB', ('white', 'N'): 'wN', ('white', 'P'): 'wP',
            ('black', 'K'): 'bK', ('black', 'Q'): 'bQ', ('black', 'R'): 'bR',
            ('black', 'B'): 'bB', ('black', 'N'): 'bN', ('black', 'P'): 'bP',
        }
        for key, name in names.items():
            path = os.path.join(asset_dir, f'{name}.png')
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.piece_images[key] = pygame.transform.smoothscale(
                    img, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))

    def draw(self, game, selected_sq, legal_move_targets, promotion_pending):
        self._draw_board(game, selected_sq, legal_move_targets)
        self._draw_pieces(game.board)
        self._draw_status(game)
        if promotion_pending:
            self._draw_promotion_menu(promotion_pending)

    def _draw_board(self, game, selected_sq, legal_move_targets):
        in_check_king = None
        if game.is_in_check(game.turn, game.board):
            from board import find_king
            in_check_king = find_king(game.board, game.turn)

        for r in range(8):
            for c in range(8):
                x, y = c * SQUARE_SIZE, r * SQUARE_SIZE
                color = LIGHT if (r + c) % 2 == 0 else DARK
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

                if selected_sq == (r, c):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill((246, 246, 105, 160))
                    self.screen.blit(s, (x, y))

                if (r, c) in legal_move_targets:
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    piece = game.board[r][c]
                    if piece is not None:
                        s.fill((106, 135, 77, 160))
                        self.screen.blit(s, (x, y))
                    else:
                        pygame.draw.circle(s, (106, 135, 77, 160),
                                           (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 14)
                        self.screen.blit(s, (x, y))

                if in_check_king == (r, c):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill((200, 50, 50, 160))
                    self.screen.blit(s, (x, y))

    def _draw_pieces(self, board):
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece is None:
                    continue
                key = (piece.color, piece.symbol())
                x = c * SQUARE_SIZE + 5
                y = r * SQUARE_SIZE + 5
                if key in self.piece_images:
                    self.screen.blit(self.piece_images[key], (x, y))
                else:
                    sym = UNICODE_PIECES.get(key, piece.symbol())
                    outline_col = (0, 0, 0) if piece.color == 'white' else (255, 255, 255)
                    fill_col = (255, 255, 255) if piece.color == 'white' else (20, 20, 20)
                    cx = c * SQUARE_SIZE + SQUARE_SIZE // 2
                    cy = r * SQUARE_SIZE + SQUARE_SIZE // 2
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        s = self.piece_font.render(sym, True, outline_col)
                        self.screen.blit(s, (cx - s.get_width()//2 + dx, cy - s.get_height()//2 + dy))
                    s = self.piece_font.render(sym, True, fill_col)
                    self.screen.blit(s, (cx - s.get_width()//2, cy - s.get_height()//2))

    def _draw_status(self, game):
        y = BOARD_SIZE
        pygame.draw.rect(self.screen, STATUS_BG, (0, y, WINDOW_WIDTH, STATUS_HEIGHT))
        if game.status == 'playing':
            in_check = game.is_in_check(game.turn, game.board)
            msg = f"{game.turn.capitalize()}'s turn"
            if in_check:
                msg += '  CHECK!'
        elif game.status == 'checkmate':
            msg = f'Checkmate! {game.winner.capitalize()} wins!'
        elif game.status == 'stalemate':
            msg = 'Stalemate — Draw!'
        else:
            msg = 'Draw!'
        surf = self.font.render(msg, True, WHITE_TEXT)
        self.screen.blit(surf, (10, y + (STATUS_HEIGHT - surf.get_height()) // 2))

    def _draw_promotion_menu(self, info):
        color, from_sq, to_sq = info
        pieces = ['Q', 'R', 'B', 'N']
        box_w, box_h = 60, 60
        total_w = len(pieces) * box_w + 20
        x0 = (WINDOW_WIDTH - total_w) // 2
        y0 = BOARD_SIZE // 2 - box_h // 2

        # Background
        pygame.draw.rect(self.screen, PROMO_BG, (x0 - 10, y0 - 10, total_w + 20, box_h + 20), border_radius=8)
        pygame.draw.rect(self.screen, PROMO_BORDER, (x0 - 10, y0 - 10, total_w + 20, box_h + 20), 2, border_radius=8)

        for i, sym in enumerate(pieces):
            bx = x0 + i * box_w + 10
            by = y0
            pygame.draw.rect(self.screen, (80, 80, 80), (bx, by, box_w - 4, box_h - 4), border_radius=4)
            key = (color, sym)
            if key in self.piece_images:
                img = pygame.transform.smoothscale(self.piece_images[key], (box_w - 10, box_h - 10))
                self.screen.blit(img, (bx + 3, by + 3))
            else:
                uni = UNICODE_PIECES.get(key, sym)
                s = self.piece_font.render(uni, True, (255, 255, 255))
                self.screen.blit(s, (bx + (box_w - s.get_width()) // 2,
                                     by + (box_h - s.get_height()) // 2))

    def promo_box_rects(self, color):
        pieces = ['Q', 'R', 'B', 'N']
        box_w, box_h = 60, 60
        total_w = len(pieces) * box_w + 20
        x0 = (WINDOW_WIDTH - total_w) // 2
        y0 = BOARD_SIZE // 2 - box_h // 2
        rects = []
        for i in range(len(pieces)):
            bx = x0 + i * box_w + 10
            rects.append(pygame.Rect(bx, y0, box_w - 4, box_h - 4))
        return list(zip(pieces, rects))

    def sq_from_pos(self, pos):
        x, y = pos
        if y >= BOARD_SIZE:
            return None
        return (y // SQUARE_SIZE, x // SQUARE_SIZE)
