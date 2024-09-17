import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from helper import query_rag, initialise

def submit_query():
    query = entry.get()

    initialise()
    output = query_rag(query)

    output_label.config(text=f"{output}")

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