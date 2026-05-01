# gui/chess_board_widget.py
# Chess board GUI with click-to-select interaction and AI integration

from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QPushButton
)
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtSvg import QSvgRenderer
import chess
import os

from engine.chess_engine import ChessEngine

LIGHT = QColor("#F0D9B5")
DARK = QColor("#B58863")


class ChessBoardWidget(QWidget):
    """Observer Pattern: Widget observes board state and updates display"""
    
    def __init__(self):
        super().__init__()

        self.board = chess.Board()
        self.selected_square = None
        
        # Composition: ChessEngine is a component of the widget
        self.engine = ChessEngine(max_depth=4)

        self.setMinimumSize(400, 400)

        # Load SVG renderers
        self.piece_renderers = {}
        self.load_pieces()

    # ----------------------------
    # Load Piece Assets
    # ----------------------------
    def load_pieces(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pieces_path = os.path.join(base_path, "assets", "pieces")

        pieces = ["p", "r", "n", "b", "q", "k"]
        colors = ["w", "b"]

        for color in colors:
            for piece in pieces:
                key = color + piece
                path = os.path.join(pieces_path, key + ".svg")

                if not os.path.exists(path):
                    print("Missing file:", path)
                    continue

                with open(path, "rb") as f:
                    data = f.read()

                renderer = QSvgRenderer(data)

                if not renderer.isValid():
                    print("Invalid SVG:", path)

                self.piece_renderers[key] = renderer

    # ----------------------------
    # Paint Board
    # ----------------------------
    def paintEvent(self, event):
        painter = QPainter(self)

        size = min(self.width(), self.height())
        square_size = size // 8

        x_offset = (self.width() - size) // 2
        y_offset = (self.height() - size) // 2

        # Draw squares
        for row in range(8):
            for col in range(8):
                color = LIGHT if (row + col) % 2 == 0 else DARK
                painter.fillRect(
                    x_offset + col * square_size,
                    y_offset + row * square_size,
                    square_size,
                    square_size,
                    color
                )

        # Highlight selected square and legal moves
        if self.selected_square is not None:
            file = chess.square_file(self.selected_square)
            rank = 7 - chess.square_rank(self.selected_square)

            painter.fillRect(
                x_offset + file * square_size,
                y_offset + rank * square_size,
                square_size,
                square_size,
                QColor(200, 200, 200, 120)
            )

            for move in self.board.legal_moves:
                if move.from_square == self.selected_square:
                    target_file = chess.square_file(move.to_square)
                    target_rank = 7 - chess.square_rank(move.to_square)

                    target_x = x_offset + target_file * square_size
                    target_y = y_offset + target_rank * square_size

                    # If move captures a piece → highlight full square red
                    if self.board.is_capture(move):
                        painter.fillRect(
                            target_x,
                            target_y,
                            square_size,
                            square_size,
                            QColor(200, 50, 50, 150)
                        )
                    # Otherwise draw small grey circle
                    else:
                        radius = square_size / 6
                        center_x = target_x + square_size / 2
                        center_y = target_y + square_size / 2

                        painter.setBrush(QColor(150, 150, 150, 180))
                        painter.setPen(Qt.PenStyle.NoPen)
                        painter.drawEllipse(
                            int(center_x - radius),
                            int(center_y - radius),
                            int(radius * 2),
                            int(radius * 2)
                        )

        # Draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                file = chess.square_file(square)
                rank = 7 - chess.square_rank(square)

                key = ("w" if piece.color else "b") + piece.symbol().lower()
                renderer = self.piece_renderers.get(key)

                if renderer:
                    rect = QRectF(
                        x_offset + file * square_size,
                        y_offset + rank * square_size,
                        square_size,
                        square_size
                    )
                    renderer.render(painter, rect)

    # ----------------------------
    # Promotion Dialog
    # ----------------------------
    def show_promotion_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Promotion")

        layout = QVBoxLayout(dialog)

        promotion_choice = {"piece": None}

        def choose(piece_type):
            promotion_choice["piece"] = piece_type
            dialog.accept()

        queen_btn = QPushButton("Queen")
        rook_btn = QPushButton("Rook")
        bishop_btn = QPushButton("Bishop")
        knight_btn = QPushButton("Knight")

        queen_btn.clicked.connect(lambda: choose(chess.QUEEN))
        rook_btn.clicked.connect(lambda: choose(chess.ROOK))
        bishop_btn.clicked.connect(lambda: choose(chess.BISHOP))
        knight_btn.clicked.connect(lambda: choose(chess.KNIGHT))

        layout.addWidget(queen_btn)
        layout.addWidget(rook_btn)
        layout.addWidget(bishop_btn)
        layout.addWidget(knight_btn)

        dialog.exec()

        return promotion_choice["piece"]

    # ----------------------------
    # Game Over Dialog
    # ----------------------------
    def show_game_over_dialog(self):
        result = self.board.result()
        message = ""

        if self.board.is_checkmate():
            if self.board.turn:
                message = "Checkmate!\nBlack Wins!"
            else:
                message = "Checkmate!\nWhite Wins!"

        elif self.board.is_stalemate():
            message = "Stalemate!\nIt's a Draw."

        elif self.board.is_insufficient_material():
            message = "Draw!\nInsufficient Material."

        elif self.board.is_seventyfive_moves():
            message = "Draw!\n75-Move Rule."

        elif self.board.is_fivefold_repetition():
            message = "Draw!\nFivefold Repetition."

        else:
            message = f"Game Over!\nResult: {result}"

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(message)
        msg_box.exec()

    # ----------------------------
    # Mouse Interaction
    # ----------------------------
    def mousePressEvent(self, event):
        size = min(self.width(), self.height())
        square_size = size // 8

        x_offset = (self.width() - size) // 2
        y_offset = (self.height() - size) // 2

        col = int((event.position().x() - x_offset) // square_size)
        row = int((event.position().y() - y_offset) // square_size)

        if not (0 <= col < 8 and 0 <= row < 8):
            return

        clicked_square = chess.square(col, 7 - row)
        piece = self.board.piece_at(clicked_square)

        # First Click (Select)
        if self.selected_square is None:
            if piece and piece.color == self.board.turn:
                self.selected_square = clicked_square
                print("Selected:", chess.square_name(clicked_square))
                self.update()

        # Second Click (Move)
        else:
            move = chess.Move(self.selected_square, clicked_square)

            piece = self.board.piece_at(self.selected_square)

            # Handle pawn promotion
            if piece and piece.piece_type == chess.PAWN:
                target_rank = chess.square_rank(clicked_square)

                if target_rank == 7 or target_rank == 0:
                    chosen_piece = self.show_promotion_dialog()

                    if chosen_piece is None:
                        self.selected_square = None
                        self.update()
                        return

                    move = chess.Move(
                        self.selected_square,
                        clicked_square,
                        promotion=chosen_piece
                    )

            if move in self.board.legal_moves:
                print("Moved:",
                      chess.square_name(self.selected_square),
                      "->",
                      chess.square_name(clicked_square))

                # Apply player move
                self.board.push(move)
                self.selected_square = None
                self.update()

                # Check game over after player move
                if self.board.is_game_over():
                    self.show_game_over_dialog()
                    return

                # Process events to ensure UI updates
                QApplication.processEvents()

                # Request AI move (Black)
                if not self.board.is_game_over():
                    print("Engine thinking...")
                    ai_move = self.engine.get_best_move(self.board)

                    if ai_move:
                        self.board.push(ai_move)
                        print("Engine moved:", ai_move)
                    self.update()
                    
                    # Check game over after engine move
                    if self.board.is_game_over():
                        self.show_game_over_dialog()

            else:
                print("Illegal move:",
                      chess.square_name(self.selected_square),
                      "->",
                      chess.square_name(clicked_square))

                self.selected_square = None

            self.update()