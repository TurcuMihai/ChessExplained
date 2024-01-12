from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Inițializează ChatBot
chatbot = ChatBot("Chatpot", language="english")

# Inițializează ChatterBotCorpusTrainer
trainer = ChatterBotCorpusTrainer(chatbot)

# Antrenează ChatBot cu datele din fișierul YAML
trainer.train("data/training_data.yml")

# Antrenează ChatBot cu un set de date care să conțină cuvinte cheie
# Poți crea un fișier YAML separat pentru acestea

# După antrenament, poți începe să interacționezi cu ChatBot
while True:
    query = input("> ")
    if query.lower() in ["exit", "quit", ":q"]:
        break

    # Obține răspunsul de la ChatBot
    response = chatbot.get_response(query)
    
    # Poți adăuga aici cod pentru a extrage cuvintele cheie din răspuns
    # și să le utilizezi în alt mod, cum ar fi stocarea într-o bază de date

    print(response)