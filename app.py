import tkinter as tk
from tkinter import ttk
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from PIL import Image, ImageTk

# Create a chatbot instance with machine learning capabilities
chatbot = ChatBot(
    "DesktopChatBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///chatbot_database.sqlite3",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I'm sorry, but I don't understand.",
            "maximum_similarity_threshold": 0.90
        }
    ]
)

# Train the chatbot with both corpus and custom AI-powered data
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train("chatterbot.corpus.english")

custom_trainer = ListTrainer(chatbot)
custom_training_data = [
    "What is AI?",
    "Artificial Intelligence is the simulation of human intelligence in machines.",
    "How does machine learning work?",
    "Machine learning is a subset of AI that allows computers to learn from data without being explicitly programmed.",
    "What is deep learning?",
    "Deep learning is a type of machine learning that uses neural networks to model complex patterns in data."
]
custom_trainer.train(custom_training_data)

# GUI Application using Tkinter with modern styling

def send_message(event=None):
    user_input = user_entry.get()
    if user_input.strip():
        chatbot_response = chatbot.get_response(user_input)
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "You: " + user_input + "\n", "user")
        chat_history.insert(tk.END, "\n", "bot_space")
        chat_history.insert(tk.END, "Bot: " + str(chatbot_response) + "\n\n", "bot")
        chat_history.config(state=tk.DISABLED)
        chat_history.yview(tk.END)
    user_entry.delete(0, tk.END)

# Create main application window
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("400x550")
root.configure(bg="#F2F3F5")
root.minsize(300, 450)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Create chatbot header
header = tk.Frame(root, bg="#2C3E50", height=60)
header.grid(row=0, column=0, sticky="ew")
header.columnconfigure(0, weight=1)

# Load and display chatbot avatar
avatar_img = Image.open("chatbot_avatar.webp").resize((40, 40))
avatar_photo = ImageTk.PhotoImage(avatar_img)
avatar_label = tk.Label(header, image=avatar_photo, bg="#2C3E50")
avatar_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Chatbot name label
chatbot_name = tk.Label(header, text="AI Chatbot", fg="white", bg="#2C3E50", font=("Arial", 14, "bold"))
chatbot_name.grid(row=0, column=1, sticky="w")

# Create a stylish frame for messages
frame = tk.Frame(root, bg="#F2F3F5")
frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

# Create chat history text area with improved visibility
chat_history = tk.Text(frame, wrap=tk.WORD, bg="#FFFFFF", fg="#000000", font=("Arial", 12), relief="flat", borderwidth=5, state=tk.DISABLED)
chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
chat_history.tag_configure("user", foreground="#007AFF", font=("Arial", 12, "bold"), justify="right")
chat_history.tag_configure("bot", foreground="#228B22", font=("Arial", 12, "bold"), justify="left")
chat_history.tag_configure("bot_space", font=("Arial", 2))

# Create entry field for user input with modern styling
input_frame = tk.Frame(root, bg="#F2F3F5")
input_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
input_frame.columnconfigure(0, weight=1)

user_entry = ttk.Entry(input_frame, font=("Arial", 14))
user_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
user_entry.bind("<Return>", send_message)  # Bind Enter key to send_message function

# Create send button with modern styling
send_button = ttk.Button(input_frame, text="Send", command=send_message)
send_button.grid(row=0, column=1, padx=5)

# Run the Tkinter event loop
root.mainloop()
