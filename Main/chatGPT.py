"""
import openai
import tkinter as tk
from tkinter import scrolledtext

def ChatGPT(prompt):
    openai.api_key = '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'
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0.5, 
        max_tokens=100  
    )
    generated_text = response.choices[0].text.strip()
    return generated_text




def send_message():
    message = entry.get()
    if message.strip() != "":
        add_message("You", message)
        add_message("EduBot", ChatGPT(message))
        entry.delete(0, tk.END)

def add_message(sender, message):
    chat_box.configure(state='normal')
    chat_box.insert(tk.END, sender + ": " + message + "\n")
    chat_box.configure(state='disabled')
    chat_box.yview(tk.END)

# Create the main window
window = tk.Tk()
window.title("Chat Bot")

# Create a scrolled text box to display the chat
chat_box = scrolledtext.ScrolledText(window, height=20, width=50, font=("Arial", 12))
chat_box.pack(padx=10, pady=10)
chat_box.configure(state='disabled')

# Create an entry field to type messages
entry = tk.Entry(window, width=50, font=("Arial", 12))
entry.pack(padx=10, pady=10)

# Create a send button
send_button = tk.Button(window, text="Send", command=send_message, font=("Arial", 12))
send_button.pack(padx=10, pady=10)
window.bind('<Return>', lambda event=None: send_button.invoke())
# Run the application
window.mainloop()
"""








import openai

# Set up your API key
openai.api_key = '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'
num_prompts = 3

for i in range(num_prompts):
    prompt = input("You: ")
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=2, 
        max_tokens=100  
    )
    generated_text = response.choices[0].text.strip()

    print("EduBoT:", generated_text)
    print("-------------------------------------------------------")
