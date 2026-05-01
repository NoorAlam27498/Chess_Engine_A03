# engine/interfaces.py
# Abstract base classes for Strategy Pattern

from abc import ABC, abstractmethod
import chess
from typing import List, Optional


class SearchStrategy(ABC):
    """Strategy Pattern: Abstract interface for search algorithms"""
    
    @abstractmethod
    def search(self, board: chess.Board) -> Optional[chess.Move]:
        """Find the best move for the current position"""
        pass
    
    @abstractmethod
    def get_search_depth(self) -> int:
        """Return current search depth configuration"""
        pass


class EvaluatorInterface(ABC):
    """Strategy Pattern: Interface for position evaluation"""
    
    @abstractmethod
    def evaluate(self, board: chess.Board) -> int:
        """
        Evaluate board position from current player's perspective.
        Positive = good for player to move, Negative = bad.
        """
        pass


class MoveOrderingStrategy(ABC):
    """Strategy Pattern: Interface for move ordering"""
    
    @abstractmethod
    def order_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
        """Sort moves to improve pruning efficiency"""
        pass