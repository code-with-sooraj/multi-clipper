import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import json
import os

# Store clipboard items in a persistent file
CLIPBOARD_FILE = "clipboard_data.json"

clipboard_items = []

def load_clipboard_data():
    """Load clipboard items from the persistent file."""
    if os.path.exists(CLIPBOARD_FILE):
        with open(CLIPBOARD_FILE, 'r') as f:
            global clipboard_items
            clipboard_items = json.load(f)
            update_listbox()

def save_clipboard_data():
    """Save clipboard items to the persistent file before closing."""
    with open(CLIPBOARD_FILE, 'w') as f:
        json.dump(clipboard_items, f)

def add_to_clipboard():
    """Add new text from input box to the clipboard."""
    text = input_box.get("1.0", tk.END).strip()
    if text:
        clipboard_items.append(text)
        input_box.delete("1.0", tk.END)
        update_listbox()

def copy_to_clipboard(event):
    """Copy selected text from the listbox to the system clipboard."""
    selection = listbox.curselection()
    if selection:
        text = clipboard_items[selection[0]]
        pyperclip.copy(text)
        status_label.config(text=f"Copied: {text}")

def update_listbox():
    """Update the listbox with all stored clipboard items."""
    listbox.delete(0, tk.END)
    for item in clipboard_items:
        listbox.insert(tk.END, item)

def delete_from_clipboard():
    """Delete the selected clipboard item."""
    selection = listbox.curselection()
    if selection:
        del clipboard_items[selection[0]]
        update_listbox()

def update_clipboard():
    """Update the selected clipboard item with new input."""
    selection = listbox.curselection()
    if selection:
        new_text = input_box.get("1.0", tk.END).strip()
        if new_text:
            clipboard_items[selection[0]] = new_text
            input_box.delete("1.0", tk.END)
            update_listbox()

def minimize_window():
    """Minimize the window."""
    root.iconify()

def on_close():
    """Handle application close event."""
    save_clipboard_data()
    root.destroy()

root = tk.Tk()
root.title("Multi Clipboard")
root.geometry("400x500")
root.configure(bg="#2c2f33")
root.resizable(True, True)

# Make the window always on top
root.attributes('-topmost', True)

# Header with title and minimize/close buttons
header_frame = tk.Frame(root, bg="#23272a", relief="raised", bd=1)
header_frame.pack(fill=tk.X, side=tk.TOP)

# Input box for new clipboard entries
input_box = tk.Text(root, height=3, width=50, bg="#7289da", fg="white", insertbackground="white", font=("Arial", 12))
input_box.pack(pady=10)

# Button frame for Add, Update, and Delete buttons
button_frame = tk.Frame(root, bg="#2c2f33")
button_frame.pack(pady=5)

add_button = ttk.Button(button_frame, text="Add", command=add_to_clipboard, style="Custom.TButton")
add_button.grid(row=0, column=0, padx=5)

update_button = ttk.Button(button_frame, text="Update", command=update_clipboard, style="Custom.TButton")
update_button.grid(row=0, column=1, padx=5)

delete_button = ttk.Button(button_frame, text="Delete", command=delete_from_clipboard, style="Custom.TButton")
delete_button.grid(row=0, column=2, padx=5)

# Configure button styling
style = ttk.Style()
style.configure("Custom.TButton", font=("Arial", 12), padding=5, relief="flat", borderwidth=1)

# Listbox for displaying stored clipboard items
listbox = tk.Listbox(root, height=15, width=50, bg="#23272a", fg="white", selectbackground="#7289da", font=("Arial", 12))
listbox.pack(pady=10)
listbox.bind('<<ListboxSelect>>', copy_to_clipboard)

# Status label for copy events
status_label = tk.Label(root, text="Select an item to copy it to the clipboard.", bg="#2c2f33", fg="white", font=("Arial", 10))
status_label.pack(pady=5)

# Add padding around all widgets
for widget in root.pack_slaves():
    widget.pack_configure(padx=10, pady=5)

# Load clipboard data after initializing all widgets
load_clipboard_data()

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
