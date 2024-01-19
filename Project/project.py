import chess
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from stockfish import Stockfish

ALL_SQUARES = [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
               chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
               chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5,
                chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]
               
def train():

    trainer = ListTrainer(chatbot)
    trainer.train([
        "Hi",
        "Welcome, friend 🤗",
    ])


    with open("training.yml", "r") as file:
        line1 = file.readline().strip()
        line2 = file.readline().strip()
        while line1 and line2:         
            trainer.train([line2, line1,])
            line1 = file.readline().strip()
            line2 = file.readline().strip()



def main():
    print("\n\nWelcome friend 🤗!")
    while True:
        print("How can i help you? (Enter the number)")
        print("1. Show the best move. (fen configuration)")
        print("2. I have a question about the rules.")
        print("3. Exit.")
        choice = input("Your choice: ")

        if choice == "1":
            best_move_fen_configuration()
        elif choice == "2":
            rules_question()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


def rules_question():
    exit_conditions = (":q", "quit", "exit")
    print("🪴 How can I help you?")
    while True:
        user_input = input("> ")
        if user_input in exit_conditions:
            break
        print(f"🪴 {chatbot.get_response(user_input)}")
    # TO DO: Train the chatbot with all the questions about the rules of chess

def best_move_fen_configuration():
    user_input = input("Enter the FEN configuration: ")
    board = chess.Board(user_input)
    stockfish.set_fen_position(user_input)
    for i in range(40):
        #board = chess.Board(user_input)
        if stockfish.is_fen_valid(user_input):
            #stockfish.set_fen_position(user_input)
            best_move_uci = stockfish.get_best_move()
            best_move = chess.Move.from_uci(best_move_uci)
            explanation = get_explanation(board, best_move)
            print("\n\nBest move: ", best_move)
            best_move = chess.Move.from_uci(best_move_uci)
            print("Explanation: ", explanation)
            # make the best move on the board
            # actualize the board with the new move
            stockfish.make_moves_from_current_position([best_move_uci])
            board.push_san(best_move_uci)
            print(board)
            
        else:
            print("Invalid FEN configuration!")
    

def get_explanation(board, move):
    
    if board.is_checkmate():
        return " Esti in sah mat. Ai pierdut partida!"

    if board.is_check():
        print (" Esti in sah. Trebuie sa faci aceasta mutare pentru a te apara.")

    if board.is_stalemate():
        return " Este pat. Partida s-a remizat!"
    
    # check if the move is en passant
    if board.is_en_passant(move):
        return "Ai capturat un pion en passant, eliminand o amenintare asupra pozitiei tale."
    
    
    if board.is_castling(move):
        if board.is_kingside_castling(move):
            return "Ai realizat o rocada de partea regelui, pozitionand regele intr-o pozitie mai sigura."
        elif board.is_queenside_castling(move):
            return "Ai realizat o rocada de partea reginei, pozitionand regele intr-o pozitie mai sigura."

    if move.promotion:
        promoted_piece = chess.piece_name(move.promotion).lower()
        # TO DO: VARIATII ALE PROPOZITIEI IN FUNCTIE DE PIESA PROMOVATA
        return f"Ai promovat un pion și ai obținut o nouă {promoted_piece}, ceea ce îți oferă un avantaj semnificativ."
    
    if board.is_capture(move):
        captured_piece = board.piece_at(move.from_square)
        # TO DO: VARIATII ALE PROPOZITIEI IN FUNCTIE DE PIESA CAPTURATA
        if captured_piece:
            return f"Ai capturat o {captured_piece.symbol()} și ai eliminat o amenințare asupra poziției tale."
        else:
            return "Ai eliminat o amenințare asupra poziției tale."

    if board.is_stalemate():
        return " Această mutare determină pat. Ai remizat partida!"
    

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
    
    return "Ai realizat o mutare strategică care îți oferă control asupra centrului tablei și te pregătește pentru etapele ulterioare ale partidei."


def get_explanation_black_king(board, move):
    if move.from_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8, chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7, chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6] and move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8, chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]:
        return "Prin aceasta mutare asiguri o pozitie mai sigura regelui tau."
    return " Prin aceasta mutare, regele joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."    


def get_explanation_white_king(board, move):
    if move.from_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2, chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3] and move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
        return "Prin aceasta mutare asiguri o pozitie mai sigura regelui tau."
    return " Prin aceasta mutare, regele joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."


def get_explanation_black_pawn(board, move):
            if move.from_square in [chess.H7] and move.to_square in [chess.H5, chess.H6]:
                return " Prin aceasta mutare, ai sanse sa obtii un control mai amplu asupra zonei laterale a tablei."
            if move.from_square in [chess.G7] and move.to_square in [chess.G5, chess.G6]:
                if board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b':
                    return " Prin aceasta mutare, iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc. Totodata, aceasta mutare deschide calea pentru nebunul de pe f8."
                else:
                    return " Prin aceasta mutare, iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc."
            if move.from_square in [chess.F7] and move.to_square in [chess.F5, chess.F6]:
                if board.piece_at(chess.E8) and board.piece_at(chess.E8).symbol() == 'q':
                    return " Prin aceasta mutare, iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale. Totodata, aceasta mutare deschide calea pentru regina de pe e8."
                else:
                    return " Prin aceasta mutare, iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale."
            if move.from_square in [chess.E7] and move.to_square in [chess.E5, chess.E6]:
                if board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b' and board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
                    return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege si pentru nebunul de pe f8."
                elif board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b':
                    return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru nebunul de pe f8."
                elif board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
                    return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege."
                else:
                    return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale."
            if move.from_square in [chess.D7] and move.to_square in [chess.D5, chess.D6]:
                if board.piece_at(chess.E8) and board.piece_at(chess.E8).symbol() == 'q' and board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
                    return "Această mutare deschide calea pentru regină și nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                elif board.piece_at(chess.E8) and board.piece_at(chess.E8).symbol() == 'q':
                    return "Această mutare deschide calea pentru regină, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                elif board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
                    return "Această mutare deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                else:
                    return "Această mutare deschide calea pentru dezvoltarea pieselor tale, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
            if move.from_square in [chess.C7] and move.to_square in [chess.C5, chess.C6]:
                return " Prin aceasta mutare, vei produce o presiune în centrul tablei și vei crea opțiuni de atac sau dezvoltare agresivă."
            if move.from_square in [chess.B7] and move.to_square in [chess.B5, chess.B6]:
                if board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b' and board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
                    return " Această mutare este o introducere în deschiderea Indiană de rege, pregătind terenul pentru dezvoltarea rapidă a nebunului și a regelui în spatele pionului de pe b7."
                elif board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
                    return " Această mutare deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                else:
                    return " Aceasta mutare contribuie la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
            if move.from_square in [chess.A7] and move.to_square in [chess.A5, chess.A6]:
                return "Aceasta mutare descurajeaza dezvoltarea adversarului in zona laterala a tablei si pregateste oportunitati de atac pe flanc."
            return f" Prin aceasta mutare avansezi strategic pionul si te pregatesti pentru mutarile ulterioare ale partidei. Poti incerca sa promovezi acest pion intr-o regina. Acest lucru iti va da un avantaj semnificativ."
       

def get_explanation_white_pawn(board, move):
            if move.from_square in [chess.A2] and move.to_square in [chess.A3, chess.A4]:
                return " Prin aceasta mutare, ai sanse sa obtii un control mai amplu asupra zonei laterale a tablei."
            if move.from_square in [chess.B2] and move.to_square in [chess.B3, chess.B4]:
                if board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B':
                    return " Prin aceasta mutare, iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc. Totodata, aceasta mutare deschide calea pentru nebunul de pe c1."
                else:
                    return " Prin aceasta mutare, iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc."
            if move.from_square in [chess.C2] and move.to_square in [chess.C3, chess.C4]:
                if board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q':
                    return " Prin aceasta mutare, iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale. Totodata, aceasta mutare deschide calea pentru regina de pe d1."
                else:
                    return " Prin aceasta mutare, iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale."
            if move.from_square in [chess.D2] and move.to_square in [chess.D3, chess.D4]:
                if board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B' and board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
                    return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege si pentru nebunul de pe c1."
                elif board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B':
                    return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru nebunul de pe c1."
                elif board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
                    return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege."
                else:
                    return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale."
            if move.from_square in [chess.E2] and move.to_square in [chess.E4, chess.E3]:
                if board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q' and board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
                    return "Această mutare deschide calea pentru regină și nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                elif board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q':
                    return "Această mutare deschide calea pentru regină, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                elif board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
                    return "Această mutare deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                else:
                    return "Această mutare deschide calea pentru dezvoltarea pieselor tale, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
            if move.from_square in [chess.F2] and move.to_square in [chess.F3, chess.F4]:
                return " Prin aceasta mutare, vei produce o presiune în centrul tablei și vei crea opțiuni de atac sau dezvoltare agresivă."
            if move.from_square in [chess.G2] and move.to_square in [chess.G3, chess.G4]:
                if board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B' and board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
                    return " Această mutare este o introducere în deschiderea Indiană de rege, pregătind terenul pentru dezvoltarea rapidă a nebunului și a regelui în spatele pionului de pe g2."
                elif board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
                    return " Această mutare deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
                else:
                    return " Aceasta mutare contribuie la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
            if move.from_square in [chess.H2] and move.to_square in [chess.H3, chess.H4]:
                return "Aceasta mutare descurajeaza dezvoltarea adversarului in zona laterala a tablei si pregateste oportunitati de atac pe flanc."
            return f" Prin aceasta mutare avansezi strategic pionul si te pregatesti pentru mutarile ulterioare ale partidei. Poti incerca sa promovezi acest pion intr-o regina. Acest lucru iti va da un avantaj semnificativ."
        
def get_explanation_white_bishop(borad, move):
            if move.from_square in [chess.C1, chess.F1] and move.to_square in [chess.G5, chess.B5]:
                return " Prin aceasta mutare aduci nebunul intr-o pozitie amenintatoare in zona adversarului, exercitand presiune asupra regelui negru."
            if move.from_square in [chess.C1, chess.F1] and move.to_square in [chess.B2, chess.A3, chess.G2, chess.H3]:
                return "Prin aceasta mutare, nebunul ofera o pozitie sigura pentru regele alb."
            if move.from_square in ALL_SQUARES and \
                move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                  chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                  chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
                return " Prin mutarea aceasta vei crea o amenintare directa asupra regelui negru. poziție poate fi exploatată pentru a provoca slăbiciuni în apărarea adversarului sau pentru a crea o oportunitate de atac."
            if move.from_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                                    chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3] and \
                move.to_square in [chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Prin aceasta mutare, nebunul trece intr-o pozitie mai ofensiva pentru a pune presiune asupra pieselor negre."
            if move.from_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2] and \
                move.to_square in [chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                                    chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3]:
                return " Prin aceasta mutare, nebunul este scos in fata pentru a pregati urmatoarea actine strategica"
            if move.from_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                    chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5,
                                    chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                    chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8] and \
                move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
                return " Prin aceasta mutare, nebunul este dus in defensiva pentru a proteja celelalte piese."
            if move.from_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                    chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8] and \
                move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                    chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Prin aceasta mutare, consolidezi pozitia nebunului si poti sa pregatesti o actiune strategica, din mijlocul tablei."           
            return " Prin aceasta mutare, nebunul joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."


def get_explanation_black_bishop(board,move):
            if move.from_square in [chess.F8, chess.C8] and move.to_square in [chess.B4, chess.G4]:
                return " Prin aceasta mutare aduci nebunul intr-o pozitie amenintatoare in zona adversarului, exercitand presiune asupra regelui alb."
            if move.from_square in [chess.F8, chess.C8] and move.to_square in [chess.G7, chess.H6, chess.B7, chess.A6]:
                return "Prin aceasta mutare, nebunul ofera o pozitie sigura pentru regele negru."
            if move.from_square in ALL_SQUARES and \
                move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                  chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                  chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Prin mutarea aceasta vei crea o amenintare directa asupra regelui alb. Poziția poate fi exploatată pentru a provoca slăbiciuni în apărarea adversarului sau pentru a crea o oportunitate de atac."
            if move.from_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                    chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6] and \
                move.to_square in [chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Prin aceasta mutare, nebunul trece intr-o pozitie mai ofensiva pentru a pune presiune asupra pieselor albe."
            if move.from_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7] and \
                move.to_square in [chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                                    chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6]:
                return " Prin aceasta mutare, nebunul este scos in fata pentru a pregati urmatoarea actine strategica" 
            if move.from_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                    chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5,
                                    chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                                    chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1] and \
                move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                                    chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]:
                return " Prin aceasta mutare, nebunul este dus in defensiva pentru a proteja celelalte piese."
            if move.from_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                                    chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                                    chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1] and \
                move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                                    chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                                    chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
                return " Prin aceasta mutare, consolidezi pozitia nebunului si poti sa pregatesti o actiune strategica, din mijlocul tablei."           
            return " Prin aceasta mutare, nebunul joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."
            

def get_explanation_white_rook(borad,move):
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5,
                           chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                          chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                          chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
        return " Aceasta mutare pregateste jocul pentru urmatoarele mutari strategice. Turnul este o piesa esentiala in crearea amenintarilor asupra regelui advers."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                           chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4]:
        return " Aceasta mutare ajuta la formarea unei influente mai mari asupra pozitiei globale a tablei"
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                            chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
        return " Aceasta mutare a turnului ajuta la o mai buna protectie a pieselor albe  ."
    return " Prin aceasta mutare, turnul ajuta la un control mai bun al tablei de joc."

def get_explanation_black_rook(board,move):
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4,
                           chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                          chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                          chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]:
        return " Aceasta mutare pregateste jocul pentru urmatoarele mutari strategice. Turnul este o piesa esentiala in crearea de amenintati asupra regelui advers."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                           chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5]:
        return " Aceasta mutare ajuta la formarea unei influente mai mari asupra pozitiei globale a tablei"
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                            chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]:
        return " Aceasta mutare a turnului ajuta la o mai buna protectie a pieselor negre."
    return " Prin aceasta mutare, turnul ajuta la un control mai bun al tablei de joc."


def get_explanation_white_knight(board, move):
    if move.from_square in [chess.B1, chess.G1] and move.to_square in [chess.C3, chess.F3]:
        return " Prin aceasta mutare, calul este scos in fata pentru a pregati urmatoarele actini strategice."
    if move.from_square in [chess.C3, chess.F3] and move.to_square in [chess.D5, chess.E5]:
        return " Prin aceasta mutare, calul controleaza un câmp central cheie și amenințând pionii negri."
    if move.from_square in [chess.B1, chess.G1] and move.to_square in [chess.A3, chess.H3]:
        return " Prin aceasta mutare, calul este pregatit pentru un atac pe flanc."
    if move.from_square in [chess.C3, chess.F3] and move.to_square in [chess.E4, chess.D4, chess.D5, chess.E5]:
        return " Prin aceasta mutare, calul ocupa o pozitie ofensiva si obtine un control mai bun asupra centrului tablei."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A4, chess.B4, chess.G4, chess.H4,
                           chess.A5, chess.B5, chess.G5, chess.H5,
                           chess.A6, chess.B6, chess.G6, chess.H6]:
        return "Aceata mutare pregateste calul pentru o actiune strategica pe flanc."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3,
                           chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                           chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]:
        return " Prin aceasta mutare, calul joaca defensiv si protejeaza piesele albe."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                            chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
        return " Aceasta mutare a calului este una ofensiva si pune presiune asupra pieselor negre."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.C4, chess.D4, chess.E4, chess.F4,
                            chess.C5, chess.D5, chess.E5, chess.F5,
                            chess.C6, chess.D6, chess.E6, chess.F6]:
        return " Prin aceasta mutare, calul obtine control asupra centrului tablei."
    
    return " Aceasta mutare pregateste jocul pentru urmatoarele mutari strategice. Calul este o piesa esentiala in crearea de amenintari asupra regelui advers."


def get_explanation_black_knight(board, move):
    if move.from_square in [chess.B8, chess.G8] and move.to_square in [chess.C6, chess.F6]:
        return " Prin aceasta mutare, calul este scos in fata pentru a pregati urmatoarele actini strategice."
    if move.from_square in [chess.C6, chess.F6] and move.to_square in [chess.D4, chess.E4]:
        return " Prin aceasta mutare, calul controleaza un câmp central cheie și amenințând pionii albi."
    if move.from_square in [chess.G8, chess.B8] and move.to_square in [chess.H6, chess.A6]:
        return " Prin aceasta mutare, calul este pregatit pentru un atac pe flanc."
    if move.from_square in [chess.F6, chess.C6] and move.to_square in [chess.D5, chess.E5, chess.E4, chess.D4]:
        return " Prin aceasta mutare, calul ocupa o pozitie ofensiva si obtine un control mai bun asupra centrului tablei." 
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A5, chess.B5, chess.G5, chess.H5,
                           chess.A4, chess.B4, chess.G4, chess.H4,
                           chess.A3, chess.B3, chess.G3, chess.H3]:
        return "Aceata mutare pregateste calul pentru o actiune strategica pe flanc."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6,
                           chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7,
                           chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]:
        return " Prin aceasta mutare, calul joaca defensiv si protejeaza piesele negre."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                            chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]:
        return " Aceasta mutare a calului este una ofensiva si pune presiune asupra pieselor albe."
    if move.from_square in ALL_SQUARES and \
        move.to_square in [chess.C5, chess.D5, chess.E5, chess.F5,
                            chess.C4, chess.D4, chess.E4, chess.F4,
                            chess.C3, chess.D3, chess.E3, chess.F3]:
        return " Prin aceasta mutare, calul obtine control asupra centrului tablei."
    return " Aceasta mutare pregateste jocul pentru urmatoarele mutari strategice. Calul este o piesa esentiala in crearea de amenintari asupra regelui advers."




if __name__ == "__main__":
    chatbot = ChatBot("Chatpot")
    stockfish = Stockfish(path="C:\stockfish\stockfish-windows-x86-64-avx2.exe")
    #train()
    #board = chess.Board("rnbqkbnr/p1p1pppp/3p4/1p4B1/3P4/8/PPP1PPPP/RN1QKBNR w KQkq - 0 1")
    #move = chess.Move.from_uci("g5d2")  # Mutarea de testat
    #explanation = get_explanation(board, move)
    #print(explanation)
    main()










    # def get_explanation(board, move):

#     if board.is_checkmate():
#         return " Esti in sah mat. Ai pierdut partida!"

#     if board.is_check():
#         print (" Esti in sah. Trebuie sa faci aceasta mutare pentru a te apara.")

#     if board.is_stalemate():
#         return " Este pat. Partida s-a remizat!"
    
#     # check if the move is en passant
#     if board.is_en_passant(move):
#         return "Ai capturat un pion en passant, eliminand o amenintare asupra pozitiei tale."
    
    
#     if board.is_castling(move):
#         if board.is_kingside_castling(move):
#             return "Ai realizat o rocada de partea regelui, pozitionand regele intr-o pozitie mai sigura."
#         elif board.is_queenside_castling(move):
#             return "Ai realizat o rocada de partea reginei, pozitionand regele intr-o pozitie mai sigura."

#     if move.promotion:
#         promoted_piece = chess.piece_name(move.promotion).lower()
#         # TO DO: VARIATII ALE PROPOZITIEI IN FUNCTIE DE PIESA PROMOVATA
#         return f"Ai promovat un pion și ai obținut o nouă {promoted_piece}, ceea ce îți oferă un avantaj semnificativ."
    
#     if board.is_capture(move):
#         captured_piece = board.piece_at(move.from_square)
#         # TO DO: VARIATII ALE PROPOZITIEI IN FUNCTIE DE PIESA CAPTURATA
#         if captured_piece:
#             return f"Ai capturat o {captured_piece.symbol()} și ai eliminat o amenințare asupra poziției tale."
#         else:
#             return "Ai eliminat o amenințare asupra poziției tale."

#     if board.is_stalemate():
#         return " Această mutare determină pat. Ai remizat partida!"
    
#     if board.turn == chess.WHITE:
#         # check if the move is a pawn move
#         if board.piece_at(move.from_square).symbol() == 'P':
#             if move.from_square in [chess.A2] and move.to_square in [chess.A3, chess.A4]:
#                 return " Prin aceasta mutare, ai sanse sa obtii un control mai amplu asupra zonei laterale a tablei."
#             if move.from_square in [chess.B2] and move.to_square in [chess.B3, chess.B4]:
#                 if board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B':
#                     return " Prin aceasta mutare, iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc. Totodata, aceasta mutare deschide calea pentru nebunul de pe c1."
#                 else:
#                     return " Prin aceasta mutare, iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc."
#             if move.from_square in [chess.C2] and move.to_square in [chess.C3, chess.C4]:
#                 if board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q':
#                     return " Prin aceasta mutare, iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale. Totodata, aceasta mutare deschide calea pentru regina de pe d1."
#                 else:
#                     return " Prin aceasta mutare, iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale."
#             if move.from_square in [chess.D2] and move.to_square in [chess.D3, chess.D4]:
#                 if board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B' and board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
#                     return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege si pentru nebunul de pe c1."
#                 elif board.piece_at(chess.C1) and board.piece_at(chess.C1).symbol() == 'B':
#                     return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru nebunul de pe c1."
#                 elif board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
#                     return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege."
#                 else:
#                     return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale."
#             if move.from_square in [chess.E2] and move.to_square in [chess.E4, chess.E3]:
#                 if board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q' and board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
#                     return "Această mutare deschide calea pentru regină și nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#                 elif board.piece_at(chess.D1) and board.piece_at(chess.D1).symbol() == 'Q':
#                     return "Această mutare deschide calea pentru regină, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#                 elif board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
#                     return "Această mutare deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#                 else:
#                     return "Această mutare deschide calea pentru dezvoltarea pieselor tale, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#             if move.from_square in [chess.F2] and move.to_square in [chess.F3, chess.F4]:
#                 return " Prin aceasta mutare, vei produce o presiune în centrul tablei și vei crea opțiuni de atac sau dezvoltare agresivă."
#             if move.from_square in [chess.G2] and move.to_square in [chess.G3, chess.G4]:
#                 if board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B' and board.piece_at(chess.E1) and board.piece_at(chess.E1).symbol() == 'K':
#                     return " Această mutare este o introducere în deschiderea Indiană de rege, pregătind terenul pentru dezvoltarea rapidă a nebunului și a regelui în spatele pionului de pe g2."
#                 elif board.piece_at(chess.F1) and board.piece_at(chess.F1).symbol() == 'B':
#                     return " Această mutare deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#                 else:
#                     return " Aceasta mutare contribuie la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#             if move.from_square in [chess.H2] and move.to_square in [chess.H3, chess.H4]:
#                 return "Aceasta mutare descurajeaza dezvoltarea adversarului in zona laterala a tablei si pregateste oportunitati de atac pe flanc."
            
#             return f" Prin aceasta mutare avansezi strategic pionul si te pregatesti pentru mutarile ulterioare ale partidei. Poti incerca sa promovezi acest pion intr-o regina. Acest lucru iti va da un avantaj semnificativ."
        
#         if board.piece_at(move.from_square).symbol() == 'K':
#             if move.from_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2, chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3] and move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
#                 return "Prin aceasta mutare asiguri o pozitie mai sigura regelui tau."
#             return " Prin aceasta mutare, regele joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."
        
#         return "Ai realizat o mutare strategică care îți oferă control asupra centrului tablei și te pregătește pentru etapele ulterioare ale partidei."
#     else:
#         if board.piece_at(move.from_square).symbol() == 'p': 
#             if move.from_square in [chess.H7] and move.to_square in [chess.H5, chess.H6]:
#                 return " Prin aceasta mutare, ai sanse sa obtii un control mai amplu asupra zonei laterale a tablei."
#             if move.from_square in [chess.G7] and move.to_square in [chess.G5, chess.G6]:
#                 if board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b':
#                     return " Prin aceasta mutare, iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc. Totodata, aceasta mutare deschide calea pentru nebunul de pe f8."
#                 else:
#                     return " Prin aceasta mutare, iti consolidezi pozitia in centru si pregatesti oportunitati de atac pe flanc."
#             if move.from_square in [chess.F7] and move.to_square in [chess.F5, chess.F6]:
#                 if board.piece_at(chess.E8) and board.piece_at(chess.E8).symbol() == 'q':
#                     return " Prin aceasta mutare, iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale. Totodata, aceasta mutare deschide calea pentru regina de pe e8."
#                 else:
#                     return " Prin aceasta mutare, iti extinzi influența în centrul tablei și pregătești calea pentru o dezvoltare flexibilă a pieselor tale."
#             if move.from_square in [chess.E7] and move.to_square in [chess.E5, chess.E6]:
#                 if board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b' and board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
#                     return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege si pentru nebunul de pe f8."
#                 elif board.piece_at(chess.F8) and board.piece_at(chess.F8).symbol() == 'b':
#                     return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru nebunul de pe f8."
#                 elif board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
#                     return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale. Totodata, aceasta mutare deschide calea pentru rege."
#                 else:
#                     return " Prin această mutare îți extinzi influența în centrul tablei și creezi un suport puternic pentru dezvoltarea pieselor tale."
#             if move.from_square in [chess.D7] and move.to_square in [chess.D5, chess.D6]:
#                 if board.piece_at(chess.E8) and board.piece_at(chess.E8).symbol() == 'q' and board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
#                     return "Această mutare deschide calea pentru regină și nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#                 elif board.piece_at(chess.E8) and board.piece_at(chess.E8).symbol() == 'q':
#                     return "Această mutare deschide calea pentru regină, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#                 elif board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
#                     return "Această mutare deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#                 else:
#                     return "Această mutare deschide calea pentru dezvoltarea pieselor tale, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#             if move.from_square in [chess.C7] and move.to_square in [chess.C5, chess.C6]:
#                 return " Prin aceasta mutare, vei produce o presiune în centrul tablei și vei crea opțiuni de atac sau dezvoltare agresivă."
#             if move.from_square in [chess.B7] and move.to_square in [chess.B5, chess.B6]:
#                 if board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b' and board.piece_at(chess.D8) and board.piece_at(chess.D8).symbol() == 'k':
#                     return " Această mutare este o introducere în deschiderea Indiană de rege, pregătind terenul pentru dezvoltarea rapidă a nebunului și a regelui în spatele pionului de pe b7."
#                 elif board.piece_at(chess.C8) and board.piece_at(chess.C8).symbol() == 'b':
#                     return " Această mutare deschide calea pentru nebunul de pe f1, contribuind la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#                 else:
#                     return " Aceasta mutare contribuie la controlul central și la ocuparea unui spațiu mai mare în mijlocul tablei."
#             if move.from_square in [chess.A7] and move.to_square in [chess.A5, chess.A6]:
#                 return "Aceasta mutare descurajeaza dezvoltarea adversarului in zona laterala a tablei si pregateste oportunitati de atac pe flanc."
#             return f" Prin aceasta mutare avansezi strategic pionul si te pregatesti pentru mutarile ulterioare ale partidei. Poti incerca sa promovezi acest pion intr-o regina. Acest lucru iti va da un avantaj semnificativ."
       
#         if board.piece_at(move.from_square).symbol() == 'k':
#             if move.from_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8, chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7, chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6] and move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8, chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]:
#                 return "Prin aceasta mutare asiguri o pozitie mai sigura regelui tau."
#             return " Prin aceasta mutare, regele joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."
        
#         return "Ai realizat o mutare strategică care îți oferă control asupra centrului tablei și te pregătește pentru etapele ulterioare ale partidei."
