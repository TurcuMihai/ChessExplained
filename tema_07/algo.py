import chess



white_wins = []
black_wins = []


def parser():
    white_wins = []
    black_wins = []
    board = chess.Board()
    with open('games.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    games = [line.split(' ') for line in lines]
    for game in games:
        for i, move in enumerate(game):
            game[i] = ''.join(char for char in move if char not in ['+', 'x'])

    for game in games:
        white = []
        black = []
        board.reset()
        for move in game:
            if len(move) > 2:
                if board.turn:
                    white.append(move)
                else:
                    black.append(move)
                board.push_san(move)
            else:
                board.push_san(move)
                current_move = board.peek()
                if not board.turn:
                    white.append(str(current_move))
                else:
                    black.append(str(current_move))
                
        if '#' in white[len(white) - 1]:
            white[len(white) - 1] = white[len(white) - 1][:-1]
            white_wins.append(white)
        if '#' in black[len(black) - 1]:
            black[len(black) - 1] = black[len(black) - 1][:-1]
            black_wins.append(black)
        
    print(white_wins[0])
    print(black_wins[0])
    print(len(white_wins))
    print(len(black_wins))
parser()


