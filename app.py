import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from helper import query_rag, initialise
import threading

def submit_query():
    query = entry.get()

    submit_button.config(state=ttk.DISABLED)
    initialise()
    thread = threading.Thread(target=run_query, args=(query,))
    thread.start()

    submit_button.config(state=ttk.ACTIVE)

def run_query(query):
    output = query_rag(query)

    # Update the UI
    output_label.config(text=f"{output}")

    # Re-enable the button 
    submit_button.config(state=ttk.NORMAL)

root = ttk.Window(themename="darkly")
root.title("Query Input App")

prompt_label = ttk.Label(root, text="Enter Query", font=("Helvetica", 12, "bold"))
prompt_label.pack(pady=10)

input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

entry = ttk.Entry(input_frame, width=40, bootstyle="info")
entry.pack(side=LEFT, padx=5)

submit_button = ttk.Button(input_frame, text="Submit", bootstyle="primary", command=submit_query)
submit_button.pack(side=LEFT, padx=5)

output_label = ttk.Label(root, text="", font=("Helvetica", 10), bootstyle="info")
output_label.pack(pady=20)

root.mainloop()
