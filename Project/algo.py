import chess

all_games = []
white_wins = []
black_wins = []

def parser():
    board = chess.Board()
    with open('data/games.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    games = [line.split(' ') for line in lines]

    for game in games:
        for i, move in enumerate(game):
            game[i] = ''.join(char for char in move if char not in ['+', 'x'])

    for game in games:
        white = []
        black = []
        current_game = []
        board.reset()
        for move in game:
            if len(move) > 2:
                if board.turn:
                    white.append(move)
                else:
                    black.append(move)
                board.push_san(move)
                current_game.append(str(move))
            else:
                board.push_san(move)
                current_move = board.peek()
                if not board.turn:
                    white.append(str(current_move))
                    current_game.append(str(current_move))
                else:
                    black.append(str(current_move))
                    current_game.append(str(current_move))
        if '#' in white[len(white) - 1]:
            white[len(white) - 1] = white[len(white) - 1][:-1]
            white_wins.append(white)
        if '#' in black[len(black) - 1]:
            black[len(black) - 1] = black[len(black) - 1][:-1]
            black_wins.append(black)
        if '#' in current_game[len(current_game) - 1]:
            current_game[len(current_game) - 1] = current_game[len(current_game) - 1][:-1]
        all_games.append(current_game)


parser()

print(all_games[:6])
print("\n")
print(white_wins[:2])
print("\n")
print(black_wins[:2])

