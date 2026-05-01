# engine/chess_engine.py
# Facade Pattern - Main interface for the chess AI system

import chess
from typing import Optional, List
from engine.interfaces import SearchStrategy
from engine.search import AlphaBetaSearch
from engine.evaluation import HeuristicEvaluator


class ChessEngine:
    """
    Facade Pattern: Main interface for the chess AI system.
    Encapsulates search, evaluation, and move generation.
    """
    
    def __init__(self, search_strategy: SearchStrategy = None, max_depth: int = 4):
        self._search_strategy: SearchStrategy = search_strategy or AlphaBetaSearch(max_depth=max_depth)
        self._evaluator = HeuristicEvaluator()
        self._move_history: List[chess.Move] = []
    
    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Primary method - compute best move for current position"""
        if board.is_game_over():
            return None
        
        best_move = self._search_strategy.search(board)
        
        if best_move:
            self._move_history.append(best_move)
            # Keep history bounded
            if len(self._move_history) > 10:
                self._move_history.pop(0)
        
        return best_move
    
    def set_search_strategy(self, strategy: SearchStrategy) -> None:
        """Dynamically change search algorithm (Strategy Pattern)"""
        self._search_strategy = strategy
    
    def get_search_strategy(self) -> SearchStrategy:
        """Return current search strategy"""
        return self._search_strategy
    
    def get_search_depth(self) -> int:
        return self._search_strategy.get_search_depth()
    
    def set_search_depth(self, depth: int) -> None:
        """Adjust search depth (higher depth = stronger but slower)"""
        if hasattr(self._search_strategy, 'set_search_depth'):
            self._search_strategy.set_search_depth(depth)
    
    def evaluate_position(self, board: chess.Board) -> int:
        """Expose evaluation for debugging/display"""
        return self._evaluator.evaluate(board)
    
    def get_move_history(self) -> List[chess.Move]:
        """Return history of engine moves"""
        return self._move_history.copy()