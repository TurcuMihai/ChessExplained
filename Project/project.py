import chess
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from stockfish import Stockfish

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
        print("1. Show the best move. (natural configuration)")
        print("2. Show the best move. (fen configuration)")
        print("3. I have a question about the rules.")
        print("4. Exit.")
        choice = input("Your choice: ")

        if choice == "1":
            best_move_natural_configuration()
        elif choice == "2":
            best_move_fen_configuration()
        elif choice == "3":
            rules_question()
        elif choice == "4":
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
            if board.turn == chess.WHITE:
                board.push(best_move)
            else:
                legal_moves_list = list(board.legal_moves)
                if legal_moves_list:
                    board.push(legal_moves_list[0])
            print(board)
            
        else:
            print("Invalid FEN configuration!")
    

def best_move_natural_configuration():
    print("Enter the table configuration element by element separated by a space: ")
    user_input = input()
    elemets = user_input.split(" ")
    print(elemets)
    board = chess.Board()
    for i in range(8):
        for j in range(8):
            board[i][j] = elemets[i / 8 + j]
    print(board)

def get_explanation(board, move):

    if board.is_checkmate():
        return " Esti in sah mat. Ai pierdut partida!"

    if board.is_check():
        print (" Esti in sah. Trebuie sa faci aceasta mutare pentru a te apara.")

    if board.is_stalemate():
        return " Este pat. Partiza s-a remizat!"
    
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
    
    if board.turn == chess.WHITE:
        # check if the move is a pawn move
        if board.piece_at(move.from_square).symbol() == 'P':
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
            return f" Prin aceasta mutare avansezi strategic pionul de pe {move.from_square} si te pregatesti pentru mutarile ulterioare ale partidei. Poti incerca sa promovezi acest pion intr-o regina. Acest lucru iti va da un avantaj semnificativ."
        if board.piece_at(move.from_square).symbol() == 'K':
            if move.from_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2, chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3] and move.to_square in [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2]:
                return "Prin aceasta mutare asiguri o pozitie mai sigura regelui tau."
            # verify if move is arroc
            return " Prin aceasta mutare, regele joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."
        
        return "Ai realizat o mutare strategică care îți oferă control asupra centrului tablei și te pregătește pentru etapele ulterioare ale partidei."
    else:
        if board.piece_at(move.from_square).symbol() == 'p': 
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
            return f" Prin aceasta mutare avansezi strategic pionul de pe {move.from_square} si te pregatesti pentru mutarile ulterioare ale partidei. Poti incerca sa promovezi acest pion intr-o regina. Acest lucru iti va da un avantaj semnificativ."
        if board.piece_at(move.from_square).symbol() == 'k':
            if move.from_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8, chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7, chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6] and move.to_square in [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8, chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]:
                return "Prin aceasta mutare asiguri o pozitie mai sigura regelui tau."
            # verify if move is arroc
            return " Prin aceasta mutare, regele joaca un rol mai activ in capturarea de pioni sau in limitarea mobilitatii regelui advers."
        
        return "Ai realizat o mutare strategică care îți oferă control asupra centrului tablei și te pregătește pentru etapele ulterioare ale partidei."
            

if __name__ == "__main__":
    chatbot = ChatBot("Chatpot")
    stockfish = Stockfish(path="C:\stockfish\stockfish-windows-x86-64-avx2.exe")
    #train()
    board = chess.Board("rnbqkbnr/ppppp1pp/8/5p2/2P5/5P2/PP1PP1PP/RNBQKBNR b KQkq - 0 1")
    move = chess.Move.from_uci("e8f7")  # O mutare pentru a promova pionul la regină
    explanation = get_explanation(board, move)
    print(explanation)
    main()

    # if board.is_insufficient_material(board):
    #     return " Această mutare determină remiză prin material insuficient."
    
    # if board.is_fivefold_repetition(board):
    #     return " Această mutare determină remiză prin repetarea aceleiași poziții de 5 ori."
    
    # if board.is_seventyfive_moves(board):
    #     return " Această mutare determină remiză prin 75 de mutări consecutive fără captură sau mutare de pion."
    
    # if board.is_variant_end(board):
    #     return " Această mutare determină remiză prin final de variantă."
    
    # if board.is_game_over(board):
    #     return " Această mutare determină remiză prin final de partidă."
    
    # if board.is_irreversible(board):
    #     return " Această mutare determină remiză prin imposibilitatea de a mai realiza o captură sau mutare de pion."
    






# def get_explanation(board, move):
#     if move.promotion:
#         promoted_piece = chess.piece_name(move.promotion).lower()
#         return f"Ai promovat un pion și ai obținut o nouă {promoted_piece}, ceea ce îți oferă un avantaj semnificativ."

#     if board.is_capture(move):
#         captured_piece = board.piece_at(move.to_square)
#         if captured_piece:
#             return f"Ai capturat o {captured_piece.symbol()} și ai eliminat o amenințare asupra poziției tale."

#     # Adaugă variante suplimentare în funcție de logica specifică aici
#     if move.from_square in [chess.B1, chess.G1] and move.to_square in [chess.C3, chess.F3]:
#         return "Ai dezvoltat un cal la o poziție centrală, consolidând controlul asupra centrului tablei."
    
#     if move.from_square in [chess.D2] and move.to_square in [chess.D4] and board.piece_at(chess.E7) and board.piece_at(chess.E7).symbol() == 'p':
#         return "Ai efectuat un avans dublu de pion pentru a controla centrul și pentru a descuraja o ripostă cu pionul negru."

#     if move.from_square in [chess.E2, chess.D2] and move.to_square in [chess.E4, chess.D4]:
#         return "Ai făcut o deschidere centrală, eliberând calea pentru dezvoltarea pieselor tale."

#     if move.from_square in [chess.E1] and move.to_square in [chess.G1]:
#         return "Ai realizat un arroc de partea reginei, poziționând regele într-o poziție mai sigură."

#     if move.from_square in [chess.D1] and move.to_square in [chess.H5] and board.piece_at(chess.G8) and board.piece_at(chess.G8).symbol() == 'N':
#         return "Ai lansat o amenințare asupra reginei negre, forțând-o să se mute sau să facă un schimb dezavantajos."

#     if move.from_square in [chess.E2] and move.to_square in [chess.E4] and board.piece_at(chess.E7) and board.piece_at(chess.E7).symbol() == 'p':
#         return "Ai pregătit o posibilă captură en passant, forțând o decizie din partea adversarului."

#     # Adaugă oricate variante dorești în funcție de contextul jocului de șah.

#     return "Ai realizat o mutare strategică care îți oferă control asupra centrului tablei și te pregătește pentru etapele ulterioare ale partidei."


# def get_explanation(board, move):
#     if move.promotion:
#         return f"Ai promovat un pion și ai obținut o nouă regină, ceea ce îți oferă un avantaj semnificativ."

#     if board.is_capture(move):
#         captured_piece = board.piece_at(move.to_square)
#         return f"Ai capturat o {captured_piece.symbol()} și ai eliminat o amenințare asupra poziției tale."

#     # Adaugă variante suplimentare în funcție de logica specifică aici
#     if move.from_square in [chess.B1, chess.G1] and move.to_square in [chess.C3, chess.F3]:
#         return "Ai dezvoltat un cal la o poziție centrală, consolidând controlul asupra centrului tablei."
    
#     if move.from_square in [chess.D2] and move.to_square in [chess.D4] and board.piece_at(chess.E7).symbol() == 'p':
#         return "Ai efectuat un avans dublu de pion pentru a controla centrul și pentru a descuraja o ripostă cu pionul negru."

#     if move.from_square in [chess.E2, chess.D2] and move.to_square in [chess.E4, chess.D4]:
#         return "Ai făcut o deschidere centrală, eliberând calea pentru dezvoltarea pieselor tale."

#     if move.from_square in [chess.E1] and move.to_square in [chess.G1]:
#         return "Ai realizat un arroc de partea reginei, poziționând regele într-o poziție mai sigură."

#     if move.from_square in [chess.D1] and move.to_square in [chess.H5] and board.piece_at(chess.G8).symbol() == 'N':
#         return "Ai lansat o amenințare asupra reginei negre, forțând-o să se mute sau să facă un schimb dezavantajos."

#     if move.from_square in [chess.E2] and move.to_square in [chess.E4] and board.piece_at(chess.E7).symbol() == 'p':
#         return "Ai pregătit o posibilă captură en passant, forțând o decizie din partea adversarului."

#     # Adaugă oricate variante dorești în funcție de contextul jocului de șah.

#     return "Ai realizat o mutare strategică care îți oferă control asupra centrului tablei și te pregătește pentru etapele ulterioare ale partidei."