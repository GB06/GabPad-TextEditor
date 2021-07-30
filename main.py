from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title("ThunderPad")
root.geometry("1080x720")


global open_status_name
open_status_name = False

global selected
selected = False


def new_file():
    my_text.delete("1.0", END)
    root.title("New File - ThunderPad")
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False


def open_file():
    my_text.delete("1.0", END)
    text_file = filedialog.askopenfilename(initialdir="", title="Open File",
                                           filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                                      ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        global open_status_name
        open_status_name = text_file

    name = text_file
    status_bar.config(text=f"{name}        ")
    name = name.replace("/Volumes/Backup/", "")
    root.title(f"{name} - ThunderPad")
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    my_text.insert(END, stuff)
    text_file.close()


def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="", title="Save File",
                                             filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                                        ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        status_bar.config(text=f'Saved: {name}        ')
        name = name.replace("/Volumes/Backup/", "")
        root.title(f'{name} - ThunderPad')
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()


def save_file():
    global open_status_name
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()
        status_bar.config(text=f'Saved: {open_status_name}        ')

    else:
        save_as_file()


def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            my_text.delete("sel.first", "sel.last")


def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)
        root.clipboard_clear()
        root.clipboard_append(selected)


def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)





my_frame = Frame(root)
my_frame.pack(pady=5)


text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)


hor_scroll = Scrollbar(my_frame, orient="horizontal")
hor_scroll.pack(side=BOTTOM, fill=X)


my_text = Text(my_frame, width=116, height=36, font=("Helvetica", 24), selectbackground="Light Blue",
               selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="none",
               xscrollcommand=hor_scroll.set)
my_text.pack()


text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)


my_menu = Menu(root)
root.config(menu=my_menu)


file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As...", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste             ", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")


status_bar = Label(root, text="Ready        ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)


root.bind("<Control-Key-x>", cut_text)
root.bind("<Control-Key-c>", copy_text)
root.bind("<Control-Key-v>", paste_text)


root.mainloop()