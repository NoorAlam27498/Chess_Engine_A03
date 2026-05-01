# ♟️ Adversarial Search-Based Chess Engine

## Minimax with Alpha-Beta Pruning (Depth 4)

---

## 📌 Project Overview

This project implements a fully functional adversarial chess engine built using **Minimax search with Alpha-Beta pruning**, integrated into a PyQt6-based graphical interface.

The system models chess as a two-player, zero-sum, deterministic, perfect-information, turn-based adversarial search problem. The engine evaluates positions using a domain-specific heuristic and searches the game tree to a fixed depth of **4 plies** (2 full moves per side).

---

## 👥 Authors

| Name | Roll Number | Section |
|------|-------------|---------|
| Noor Alam | 23i-3089 | SE-6B |
| Moeez Abid | 23i-3033 | SE-6B |
| Ahnaf Abdullah | 23i-3012 | SE-6B |

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| ♟️ Full Chess Rules | Castling, en passant, pawn promotion fully implemented |
| 🔍 Minimax Algorithm | Recursive game tree search for optimal decision making |
| ✂️ Alpha-Beta Pruning | Eliminates irrelevant branches for 300x speedup |
| 📊 Heuristic Evaluation | Material + Positional + Mobility scoring |
| 🎨 PyQt6 GUI | Professional graphical interface with SVG pieces |
| 💡 Move Highlighting | Visual indicators for legal moves and captures |
| 🏆 Game Over Detection | Checkmate, stalemate, insufficient material handling |
| 🔄 Move Ordering | Capture-first strategy for maximum pruning efficiency |

---

## 🏗️ Architecture

The project follows a **Layered Architecture** with four distinct layers:

| Layer | Description | Files |
|-------|-------------|-------|
| **Presentation Layer** | GUI, board rendering, user input | `gui/` |
| **Application Layer** | Facade pattern, engine orchestration | `engine/chess_engine.py` |
| **Business Logic Layer** | Search, evaluation, move ordering | `engine/search.py`, `engine/evaluation.py`, `engine/move_ordering.py` |
| **Data Access Layer** | External libraries, assets | `python-chess`, `PyQt6`, `assets/` |

---

## 📂 Project Structure
Chess_Engine_A03/
│
├── main.py # Application entry point
├── README.md # This file
├── requirements.txt # Python dependencies
│
├── gui/ # PRESENTATION LAYER
│ ├── init.py
│ ├── main_window.py # Main application window
│ └── chess_board_widget.py # Chess board with event handling
│
├── engine/ # APPLICATION & BUSINESS LOGIC LAYERS
│ ├── init.py
│ ├── interfaces.py # Abstract base classes (Strategy Pattern)
│ ├── chess_engine.py # Facade pattern - main engine interface
│ ├── search.py # AlphaBetaSearch, MinimaxSearch
│ ├── evaluation.py # HeuristicEvaluator, PieceValues (Singleton)
│ └── move_ordering.py # CaptureFirstOrdering strategy
│
└── assets/
└── pieces/ # SVG piece images (12 files)
├── wp.svg, wr.svg, wn.svg, wb.svg, wq.svg, wk.svg
└── bp.svg, br.svg, bn.svg, bb.svg, bq.svg, bk.svg

---

## 💻 Installation Instructions

### Prerequisites

Before installing, ensure you have the following installed on your system:

| Requirement | Minimum Version | Check Command |
|-------------|-----------------|---------------|
| Python      | 3.9 or higher   |python --version|
| pip         | 20.0 or higher  |pip --version  |

### Step 1: Clone the Repository

```
git clone https://github.com/NoorAlam27498/Chess_Engine_A03.git
cd Chess_Engine_A03


### Step 2: Create Virtual Environment (Recommended)
Windows:
python3 -m venv venv
source venv/bin/activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

### Step 3: Install Required Libraries
pip install -r requirements.txt

or

pip install PyQt6 python-chess

### Step 4: Verify Asset Files
Ensure the following SVG files exist in assets/pieces/ folder:

White Pieces	        Black Pieces
wp.svg (white pawn)	bp.svg (black pawn)
wr.svg (white rook)	br.svg (black rook)
wn.svg (white knight)	bn.svg (black knight)
wb.svg (white bishop)	bb.svg (black bishop)
wq.svg (white queen)	bq.svg (black queen)
wk.svg (white king)	bk.svg (black king)

🚀 Execution Instructions
Run the Application
bash
python main.py
What to Expect
Upon successful execution, the following will appear:

A maximized window with a chess board in the center

Left and right panels (reserved for future features)

Initial board position with all pieces correctly placed

Status bar showing "White's Turn"

Console Output (Background)
text
Loading piece assets...
Assets loaded successfully: 12/12 pieces
Engine initialized: Alpha-Beta Search (Depth 4)
GUI started on main thread
🎮 How to Play
Game Rules
White (Human) moves first

Black (AI) responds automatically

Standard chess rules apply (check, checkmate, stalemate, castling, en passant, promotion)

Mouse Controls
Action	Method
Select a piece	Left-click on your piece (White pieces only on your turn)
Move a piece	Left-click on a highlighted destination square
Cancel selection	Click anywhere else or click the same piece again
Promote a pawn	Dialog appears automatically when pawn reaches last rank
Visual Indicators
Indicator	Meaning
Light gray square	Currently selected piece
Small grey circle	Legal non-capture destination
Red square	Legal capture destination
Game Flow
text
1. Player clicks on a white piece → Square highlights
2. Player clicks on a highlighted destination → Piece moves
3. AI thinks for ~0.4 seconds
4. AI responds with its move
5. Board updates automatically
6. Continue until game ends (checkmate or draw)
⚙️ Configuration
Changing Search Depth
The engine searches to depth 4 by default. To change this, edit engine/search.py:

python
class AlphaBetaSearch(SearchStrategy):
    def __init__(self, max_depth: int = 4, ...):  # Change 4 to desired depth
Depth vs Performance
Depth	Avg Time	Playing Strength
2	<0.05 sec	Very weak
3	~0.1 sec	Weak
4	~0.4 sec	Decent club player (Default)
5	~3.5 sec	Strong but slower
🧪 Testing the Application
Basic Functionality Test
bash
python main.py
Then verify:

Window opens successfully

All pieces are displayed correctly

You can click and move pieces

AI responds after your move

Sample Console Output During Game
text
Selected: e2
Moved: e2 -> e4
Engine thinking...
[Search] Evaluated 3842 nodes
Engine moved: e7e5

Selected: g1
Moved: g1 -> f3
Engine thinking...
[Search] Evaluated 4251 nodes
Engine moved: g8f6
📊 Algorithm Description
Search Algorithm: Minimax with Alpha-Beta Pruning
Time Complexity (best case): O(b^(d/2)) where b ≈ 35, d = 4

Time Complexity (worst case): O(b^d)

Nodes evaluated per move: ~2,000 - 5,000

Speedup factor: ~300x compared to naive minimax

Heuristic Evaluation Function: f(s) = M(s) + P(s) + 0.1 × Mob(s)
Component	Description
M(s)	Material balance (Pawn=100, Knight=320, Bishop=330, Rook=500, Queen=900, King=20000)
P(s)	Positional advantage from piece-square tables
Mob(s)	Mobility (number of legal moves)
📁 Repository Link
GitHub Repository: https://github.com/NoorAlam27498/Chess_Engine_A03

