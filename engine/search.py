# engine/search.py
# Minimax with Alpha-Beta Pruning - OOP implementation

import chess
from typing import Optional
from engine.interfaces import SearchStrategy, EvaluatorInterface
from engine.move_ordering import CaptureFirstOrdering, MoveOrderingStrategy
from engine.evaluation import HeuristicEvaluator


class AlphaBetaSearch(SearchStrategy):
    """Minimax with Alpha-Beta pruning - Primary search algorithm"""
    
    def __init__(self, max_depth: int = 4, evaluator: EvaluatorInterface = None, 
                 move_ordering: MoveOrderingStrategy = None):
        self.max_depth: int = max_depth
        self.evaluator: EvaluatorInterface = evaluator or HeuristicEvaluator()
        self.move_ordering: MoveOrderingStrategy = move_ordering or CaptureFirstOrdering()
        self._nodes_evaluated: int = 0
    
    def search(self, board: chess.Board) -> Optional[chess.Move]:
        """Primary public method - finds best move from current position"""
        self._nodes_evaluated = 0
        best_move = None
        best_value = float('-inf')
        
        moves = self.move_ordering.order_moves(board, list(board.legal_moves))
        
        for move in moves:
            board.push(move)
            move_value = self._alphabeta(
                board, self.max_depth - 1, 
                float('-inf'), float('inf'), 
                False  # opponent's turn (minimizing)
            )
            board.pop()
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
        
        print(f"[Search] Evaluated {self._nodes_evaluated} nodes")
        return best_move
    
    def _alphabeta(self, board: chess.Board, depth: int, 
                   alpha: float, beta: float, is_maximizing: bool) -> float:
        """Recursive Alpha-Beta search core"""
        self._nodes_evaluated += 1
        
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            moves = self.move_ordering.order_moves(board, list(board.legal_moves))
            
            for move in moves:
                board.push(move)
                evaluation = self._alphabeta(board, depth - 1, alpha, beta, False)
                board.pop()
                
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            moves = self.move_ordering.order_moves(board, list(board.legal_moves))
            
            for move in moves:
                board.push(move)
                evaluation = self._alphabeta(board, depth - 1, alpha, beta, True)
                board.pop()
                
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
    
    def get_search_depth(self) -> int:
        return self.max_depth
    
    def set_search_depth(self, depth: int) -> None:
        self.max_depth = max(1, depth)
    
    def get_nodes_evaluated(self) -> int:
        return self._nodes_evaluated


class MinimaxSearch(SearchStrategy):
    """Basic Minimax without pruning (for comparison/benchmarking)"""
    
    def __init__(self, max_depth: int = 3, evaluator: EvaluatorInterface = None):
        self.max_depth = max_depth
        self.evaluator = evaluator or HeuristicEvaluator()
    
    def search(self, board: chess.Board) -> Optional[chess.Move]:
        best_move = None
        best_value = float('-inf')
        
        for move in board.legal_moves:
            board.push(move)
            move_value = self._minimax(board, self.max_depth - 1, False)
            board.pop()
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
        
        return best_move
    
    def _minimax(self, board: chess.Board, depth: int, is_maximizing: bool) -> float:
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval_val = self._minimax(board, depth - 1, False)
                board.pop()
                max_eval = max(max_eval, eval_val)
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_val = self._minimax(board, depth - 1, True)
                board.pop()
                min_eval = min(min_eval, eval_val)
            return min_eval
    
    def get_search_depth(self) -> int:
        return self.max_depth