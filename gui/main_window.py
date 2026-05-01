# gui/main_window.py
# Main application window with left/right panels and chessboard

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from gui.chess_board_widget import ChessBoardWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adversarial Search Chess Engine - Minimax with Alpha-Beta Pruning")

        # Central container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main horizontal layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Left panel (can be used for move history or settings later)
        self.left_panel = QWidget()
        self.left_panel.setMinimumWidth(250)
        self.left_panel.setStyleSheet("background-color: #2b2b2b;")

        # Right panel (can be used for evaluation or controls later)
        self.right_panel = QWidget()
        self.right_panel.setMinimumWidth(250)
        self.right_panel.setStyleSheet("background-color: #2b2b2b;")

        # Center board widget
        self.board_widget = ChessBoardWidget()
        self.board_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        
        # Calculate appropriate board size based on screen
        screen_rect = self.screen().availableGeometry()
        max_board_size = min(screen_rect.width() - 500, screen_rect.height())
        self.board_widget.setMinimumSize(int(max_board_size * 0.90), int(max_board_size * 0.90))
        
        # Add widgets to main layout
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.board_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.right_panel)

        # Start maximized
        self.showMaximized()