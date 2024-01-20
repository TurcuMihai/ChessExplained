import chess

board = chess.Board()

with open('games.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

games = [line.split(' ') for line in lines]
for game in games:
    for i, move in enumerate(game):
        if '+' in move:
            game[i] = move[:-1]
            
white_moves = []
black_moves = []

for game in games:
    white = []
    black = []
    board.reset()
    for move in game:
        if board.turn:
            white.append(move)
        else:
            black.append(move)
        board.push_san(move)
        #mov = board.peek()
 
        
        if len(white) > 5:
            white.pop(0)
        if len(black) > 5:
            black.pop(0)
   
    if '#' in white[len(white) - 1]:
        white_moves.append(white)
    if '#' in black[len(black) - 1]:
        black_moves.append(black)
    

white_moves_freq = {}
black_moves_freq = {}

for move in white_moves:
    if tuple(move[-3:]) in white_moves_freq:
        white_moves_freq[tuple(move[-3:])] += 1
    else:
        white_moves_freq[tuple(move[-3:])] = 1
for move in black_moves:
    if tuple(move[-3:]) in black_moves_freq:
        black_moves_freq[tuple(move[-3:])] += 1
    else:
        black_moves_freq[tuple(move[-3:])] = 1

print('White moves:')
for move in white_moves_freq:
    if (white_moves_freq[tuple(move[-3:])] > 1):
        print(move, white_moves_freq[move[-3:]])

print('\nBlack moves:')
for move in black_moves_freq:
    if (black_moves_freq[tuple(move[-3:])] > 1):
        print(move, black_moves_freq[move[-3:]])
