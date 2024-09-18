import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from helper import query_rag, initialise
import threading

def submit_query():
    query = entry.get()

    submit_button.config(state=ttk.DISABLED)

    thread = threading.Thread(target=run_query, args=(query,))
    thread.start()

def update_history(prompt, reply):
    history_text = history_label.cget("text")
    history_text = history_text + "\nPrompt:\n" + prompt + "\nReply:\n" + reply
    history_label.config(text=history_text) 

def run_query(query):
    initialise()
    output = query_rag(query)
    output_label.config(text=f"{output}")
    update_history(query, output)
    submit_button.config(state=ttk.ACTIVE)

root = ttk.Window(themename="darkly")
root.title("Query Input App")

# Create frames
left_frame = ttk.Frame(root, width=300, height=400, relief=ttk.SUNKEN)
left_frame.grid(row=0, column=0, sticky="nsew")

right_frame = ttk.Frame(root, width=300, height=400, relief=ttk.SUNKEN)
right_frame.grid(row=0, column=1, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

prompt_label = ttk.Label(left_frame, text="Enter Query", font=("Helvetica", 12, "bold"))
prompt_label.pack(pady=10)

history_label = ttk.Label(right_frame, text="History", font=("Helvetica", 12, "bold"))
history_label.pack(pady=10)

history_frame = ttk.Frame(right_frame, width=200, height=400, relief=ttk.SUNKEN)
history_frame.pack()

history_label = ttk.Label(history_frame, text="", font=("Helvetica", 10), bootstyle="info")
history_label.pack()

entry = ttk.Entry(left_frame, width=40, bootstyle="info")
entry.pack(padx=5)

submit_button = ttk.Button(left_frame, text="Submit", bootstyle="primary", command=submit_query)
submit_button.pack(padx=5)

output_label = ttk.Label(left_frame, text="", font=("Helvetica", 10), bootstyle="info")
output_label.pack()

root.mainloop()