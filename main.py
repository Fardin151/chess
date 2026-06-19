import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pygame
from game import GameState
from renderer import Renderer, WINDOW_WIDTH, WINDOW_HEIGHT
from move import Move


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()

    game = GameState()
    renderer = Renderer(screen)

    selected_sq = None
    legal_moves = []
    legal_targets = set()
    promotion_pending = None  # (color, from_sq, to_sq) waiting for piece choice

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = GameState()
                    selected_sq = None
                    legal_moves = []
                    legal_targets = set()
                    promotion_pending = None

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                # Handle promotion menu
                if promotion_pending is not None:
                    color, from_sq, to_sq = promotion_pending
                    for sym, rect in renderer.promo_box_rects(color):
                        if rect.collidepoint(pos):
                            move = Move(from_sq, to_sq, promotion=sym)
                            game.make_move(move)
                            promotion_pending = None
                            selected_sq = None
                            legal_moves = []
                            legal_targets = set()
                    continue

                if game.status != 'playing':
                    continue

                sq = renderer.sq_from_pos(pos)
                if sq is None:
                    continue

                r, c = sq

                if selected_sq is None:
                    # Select a piece
                    piece = game.board[r][c]
                    if piece is not None and piece.color == game.turn:
                        selected_sq = sq
                        legal_moves = game.get_legal_moves_for_square(r, c)
                        legal_targets = {m.to_sq for m in legal_moves}
                else:
                    # Try to execute a move
                    matching = [m for m in legal_moves if m.to_sq == sq]
                    if matching:
                        move = matching[0]
                        # Check for promotion with multiple choices
                        promos = [m for m in matching if m.promotion]
                        if promos:
                            # Show promotion picker
                            promotion_pending = (game.turn, selected_sq, sq)
                            selected_sq = None
                            legal_moves = []
                            legal_targets = set()
                        else:
                            game.make_move(move)
                            selected_sq = None
                            legal_moves = []
                            legal_targets = set()
                    else:
                        # Re-select or deselect
                        piece = game.board[r][c]
                        if piece is not None and piece.color == game.turn:
                            selected_sq = sq
                            legal_moves = game.get_legal_moves_for_square(r, c)
                            legal_targets = {m.to_sq for m in legal_moves}
                        else:
                            selected_sq = None
                            legal_moves = []
                            legal_targets = set()

        screen.fill((0, 0, 0))
        renderer.draw(game, selected_sq, legal_targets, promotion_pending)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
