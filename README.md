# Chess

A two-player chess game built with Python and Pygame, featuring a graphical board, full rule enforcement, and piece images.

## Features

- Complete chess rules: castling, en passant, pawn promotion, check/checkmate, stalemate
- Draw detection: 50-move rule, insufficient material
- Visual highlights for selected pieces and legal moves
- King highlighted in red when in check
- Promotion picker UI when a pawn reaches the back rank
- PNG piece images with Unicode fallback if images are missing

## Requirements

- Python 3.x
- Pygame

```
pip install pygame
```

## Setup

Optionally download piece images from Wikimedia Commons (falls back to Unicode symbols if skipped):

```
python download_pieces.py
```

## Running

```
python main.py
```

## Controls

| Input | Action |
|---|---|
| Left click | Select a piece / move to a square |
| R | Reset the game |

## Project Structure

```
chess/
├── main.py          # Entry point, event loop
├── game.py          # Game state, move validation, check/checkmate logic
├── board.py         # Board setup and helpers
├── renderer.py      # Pygame rendering
├── move.py          # Move data class
├── download_pieces.py  # Downloads piece PNG assets
└── pieces/
    ├── piece.py     # Base piece class
    ├── pawn.py
    ├── knight.py
    ├── bishop.py
    ├── rook.py
    ├── queen.py
    └── king.py
```
