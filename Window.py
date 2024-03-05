from tkinter import *
from tkinter import messagebox as message
from tkinter import filedialog as fd
from Stack import *


class Window:
    def __init__(self):
        self.isFileOpen, self.File, self.isFileChange = True, "", False
        self.elecnt, self.mode = 0, "normal"
        self.fileTypes = [('All Files', '*.*'), ('Python Files', '*.py'), ('Text Document', '*.txt')]

        jls_extract_var = self
        jls_extract_var.window = Tk()
        self.window.geometry("1200x700+200+150")
        self.window.wm_title("Untitled")

        self.TextBox = Text(self.window, highlightthickness=0, font=("Comic Sa", 14))
        self.menuBar = Menu(self.window, bg="#eeeeee", font=("Helvetica", 13), borderwidth=0)
        self.window.config(menu=self.menuBar)

        self.init_file_menu()
        self.init_edit_menu()
        self.init_view_menu()

        self.UStack = Stack(self.TextBox.get("1.0", "end-1c"))
        self.RStack = Stack(self.TextBox.get("1.0", "end-1c"))


    def init_file_menu(self):
        self.fileMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.fileMenu.add_command(label="    New       Ctrl+N", command=self.new_file)
        self.fileMenu.add_command(label="    Open      Ctrl+O", command=self.open_file)
        self.fileMenu.add_command(label="    Save         Ctrl+S", command=self.retrieve_input)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="    Exit          Ctrl+D", command=self._quit)
        self.menuBar.add_cascade(label="   File   ", menu=self.fileMenu)


    def init_edit_menu(self):
        self.editMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.editMenu.add_command(label="    Undo    Ctrl+Z", command=self.undo)
        self.editMenu.add_command(label="    Redo    Ctrl+Shift+Z", command=self.redo)

        self.editMenu.add_separator()

        self.editMenu.add_command(label="    Cut    Ctrl+X", command=self.cut)
        self.editMenu.add_command(label="    Copy    Ctrl+C", command=self.copy)
        self.editMenu.add_command(label="    Paste   Ctrl+V", command=self.paste)
        self.menuBar.add_cascade(label="   Edit   ", menu=self.editMenu)

    def init_view_menu(self):
        self.viewMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.viewMenu.add_command(label="   Change Mode   ", command=self.change_color)
        self.menuBar.add_cascade(label="   View   ", menu=self.viewMenu)


    def new_file(self):
        self.TextBox.config(state=NORMAL)
        if self.isFileOpen:
            if len(self.File) > 0:
                if self.isFileChange:
                    self.save_file(self.File)
                self.window.wm_title("Untitled")
                self.TextBox.delete('1.0', END)
                self.File = ''

            else:
                if self.isFileChange:
                    result = message.askquestion('Bruh Chill', 'Do You Want to Save Changes?')
                    self.save_new_file(result)
                self.window.wm_title("Untitled")
                self.TextBox.delete('1.0', END)

        else:
            self.isFileOpen = True
            self.window.wm_title("Untitled")
        self.isFileChange = False
        if self.UStack.size() > 0:
            self.UStack.clear_stack()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))


# 2. Open a file which opens a file in editing mode
    def open_file(self):
        self.TextBox.config(state=NORMAL)
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)

        filename = fd.askopenfilename(filetypes=self.fileTypes, defaultextension=".txt")
        if len(filename) != 0:
            self.isFileChange = False
            outfile = open(filename, "r")
            text = outfile.read()

            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)
            self.window.wm_title(filename)
            self.isFileOpen = True
            self.File = filename

        if self.UStack.size() > 0:
            self.UStack.clear_stack()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))


    # 3. Save file
    def save_file(self, file):
        result = message.askquestion('Window Title', 'Do You Want to Save Changes')
        if result == "yes":
            if len(file) == 0:
                saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
                print(saveFile.name)
                self.write_file(saveFile.name)
                self.TextBox.delete('1.0', END)
            else:
                self.write_file(file)


    # 4. Save new file -> this function is for saving the new file
    def save_new_file(self, result):
        self.isFileChange = False
        if result == "yes":
            saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
            self.write_file(saveFile.name)
            self.File = saveFile.name
        else:
            self.TextBox.delete('1.0', END)


    # 5. Writing in file
    def write_file(self, file):
        inputValue = self.TextBox.get("1.0", "end-1c")
        outfile = open(file, "w")
        outfile.write(inputValue)


    # 6. Getting the data from file and showing in the text widget box
    def retrieve_input(self):
        if self.isFileOpen and len(self.File) != 0:
            self.write_file(self.File)
            self.isFileChange = False
        else:
            self.save_new_file("yes")
            self.window.wm_title(self.File)
            self.isFileOpen = True


    # 7. This function invokes whenever a key is pressed whether it is a special-key or a normal key
    def key_pressed(self, event):

        if event.char == "\x1a" and event.keysym == "Z":
            self.redo()
        elif event.char == "\x1a" and event.keysym == "z":
            self.undo()

        elif event.char == "\x13":
            self.retrieve_input()

        elif event.char == "\x0f":
            self.open_file()
        elif event.char == "\x0e":

            self.new_file()
        elif event.char == "\x04":
            self._quit()

        elif event.char == " " or event.char == ".":
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)

        elif event.keysym == 'Return':
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")

            self.UStack.add(inputValue)
        elif event.keysym == 'BackSpace':

            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)

        elif (event.keysym == 'Up' or event.keysym == 'Down') or (event.keysym == 'Left' or event.keysym == 'Right'):

            self.isFileChange = True
            self.elecnt = 0
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)

        else:
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            if self.elecnt >= 1:
                self.UStack.remove()
            self.UStack.add(inputValue)
            self.elecnt += 1


        if self.TextBox.get("1.0", "end-1c") == self.UStack.ele(0):
            self.isFileChange = False


    # 8. Undo the data by calling Stack class functions
    def undo(self):
        self.isFileChange = True
        if self.UStack.size() == 1:
            self.UStack.remove()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))

        else:
            self.RStack.add(self.UStack.remove())
            text = self.UStack.peek()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)


    # 9. Redo/Rewrite the task/data by calling Stack class functions
    def redo(self):
        if self.RStack.size() > 1:
            text = self.RStack.peek()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)
            self.UStack.add(text)
            self.RStack.remove()


    # 10. Close the window (called when the close button at the right-top is clicked)
    def on_closing(self):
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)
        self._quit()


    # 11. Quit or Exit Function to exit from Text-Editor
    def _quit(self):
        self.window.quit()
        self.window.destroy()


    # 12. Night mode view by changing the color of Text widget
    def change_color(self):
        if self.mode == "normal":
            self.mode = "dark"
            self.TextBox.configure(background="#121111", foreground="#BDBDBD", font=("Helvetica", 14),
                                   insertbackground="white")

        else:
            self.mode = "normal"
            self.TextBox.configure(background="white", foreground="black", font=("Helvetica", 14),
                                   insertbackground="black")


    # 14. Copy
    def copy(self):
        self.TextBox.clipboard_clear()
        text = self.TextBox.get("sel.first", "sel.last")
        self.TextBox.clipboard_append(text)


    # 15. Cut
    def cut(self):
        self.copy()
        self.TextBox.delete("sel.first", "sel.last")
        self.UStack.add(self.TextBox.get("1.0", "end-1c"))


    # 16. Paste
    def paste(self):
        text = self.TextBox.selection_get(selection='CLIPBOARD')
        self.TextBox.insert('insert', text)
        self.UStack.add(self.TextBox.get("1.0", "end-1c"))
