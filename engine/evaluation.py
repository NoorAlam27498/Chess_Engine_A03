# engine/evaluation.py
# Heuristic evaluation with Singleton patterns

import chess
from typing import Dict, List
from engine.interfaces import EvaluatorInterface


class PieceValues:
    """Singleton pattern: Centralized piece valuation"""
    
    _instance = None
    _values: Dict[int, int] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self._values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
    
    def get(self, piece_type: int) -> int:
        return self._values.get(piece_type, 0)
    
    @property
    def all_values(self) -> Dict[int, int]:
        return self._values.copy()


class PieceSquareTables:
    """Singleton pattern: Positional bonus tables"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_tables()
        return cls._instance
    
    def _initialize_tables(self):
        # PAWN_TABLE
        self.PAWN_TABLE = [
            0, 0, 0, 0, 0, 0, 0, 0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5, 5, 10, 25, 25, 10, 5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, -5, -10, 0, 0, -10, -5, 5,
            5, 10, 10, -20, -20, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        
        # KNIGHT_TABLE
        self.KNIGHT_TABLE = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]
        
        # BISHOP_TABLE (reuse knight table)
        self.BISHOP_TABLE = self.KNIGHT_TABLE[:]
        
        # ROOK_TABLE
        self.ROOK_TABLE = [0] * 64
        
        # QUEEN_TABLE
        self.QUEEN_TABLE = [0] * 64
        
        # KING_TABLE
        self.KING_TABLE = [
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            20, 20, 0, 0, 0, 0, 20, 20,
            20, 30, 10, 0, 0, 10, 30, 20
        ]
        
        self._tables = {
            chess.PAWN: self.PAWN_TABLE,
            chess.KNIGHT: self.KNIGHT_TABLE,
            chess.BISHOP: self.BISHOP_TABLE,
            chess.ROOK: self.ROOK_TABLE,
            chess.QUEEN: self.QUEEN_TABLE,
            chess.KING: self.KING_TABLE
        }
    
    def get_positional_value(self, piece_type: int, square: int, is_white: bool) -> int:
        table = self._tables.get(piece_type)
        if not table:
            return 0
        idx = square if is_white else chess.square_mirror(square)
        return table[idx]
    
    def get_table(self, piece_type: int) -> List[int]:
        return self._tables.get(piece_type, [0] * 64)


class HeuristicEvaluator(EvaluatorInterface):
    """Concrete evaluator using material + position + mobility"""
    
    def __init__(self):
        self.piece_values = PieceValues()
        self.position_tables = PieceSquareTables()
        self.mobility_weight: float = 0.1
    
    def evaluate(self, board: chess.Board) -> int:
        # Terminal state detection
        if board.is_checkmate():
            return -999999 if board.turn else 999999
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0
        
        # Material + Positional evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.piece_values.get(piece.piece_type)
                pos_value = self.position_tables.get_positional_value(
                    piece.piece_type, square, piece.color == chess.WHITE
                )
                
                if piece.color == chess.WHITE:
                    score += value + pos_value
                else:
                    score -= (value + pos_value)
        
        # Mobility bonus
        mobility = len(list(board.legal_moves))
        if board.turn == chess.WHITE:
            score += self.mobility_weight * mobility
        else:
            score -= self.mobility_weight * mobility
        
        return int(score)