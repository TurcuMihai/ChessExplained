import chess
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from stockfish import Stockfish
 
white_wins = []
black_wins = []
all_games_white = []
all_games_black = []
exit_conditions = (":q", "quit", "exit","stop","Exit","Stop","Quit","Q","q","STOP","QUIT","EXIT")
ALL_SQUARES = [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
               chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
               chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5,
                chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]
 
def parser():
    board = chess.Board()
    with open('data/games.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    games = [line.split(' ') for line in lines]
 
    for game in games:
        for i, move in enumerate(game):
            game[i] = ''.join(char for char in move if char not in ['+'])
 
    for game in games:
        white = []
        black = []
        board.reset()
        for move in game:
            if len(move) > 2 and move[0] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
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
        all_games_white.append(white)
        if '#' in black[len(black) - 1]:
            black[len(black) - 1] = black[len(black) - 1][:-1]
            black_wins.append(black)
        all_games_black.append(black)
 
    for game in white_wins:
        for i, move in enumerate(game):
            game[i] = ''.join(char for char in move if char not in ['+', 'x'])
    for game in black_wins:
        for i, move in enumerate(game):
            game[i] = ''.join(char for char in move if char not in ['+', 'x'])
    for game in all_games_black:
        for i, move in enumerate(game):
            game[i] = ''.join(char for char in move if char not in ['+', 'x'])
    for game in all_games_white:
            for i, move in enumerate(game):
                game[i] = ''.join(char for char in move if char not in ['+', 'x'])
 
def train():
    trainer = ListTrainer(chatbot)
    trainer.train([
        "Hi",
        "Welcome, friend 🤗",
    ])
 
    with open("data/training.txt", "r", encoding='utf-8') as file:
        line1 = file.readline().strip()
        line2 = file.readline().strip()
        while line1 and line2:         
            trainer.train([line1, line2,])
            line1 = file.readline().strip()
            line2 = file.readline().strip()
 
 
def main():
    print("\n\nBine ai venit! 🤗")
    while True:
        print("\n\nCu ce te pot ajuta astazi? 🥰")
        print("1. Vreau mutarea optima pentru o configuratie FEN. 😎")
        print("2. Am o intrebare legata de regulamentul sahului. 😏")
        print("3. Iesire. 😪")
        choice = input("Alege o optiune: ")
 
        if choice == "1":
            best_move_fen_configuration()
        elif choice == "2":
            rules_question()
        elif choice == "3":
            print("O zi buna! 🤗")
            break
        else:
            print("Alegere invalida!")
 
 
def rules_question():
    exit_conditions = (":q", "quit", "exit")
    print("🧐 Cu ce te pot ajuta? ")
    while True:
        user_input = input("👱 > ")
        if user_input in exit_conditions:
            break
        print(f"🤖 > {chatbot.get_response(user_input)}")

 
def best_move_fen_configuration():
    while True:
        user_input = input("\nIntrodu o configuratie FEN valida: ")
        if user_input in exit_conditions:
            break
        board = chess.Board(user_input)
        stockfish.set_fen_position(user_input)
        for i in range(40):
            if stockfish.is_fen_valid(user_input):
                    best_move_uci = stockfish.get_best_move()
                    best_move = chess.Move.from_uci(best_move_uci)
                    explanation = get_explanation(board, best_move)
                    print("\nTabla inainte de mutare:")
                    print(board)
                    print("\nCea mai buna mutare: ", best_move)
                    print("Explicatie: ", explanation)
                    winning_percentage = compute_winning_percentage(board, best_move)
                    if winning_percentage < 40 or winning_percentage == "Nedefinit":
                        print(f"Aceasta mutare este una obisnuita. ({winning_percentage}%)")
                    elif winning_percentage < 50:
                        print(f"Este o mutare buna. ({winning_percentage}%)")
                    elif winning_percentage < 60:
                        print(f"Este o mutare foarte buna. ({winning_percentage}%)")
                    else:
                        print(f"Aceasta mutare iti ofera sanse mari de castig. ({winning_percentage}%)")
                    stockfish.make_moves_from_current_position([best_move_uci])
                    board.push_san(best_move_uci)
                    print("Noua configuratie ", board.fen())
                    print("\nTabla dupa realizarea mutarii: ")
                    print(board)   
            else:
                    print("Configuratie invalida!")
 
 
def compute_winning_percentage(board, move):
    move_percentage = str(move)
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'K':
        move_percentage = 'K' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'Q':
        move_percentage = 'Q' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'N':
        move_percentage = 'N' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'B':
        move_percentage = 'B' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'R':
        move_percentage = 'R' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'k':
        move_percentage = 'K' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'q':
        move_percentage = 'Q' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'n':
        move_percentage = 'N' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'b':
        move_percentage = 'B' + move_percentage[2:]
    if board. piece_at(move.from_square) and board.piece_at(move.from_square).symbol() == 'r':
        move_percentage = 'R' + move_percentage[2:]
    if move.from_square == chess.E1 and move.to_square == chess.G1 and board.piece_at(move.from_square).symbol() == 'K':
        move_percentage = 'O-O'
    if move.from_square == chess.E1 and move.to_square == chess.C1 and board.piece_at(move.from_square).symbol() == 'K':
        move_percentage = 'O-O-O'
    if move.from_square == chess.E8 and move.to_square == chess.G8 and board.piece_at(move.from_square).symbol() == 'k':
        move_percentage = 'O-O'
    if move.from_square == chess.E8 and move.to_square == chess.C8 and board.piece_at(move.from_square).symbol() == 'k':
        move_percentage = 'O-O-O'
    move_apparitions_in_wins = 0
    move_apparitions = 0
    if board.turn:
        for game in white_wins:
            if move_percentage in game:
                move_apparitions_in_wins +=1
        for game in all_games_white:
            if move_percentage in game:
                move_apparitions +=1
        if move_apparitions == 0:
            return "Nedefinit"
        else:
            return round(move_apparitions_in_wins / move_apparitions * 100, 2)
    else:
        for game in black_wins:
            if move_percentage in game:
                move_apparitions_in_wins +=1
        for game in all_games_black:
            if move_percentage in game:
                move_apparitions +=1
        if move_apparitions == 0:
            return "Nedefinit"
        else:
            return round(move_apparitions_in_wins / move_apparitions * 100, 2)
 
 
 
def get_explanation(board, move):
 
    if board.is_checkmate():
        if board.turn:
            return " Este sah mat. Negrul a castigat partida!"
        else:
            return " Este sah mat. Albul a castigat partida!"
 
    if board.is_check():
        if board.turn:
            return " Este sah. Albul trebuie sa faca aceasta mutare pentru a se apara."
        else:
            return " Este sah. Negrul trebuie sa faca aceasta mutare pentru a se apara."
 
    if board.is_stalemate():
        return " Partida s-a incheiat la egalitate!"
 
    if board.is_fivefold_repetition():
        return " Partida s-a incheiat la egalitate!"
 
    if board.is_seventyfive_moves():
        return " Partida s-a incheiat la egalitate!"
 
    if board.is_insufficient_material():
        return " Partida s-a incheiat la egalitate!"
 
    response = verify_if_move_will_be_check_or_checkmate(board, move)
    if board.turn and response != None:
        if response == "Checkmate":
            return " Cu aceasta mutare, albul va produce sah mat."
        elif response == "Check":
            return " Cu aceasta mutare, albul va produce sah."
    else:
        if response == "Checkmate":
            return " Cu aceasta mutare, negrul va produce sah mat."
        elif response == "Check":
            return " Cu aceasta mutare, negrul va produce sah."
 
    if board.is_castling(move):
        if board.is_kingside_castling(move):
            return " Realizeaza o rocada de partea regelui, pozitionandu-l mai in siguranta."
        elif board.is_queenside_castling(move):
            return " Realizeaza o rocada de partea reginei, pozitionand regele mai in siguranta."
 
    if move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8] and board.piece_at(move.from_square).symbol() == 'P':
        return f" Promovezi un pion si poti obtine un cal, o tura, un nebun sau o regina. Acest lucru iti ofera un avantaj semnificativ."
  
    if move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1] and board.piece_at(move.from_square).symbol() == 'p':
        return f" Promovezi un pion si poti obtine un cal, o tura, un nebun sau o regina. Acest lucru iti ofera un avantaj semnificativ."
    
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        return get_explanation_of_captured_piece(captured_piece)
 
    if board.piece_at(move.from_square).symbol() == 'P':
        return get_explanation_white_pawn(board, move)
    elif board.piece_at(move.from_square).symbol() == 'p':
        return get_explanation_black_pawn(board, move)
    elif board.piece_at(move.from_square).symbol() == 'K':
        return get_explanation_white_king(board, move)
    elif board.piece_at(move.from_square).symbol() == 'k':
        return get_explanation_black_king(board, move)
    elif board.piece_at(move.from_square).symbol() == 'B':
        return get_explanation_white_bishop(board, move)
    elif board.piece_at(move.from_square).symbol() == 'b':
        return get_explanation_black_bishop(board, move)
    elif board.piece_at(move.from_square).symbol() == 'R':
        return get_explanation_white_rook(board, move)
    elif board.piece_at(move.from_square).symbol() == 'r':
        return get_explanation_black_rook(board, move)
    elif board.piece_at(move.from_square).symbol() == 'N':
        return get_explanation_white_knight(board, move)
    elif board.piece_at(move.from_square).symbol() == 'n':
        return get_explanation_black_knight(board, move)
    elif board.piece_at(move.from_square).symbol() == 'Q':
        return get_explanation_white_queen(board, move)
    elif board.piece_at(move.from_square).symbol() == 'q':
        return get_explanation_black_queen(board, move)
    else:
        return " Realizezi o mutare strategica care iti ofera control asupra centrului tablei si te pregateste pentru etapele urmatoare ale partidei."
 
 
def get_explanation_black_king(board, move):
    if move.from_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8, chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7, chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6] and move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8, chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]:
        return " Asigura o pozitie mai sigura regelui."
    return " Regele joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."    
 
def get_explanation_white_king(board, move):
    if move.from_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2, chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3] and move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
        return " A siguri o pozitie mai sigura regelui tau."
    return " Regele joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."
 
 
def get_explanation_black_pawn(board, move):
            if move.from_square in [chess.H7] and move.to_square in [chess.H5, chess.H6]:
                return " Ai sanse sa obtii un control mai amplu asupra zonei laterale a tablei."
            if move.from_square in [chess.G7] and move.to_square in [chess.G5, chess.G6]:
                if board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b':
                    return " Iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc. Totodata, aceasta mutare deschide calea pentru nebunul de pe f8."
                else:
                    return " Iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc."
            if move.from_square in [chess.F7] and move.to_square in [chess.F5, chess.F6]:
                return " Produci o presiune în centrul tablei și creezi opțiuni de atac sau dezvoltare agresivă."
            if move.from_square in [chess.E7] and move.to_square in [chess.E5, chess.E6]:
                if board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b' and board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
                    return " Iti extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege si pentru nebunul de pe f8."
                elif board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b':
                    return " Iti extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru nebunul de pe f8."
                elif board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
                    return " Iti extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege."
                else:
                    return " Iti extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale."
            if move.from_square in [chess.D7] and move.to_square in [chess.D5, chess.D6]:
                if board.piece_at(chess.E8) and board.piece_at(chess.E8).symbol() == 'q' and board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
                    return " Deschide calea pentru regină și nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                elif board.piece_at(chess.E8) and board.piece_at(chess.E8).symbol() == 'q':
                    return " Deschide calea pentru regină, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                elif board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
                    return " Deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                else:
                    return "Deschide calea pentru dezvoltarea pieselor tale, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
            if move.from_square in [chess.C7] and move.to_square in [chess.C5, chess.C6]:
                if board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'q':
                    return " Iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale. Totodata, aceasta mutare deschide calea pentru regina."
                else:
                    return " Iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale."
            if move.from_square in [chess.B7] and move.to_square in [chess.B5, chess.B6]:
                if board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b' and board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
                    return " Faci o introducere în deschiderea Indiană de rege, pregătind terenul pentru dezvoltarea rapidă a nebunului și a regelui în spatele pionului de pe b7."
                elif board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
                    return " Deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                else:
                    return " Contribuie la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
            if move.from_square in [chess.A7] and move.to_square in [chess.A5, chess.A6]:
                return " Descurajeaza dezvoltarea adversarului in zona laterala a tablei si pregateste oportunitati de atac pe flanc."
            return f" Avansezi strategic pionul si te pregatesti pentru mutarile ulterioare ale partidei. Poti incerca sa promovezi acest pion intr-o regina. Acest lucru iti va da un avantaj semnificativ."
 
 
def get_explanation_white_pawn(board, move):
            if move.from_square in [chess.A2] and move.to_square in [chess.A3, chess.A4]:
                return " Ai sanse sa obtii un control mai amplu asupra zonei laterale a tablei."
            if move.from_square in [chess.B2] and move.to_square in [chess.B3, chess.B4]:
                if board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B':
                    return " Iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc. Totodata, aceasta mutare deschide calea pentru nebunul de pe c1."
                else:
                    return " Iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc."
            if move.from_square in [chess.C2] and move.to_square in [chess.C3, chess.C4]:
                if board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q':
                    return " Iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale. Totodata, aceasta mutare deschide calea pentru regina."
                else:
                    return " Iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale."
            if move.from_square in [chess.D2] and move.to_square in [chess.D3, chess.D4]:
                if board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B' and board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
                    return " Iți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege si pentru nebunul de pe c1."
                elif board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B':
                    return " Iți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru nebunul de pe c1."
                elif board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
                    return " Iți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege."
                else:
                    return " Iti extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale."
            if move.from_square in [chess.E2] and move.to_square in [chess.E4, chess.E3]:
                if board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q' and board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
                    return "Deschide calea pentru regină și nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                elif board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q':
                    return "Deschide calea pentru regină, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                elif board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
                    return "Deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                else:
                    return "Deschide calea pentru dezvoltarea pieselor tale, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
            if move.from_square in [chess.F2] and move.to_square in [chess.F3, chess.F4]:
                return " Vei produce o presiune în centrul tablei și vei crea opțiuni de atac sau dezvoltare agresivă."
            if move.from_square in [chess.G2] and move.to_square in [chess.G3, chess.G4]:
                if board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B' and board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
                    return " Faci o introducere în deschiderea Indiană de rege, pregătind terenul pentru dezvoltarea rapidă a nebunului și a regelui în spatele pionului de pe g2."
                elif board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
                    return " Deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                else:
                    return " Contribuie la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
            if move.from_square in [chess.H2] and move.to_square in [chess.H3, chess.H4]:
                return " Descurajeaza dezvoltarea adversarului in zona laterala a tablei si pregateste oportunitati de atac pe flanc."
            return f" Avansezi strategic pionul si te pregatesti pentru mutarile ulterioare ale partidei. Poti incerca sa promovezi acest pion intr-o regina. Acest lucru iti va da un avantaj semnificativ."
 
 
def get_explanation_white_bishop(borad, move):
            if move.from_square in [chess.C1, chess.F1] and move.to_square in [chess.G5, chess.B5]:
                return " Aduci nebunul intr-o pozitie amenintatoare in zona adversarului, exercitand presiune asupra regelui negru."
            if move.from_square in [chess.C1, chess.F1] and move.to_square in [chess.B2, chess.A3, chess.G2, chess.H3]:
                return " Nebunul ofera o pozitie sigura pentru regele alb."
            if move.from_square in ALL_SQUARES and \
                move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                  chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                  chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
                return " Vei crea o amenintare directa asupra regelui negru. Pozitia poate fi exploatată pentru a provoca slăbiciuni în apărarea adversarului sau pentru a crea o oportunitate de atac."
            if move.from_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                                    chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3] and \
                move.to_square in [chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Nebunul trece intr-o pozitie mai ofensiva pentru a pune presiune asupra pieselor negre."
            if move.from_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2] and \
                move.to_square in [chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                                    chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3]:
                return " Nebunul este scos in fata pentru a pregati urmatoarea actiune strategica"
            if move.from_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                    chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5,
                                    chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                    chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8] and \
                move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
                return " Nebunul este dus in defensiva pentru a proteja celelalte piese."
            if move.from_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                    chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8] and \
                move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                    chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Consolidezi pozitia nebunului si poti sa pregatesti o actiune strategica, din mijlocul tablei."           
            return " Nebunul joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."
 
 
def get_explanation_black_bishop(board,move):
            if move.from_square in [chess.F8, chess.C8] and move.to_square in [chess.B4, chess.G4]:
                return " Aduci nebunul intr-o pozitie amenintatoare in zona adversarului, exercitand presiune asupra regelui alb."
            if move.from_square in [chess.F8, chess.C8] and move.to_square in [chess.G7, chess.H6, chess.B7, chess.A6]:
                return " Nebunul ofera o pozitie sigura pentru regele negru."
            if move.from_square in ALL_SQUARES and \
                move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                  chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                  chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Vei crea o amenintare directa asupra regelui alb. Poziția poate fi exploatată pentru a provoca slăbiciuni în apărarea adversarului sau pentru a crea o oportunitate de atac."
            if move.from_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                    chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6] and \
                move.to_square in [chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Nebunul trece intr-o pozitie mai ofensiva pentru a pune presiune asupra pieselor albe."
            if move.from_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7] and \
                move.to_square in [chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                    chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6]:
                return " Nebunul este scos in fata pentru a pregati urmatoarea actine strategica" 
            if move.from_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                    chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5,
                                    chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                                    chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1] and \
                move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]:
                return " Nebunul este dus in defensiva pentru a proteja celelalte piese."
            if move.from_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                                    chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1] and \
                move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                    chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Consolidezi pozitia nebunului si poti sa pregatesti o actiune strategica, din mijlocul tablei."           
            return " Nebunul joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."
 
 
def get_explanation_white_rook(borad,move):
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5,
                           chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                          chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                          chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
        return " Pregateste jocul pentru urmatoarele mutari strategice. Turnul este o piesa esentiala in crearea amenintarilor asupra regelui advers."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                           chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4]:
        return " Ajuta la formarea unei influente mai mari asupra pozitiei globale a tablei"
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                            chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
        return " Mutarea turnului ajuta la o mai buna protectie a pieselor albe  ."
    return " Turnul ajuta la un control mai bun al tablei de joc."
 
 
def get_explanation_black_rook(board,move):
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                           chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                          chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                          chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]:
        return " Pregateste jocul pentru urmatoarele mutari strategice. Turnul este o piesa esentiala in crearea de amenintati asupra regelui advers."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                           chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
        return " Ajuta la formarea unei influente mai mari asupra pozitiei globale a tablei"
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                            chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]:
        return " Ajuta la o mai buna protectie a pieselor negre."
    return " Turnul ajuta la un control mai bun al tablei de joc."
 
 
def get_explanation_white_knight(board, move):
    if move.from_square in [chess.B1, chess.G1] and move.to_square in [chess.C3, chess.F3]:
        return " Calul este scos in fata pentru a pregati urmatoarele actiuni strategice."
    if move.from_square in [chess.C3, chess.F3] and move.to_square in [chess.D5, chess.E5]:
        return " Calul controleaza un câmp central cheie și ameninta pionii negri."
    if move.from_square in [chess.B1, chess.G1] and move.to_square in [chess.A3, chess.H3]:
        return " Calul este pregatit pentru un atac pe flanc."
    if move.from_square in [chess.C3, chess.F3] and move.to_square in [chess.E4, chess.D4, chess.D5, chess.E5]:
        return " Ccalul ocupa o pozitie ofensiva si obtine un control mai bun asupra centrului tablei."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A4, chess.B4, chess.G4, chess.H4,
                           chess.A5, chess.B5, chess.G5, chess.H5,
                           chess.A6, chess.B6, chess.G6, chess.H6]:
        return " Pregateste calul pentru o actiune strategica pe flanc."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                           chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                           chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]:
        return " Calul joaca defensiv si protejeaza piesele albe."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                            chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
        return " Mutarea calului este una ofensiva si pune presiune asupra pieselor negre."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.C4, chess.D4, chess.E4, chess.F4,
                            chess.C5, chess.D5, chess.E5, chess.F5,
                            chess.C6, chess.D6, chess.E6, chess.F6]:
        return " Calul obtine control asupra centrului tablei."
 
    return " Pregateste jocul pentru urmatoarele mutari strategice. Calul este o piesa esentiala in crearea de amenintari asupra regelui advers."
 
 
def get_explanation_black_knight(board, move):
    if move.from_square in [chess.B8, chess.G8] and move.to_square in [chess.C6, chess.F6]:
        return " Calul este scos in fata pentru a pregati urmatoarele actiuni strategice."
    if move.from_square in [chess.C6, chess.F6] and move.to_square in [chess.D4, chess.E4]:
        return " Calul controleaza un câmp central cheie și amenințând pionii albi."
    if move.from_square in [chess.G8, chess.B8] and move.to_square in [chess.H6, chess.A6]:
        return " Calul este pregatit pentru un atac pe flanc."
    if move.from_square in [chess.F6, chess.C6] and move.to_square in [chess.D5, chess.E5, chess.E4, chess.D4]:
        return " Calul ocupa o pozitie ofensiva si obtine un control mai bun asupra centrului tablei." 
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A5, chess.B5, chess.G5, chess.H5,
                           chess.A4, chess.B4, chess.G4, chess.H4,
                           chess.A3, chess.B3, chess.G3, chess.H3]:
        return "Pregateste calul pentru o actiune strategica pe flanc."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                           chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                           chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
        return " Calul joaca defensiv si protejeaza piesele negre."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                            chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]:
        return " Mutarea calului este una ofensiva si pune presiune asupra pieselor albe."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.C5, chess.D5, chess.E5, chess.F5,
                            chess.C4, chess.D4, chess.E4, chess.F4,
                            chess.C3, chess.D3, chess.E3, chess.F3]:
        return " Calul obtine control asupra centrului tablei."
    return " Pregateste jocul pentru urmatoarele mutari strategice. Calul este o piesa esentiala in crearea de amenintari asupra regelui advers."
 
 
def get_explanation_white_queen(board, move):
    if move.from_square in [chess.D1] and move.to_square in [chess.F3] and board.piece_at(chess.C1) == 'B':
        return " Regina va coopera mai bine cu nebunul de pe c1."
    if move.from_square in [chess.D1] and move.to_square in [chess.D4, chess.E4, chess.D5, chess.E5]:
        return " Regina este plasata in centrul tablei controland patru patrate importante si avand o influenta semnificativa asupra centrului tablei."
    if move.from_square in [chess.D1] and move.to_square in [chess.E2]:
        return " Pregateste regina pentru oportunitati viitoare de atac."
    if move.from_square in [chess.D1] and move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                                                          chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
        return " Regina este scoasa in fata pentru a pregati urmatoarele actiuni strategice."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                            chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
        return " Regina joaca defensiv si protejeaza piesele albe."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                            chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                            chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
        return " Regina este plasata in centrul tablei pentru a incerca sa captureze piese negre."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                            chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                            chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
        return " Regina este mutata intr-o pozitie ofensiva punand presiune pe regele advers, incercat sa produca un sah mat."
    return " Pregateste jocul pentru urmatoarele mutari strategice. Calul este o piesa esentiala in crearea de amenintari asupra regelui advers."
 
 
def get_explanation_black_queen(board, move):
    if move.from_square in [chess.D8] and move.to_square in [chess.F6] and board.piece_at(chess.C8) == 'b':
        return " Regina va coopera mai bine cu nebunul de pe c8."
    if move.from_square in [chess.D8] and move.to_square in [chess.D4, chess.E4, chess.D5, chess.E5]:
        return " Regina este plasata in centrul tablei controland patru patrate importante si avand o influenta mai semnificativa asupra centrului tablei."
    if move.from_square in [chess.D8] and move.to_square in [chess.E7]:
        return " Pregateste regina pentru oportunitati viitoare de atac."
    if move.from_square in [chess.D8] and move.to_square in [chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                                          chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
        return " Regina este scoasa in fata pentru a pregati urmatoarele actiuni strategice."   
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                            chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
        return " Regina joaca defensiv si protejeaza piesele albe."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                            chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                            chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
        return " Regina este plasata in centrul tablei pentru a incerca sa captureze piese albe."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                            chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                            chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]:
        return " Regina este mutata intr-o pozitie ofensiva punand presiune pe regele advers, incercat sa produca un sah mat."
    return " Pregateste jocul pentru urmatoarele mutari strategice. Calul este o piesa esentiala in crearea de amenintari asupra regelui advers."
 
 
def verify_if_move_will_be_check_or_checkmate(board,move):
    board.push(move)
    if board.is_checkmate():
        board.pop()
        return "Checkmate"
    elif board.is_check():
        board.pop()
        return "Check"
    else:
        board.pop()
        return None
 
def get_explanation_of_captured_piece(captured_piece):
    if captured_piece.symbol() == 'P':
        return "Capturezi pionul, care este o piesa importanta in jocul de sah. Pionul poate fi promovat in orice alta piesa, cu exceptia regelui."
    if captured_piece.symbol() == 'N':
        return "Capturezi calul, care este o piesa importanta in jocul de sah. Calul poate sari peste alte piese si poate fi folosit pentru a ataca regina adversarului."
    if captured_piece.symbol() == 'B':
        return "Capturezi nebunul, care este o piesa importanta in jocul de sah. Nebunul poate fi folosit pentru a ataca regina adversarului."
    if captured_piece.symbol() == 'R':
        return "Capturezi turnul, care este o piesa importanta in jocul de sah. Turnul poate fi folosit pentru a ataca regina adversarului."
    if captured_piece.symbol() == 'Q':
        return "Capturezi regina, care este cea mai importanta piesa din joc. Regina poate fi folosita pentru a ataca regina adversarului."
    if captured_piece.symbol() == 'p':
        return "Capturezi pionul, care este o piesa importanta in jocul de sah. Pionul poate fi promovat in orice alta piesa, cu exceptia regelui."
    if captured_piece.symbol() == 'n':
        return "Capturezi calul, care este o piesa importanta in jocul de sah. Calul poate sari peste alte piese si poate fi folosit pentru a ataca regina adversarului."
    if captured_piece.symbol() == 'b':
        return "Capturezi nebunul, care este o piesa importanta in jocul de sah. Nebunul poate fi folosit pentru a ataca regina adversarului."
    if captured_piece.symbol() == 'r':
        return "Capturezi turnul, care este o piesa importanta in jocul de sah. Turnul poate fi folosit pentru a ataca regina adversarului."
    if captured_piece.symbol() == 'q':
        return "Capturezi regina, care este cea mai importanta piesa din joc. Regina poate fi folosita pentru a ataca regina adversarului."
    return " Capturezi o piesa a adversarului."
 
if __name__ == "__main__":
    chatbot = ChatBot("Chatpot")
    stockfish = Stockfish(path="C:\stockfish\stockfish-windows-x86-64-avx2.exe")
    train()
    parser()
 
    # board = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPP3P/RNBQKBNR b KQkq - 0 1")
    # print(board.is_checkmate())
    # move = chess.Move.from_uci("d8h4")
    # explanation = get_explanation(board, move)
    # print(explanation)
    # print(board)
    # board.push(move)
    # print(board.fen())
    # print(compute_winning_percentage(board,move))
    main()
    # print(white_wins)
    # print(black_wins)




# DEMO:

# Ce inseamna promovarea pionului?

# Ce se muta regele?

# Cum se muta regina?

# Cum se muta nebunul?

# Cum se muta pionul?

# Ce inseamna rocada?

# Cum sunt identificate patratelele?

# In ce consta regula mutarii pieselor?

# Cine muta primul in jocul de sah?

# Explica ce este en passant.

# Care este diferenta dintre sah si sah mat?
    

# https://www.dailychess.com/chess/chess-fen-viewer.php
# Configuratii: 
# default: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
# 
# promovare: r3kbnr/pP2pppp/8/8/8/8/P1PPPPPP/RNBQKBNR w KQkq - 0 1
# b7b8
# produc sah: rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPP3P/RNBQKBNR b KQkq - 0 1
# d8d4
# produc sah mat: rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPPP2P/RNBQKBNR b KQkq - 0 1
# d8h4