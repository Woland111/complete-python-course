import tkinter as tk
from tkinter import ttk, filedialog, messagebox

text_contents = dict()


def check_for_changes():
    current = root.nametowidget(notebook.select())
    content = current.get("1.0", "end-1c")
    name = notebook.tab("current")["text"]

    if hash(content) != text_contents[str(current)]:
        if name[-1] != "*":
            notebook.tab("current", text=name + "*")
    elif name[-1] == "*":
        notebook.tab("current", text=name[:-1])


def close_current_tab():
    current = root.nametowidget(notebook.select())
    if current_tab_unsaved() and confirm_close_tab():
        if len(notebook.tabs()) == 1:
            create_file()

        notebook.forget(current)


def current_tab_unsaved():
    current_tab_name = notebook.tab("current")["text"]
    return current_tab_name[-1] == "*"


def confirm_close_tab():
    return messagebox.askyesno(
        message="You have unsaved changes. Are you sure you want to close this file?",
        icon="question",
        title="Confirm Close",
    )


def confirm_quit():
    unsaved = False

    for tab in notebook.tabs():
        text_widget = root.nametowidget(notebook.select())
        content = text_widget.get("1.0", "end-1c")

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break

    if unsaved:
        confirm = messagebox.askyesno(
            message="You have unsaved changes. Are you sure you want to quit?",
            icon="question",
            title="Confirm Quit",
        )

        if not confirm:
            return

    root.destroy()


def create_file():
    text_area = tk.Text(notebook)
    text_area.pack(fill="both", expand=True)

    notebook.add(text_area, text="Untitled")
    notebook.pack(fill="both", expand=True)
    notebook.select(text_area)

    text_contents[str(text_area)] = hash("")


def open_file():
    file_path = filedialog.askopenfilename()

    try:
        filename = file_path.split("/")[-1]

        with open(file_path, "r") as file:
            content = file.read()

    except (AttributeError, FileNotFoundError):
        print("Open operation cancelled")
        return

    text_area = tk.Text(notebook)
    text_area.insert("end", content)
    text_area.pack(fill="both", expand=True)

    notebook.add(text_area, text=filename)
    notebook.pack(fill="both", expand=True)
    notebook.select(text_area)

    text_contents[str(text_area)] = hash(content)


def save_file():
    file_path = filedialog.asksaveasfilename()

    try:
        filename = file_path.split("/")[-1]
        current = root.nametowidget(notebook.select())
        content = current.get("1.0", "end-1c")

        with open(file_path, "w") as file:
            file.write(content)

    except (AttributeError, FileNotFoundError):
        print("Save operation cancelled")
        return

    notebook.tab("current", text=filename)
    text_contents[str(current)] = hash(content)


root = tk.Tk()
root.title("Teclado Text Editor")
root.option_add("*tearOff", False)

main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=(1), pady=(4, 0))

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar)

menubar.add_cascade(menu=file_menu, label="File")

file_menu.add_command(label="New", command=create_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(
    label="Close Tab", command=close_current_tab, accelerator="Ctrl+Q"
)
file_menu.add_command(label="Exit", command=confirm_quit)

notebook = ttk.Notebook(main)

create_file()

root.bind("<KeyPress>", lambda event: check_for_changes())
root.bind("<Control-n>", lambda event: create_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-q>", lambda event: close_current_tab())
root.bind("<Control-s>", lambda event: save_file())

root.mainloop()
