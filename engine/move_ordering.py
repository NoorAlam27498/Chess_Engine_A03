# engine/move_ordering.py
# Move ordering strategies for alpha-beta pruning efficiency

import chess
from typing import List
from engine.interfaces import MoveOrderingStrategy


class CaptureFirstOrdering(MoveOrderingStrategy):
    """Prioritize capture moves for better alpha-beta pruning"""
    
    def order_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
        return sorted(moves, key=lambda m: board.is_capture(m), reverse=True)


class MVV_LVA_Ordering(MoveOrderingStrategy):
    """Most Valuable Victim - Least Valuable Aggressor ordering"""
    
    _piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 100
    }
    
    def order_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
        def move_score(move: chess.Move) -> float:
            if board.is_capture(move):
                victim = board.piece_at(move.to_square)
                attacker = board.piece_at(move.from_square)
                if victim and attacker:
                    # MVV - LVA heuristic
                    return self._piece_values.get(victim.piece_type, 0) - (self._piece_values.get(attacker.piece_type, 0) / 100.0)
            return 0.0
        return sorted(moves, key=move_score, reverse=True)