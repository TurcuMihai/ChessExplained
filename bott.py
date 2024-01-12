# bot.py
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("Chatpot")

trainer = ListTrainer(chatbot)
trainer.train([
    "Hi",
    "Welcome, friend 🤗",
])


with open("data/training.yml", "r") as file:
    line1 = file.readline().strip()
    line2 = file.readline().strip()
    while line1 and line2:
        # Process the two lines here
        print(line1)
        print(line2)           
        trainer.train([line2, line1,])
        line1 = file.readline().strip()
        line2 = file.readline().strip()

# Use the training data as needed


# trainer.train([
#     "How is a pawn promoted in chess?",
#     "When a pawn reaches the opposite side of the board it is promoted to another piece of the same color.",
# ])
# trainer.train([
#    "Tell me about pawn promotion.",
#    "When a pawn reaches the opposite side of the board it is promoted to another piece of the same color.",
# ])
# trainer.train([
#    "What happens when a pawn reaches the other side of the board?",
#    "When a pawn reaches the opposite side of the board it is promoted to another piece of the same color.",
# ])

exit_conditions = (":q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"🪴 {chatbot.get_response(query)}")