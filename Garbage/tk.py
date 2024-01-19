import chess


sah_matrix = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", ".", "p", "p", "p", "p"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "N", "."],
    ["P", "P", "P", "P", ".", "P", "N", "P"],
    ["R", "N", "B", "Q", "N", "B", "N", "R"]
]


board = chess.Board()

for row_index, row in enumerate(sah_matrix):
    for col_index, piece_symbol in enumerate(row):
        square = chess.square(col_index, 7 - row_index)  # Conversia dintre coordonatele matricei și coordonatele tablei de șah
        piece = chess.Piece.from_symbol(piece_symbol) if piece_symbol != "." else None
        board.set_piece_at(square, piece)


print(board)
print(board.is_valid())