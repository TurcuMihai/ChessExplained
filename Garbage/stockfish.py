# import chess
# import chess.svg
# import chess.engine

# def analyze_moves(fen):
#     board = chess.Board(fen)
    
#     # Utilizăm Stockfish, un motor de șah open-source, pentru analiza poziției
#     with chess.engine.SimpleEngine.popen_uci("C:\stockfish\stockfish-windows-x86-64-avx2.exe") as engine:
#         result = engine.play(board, chess.engine.Limit(time=2.0))
#         best_move = result.move
        
#         print("Mutarea recomandată de Stockfish:", best_move.uci())
        
#         # Analizăm scorul poziției după mutarea recomandată
#         info = engine.analyse(board, chess.engine.Limit(time=2.0))
#         print("Scorul poziției după mutarea recomandată:", info["score"])

#         # Explicăm mutarea recomandată
#         explanation = chess.Board.san(board, best_move)
#         print("Explicație:", explanation)

# # Exemplu de folosire
# fen = "rnb1k1nr/pp1pppbp/6p1/8/3P4/8/PPP2PPP/R1BQKBNR b KQkq - 1 5"
# analyze_moves(fen)




import chess
import chess.engine

def explain_best_move(fen):
    board = chess.Board(fen)
    
    # Utilizează Stockfish pentru a obține informații despre cea mai bună mutare
    with chess.engine.SimpleEngine.popen_uci("C:\stockfish\stockfish-windows-x86-64-avx2.exe") as engine:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        best_move = result.move

        # Analizează scorul poziției după mutarea recomandată
        info = engine.analyse(board, chess.engine.Limit(time=2.0))
        score = info["score"].relative.score(mate_score=32767)  # Converteste scorul

        # Generează un mesaj de explicație în funcție de scor și mutare
        explanation = generate_explanation(score, best_move)

        return explanation

def generate_explanation(score, best_move):
    if score > 0:
        return f"Prin efectuarea mutării {best_move.uci()}, poziția devine avantajoasă pentru tine."
    elif score < 0:
        return f"Prin efectuarea mutării {best_move.uci()}, poziția devine avantajoasă pentru adversar."
    else:
        return f"Mutarea {best_move.uci()} menține echilibrul poziției."

# Exemplu de folosire
fen = "r1bqk2r/pp1p1ppp/2n1pn2/2b5/2B1P3/8/PPPP1PPP/R1BQK1NR b KQkq - 1 6"
explanation = explain_best_move(fen)
print(explanation)


















import chess
import chess.engine

def explain_best_move(fen):
    board = chess.Board(fen)
    
    # Utilizează Stockfish pentru a obține informații despre cea mai bună mutare
    with chess.engine.SimpleEngine.popen_uci("caminhodocasal/stockfish") as engine:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        best_move = result.move

        # Analizează scorul poziției după mutarea recomandată
        info = engine.analyse(board, chess.engine.Limit(time=2.0))
        score = info["score"].relative.score(mate_score=32767)  # Converteste scorul

        # Generează un mesaj de explicație în funcție de scor și mutare
        explanation = generate_explanation(board, score, best_move)

        return explanation

def generate_explanation(board, score, best_move):
    # Converteste coordonatele de la algebraic la coordinat format
    from_square = chess.SQUARE_NAMES.index(best_move.uci()[:2])
    to_square = chess.SQUARE_NAMES.index(best_move.uci()[2:])
    
    # Extrage piesa mutată și piesa capturată (dacă există)
    moved_piece = board.piece_at(from_square)
    captured_piece = board.piece_at(to_square) if board.is_capture(best_move) else None

    explanation = f"Prin efectuarea mutării {best_move.uci()}, "
    
    if captured_piece:
        explanation += f"ai capturat o {captured_piece.symbol()} și "
    
    explanation += f"poziția devine avantajoasă pentru tine, deoarece {reason_for_advantage(board, best_move)}."

    return explanation

def reason_for_advantage(board, move):
    # Exemplu simplificat; implementează logica ta specifică aici
    if move.promotion:
        return f"ai promovat un pion și ai obținut o nouă regină, ceea ce îți oferă o avantaj semnificativ."

    if board.is_capture(move):
        return "ai eliminat o piesă a adversarului, ceea ce îți consolidează poziția."

    return "ai realizat o mutare strategică care îți oferă control asupra centrului tablei."

# Exemplu de folosire
fen = "r1bqk2r/pp1p1ppp/2n1pn2/2b5/2B1P3/8/PPPP1PPP/R1BQK1NR b KQkq - 1 6"
explanation = explain_best_move(fen)
print(explanation)
