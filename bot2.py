from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize ChatBot
chatbot = ChatBot("Chatpot", language="english")

# Initialize ChatterBotCorpusTrainer
trainer = ChatterBotCorpusTrainer(chatbot)

# Train ChatBot with data from the YAML file
trainer.train("data/training.yml")

# Train ChatBot with a dataset that contains keywords
# You can create a separate YAML file for these

# After training, you can start interacting with ChatBot
while True:
    query = input("> ")
    if query.lower() in ["exit", "quit", ":q"]:
        break

    # Get the response from ChatBot
    response = chatbot.get_response(query)
    
    # You can add code here to extract keywords from the response
    # and use them in another way, such as storing in a database

    print(response)

    