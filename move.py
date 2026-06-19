from dataclasses import dataclass, field


@dataclass
class Move:
    from_sq: tuple
    to_sq: tuple
    promotion: str | None = None  # 'Q', 'R', 'B', 'N'
    is_en_passant: bool = False
    is_castling: bool = False

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.from_sq == other.from_sq and self.to_sq == other.to_sq
                and self.promotion == other.promotion)

    def __hash__(self):
        return hash((self.from_sq, self.to_sq, self.promotion))
