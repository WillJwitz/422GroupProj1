import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from memoryServerComponent import memory_server_component
import subprocess
import os

class app_window(tk.Tk):
    """ Class to define the application window.
        Different menus will be contained in 
        tkinter 'frames' which can be understood
        as a 'layer' of the display. Screen
        switching will occur via bringing these
        'layers' to the top.
        Child of tk.Tk which is the window class"""
    

    def __init__(self, serverComp):
        super().__init__()

        self.server = serverComp

        self.title("SQ3R Note-Taker") # Set window title
        self.geometry("800x450") # Set window default dimensions

        self.container = tk.Frame(self) # Frame for subframes to sit in
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.scenes = {}
        '''
        self.blank = tk.Frame()
        self.blank.grid(row=0, column=0, sticky="nsew")
        '''
        self.login_screen = login(self.container, self)
        self.login_screen.grid(row=0, column=0, sticky="nsew")
        
        self.main_menu = main_menu(self.container, self)
        self.main_menu.grid(row=0, column=0, sticky="nsew")
        
        self.show(self.login_screen)

    def show(self, screen):
        screen.tkraise()


class login(tk.Frame):
    def __init__(self, container, app):
        super().__init__(container)
        self.application = app

        self.entry_field = tk.Frame(self)

        self.prompt = tk.Label(self.entry_field, text="Enter Username")
        self.prompt.pack()

        self.username = ""
        self.user_field = tk.Entry(self.entry_field,textvariable=self.username )
        self.user_field.pack()

        self.error = tk.Label(self.entry_field, text="")
        self.error.pack()

        self.entry_field.pack(expand=True)

        self.user_field.bind("<Return>", self.submit_user)
        self.user_field.focus_set()

    def submit_user(self, event=None):
        print("ENTER")
        user_entered = self.user_field.get()
        # HAYDEN
        # Use servercomponent to set user and get boolean
        # On server succes:
        # Use main_menu.set_user to change user for that class
        # use self.application to access main_menu
        
        auth = self.application.server.authenticate(user_entered)
        if (auth):
            # display main menu
            # use self.application.show
            self.application.set_user = user_entered
            self.application.show(self.application.main_menu)
        else:
            #WILL
            #Not sure if we even want to handle this error, so feel free to change or completely remove the else part.
            tk.messagebox.showerror("Login Error", "User authentication failed, try again.")
            raise Exception("Something occured when authenticating.")
        
        pass


class main_menu(tk.Frame):
    def __init__(self, container, app):

        # Establish Parent and essential vars
        super().__init__(container)
        self.application = app
        self.current_user = "temp"

        self.pdf = "" # str for pdf name
        self.pdf_path = "" # str for pdf path
        self.note_json = None# var for note json object
        

        # Configure grid to have top and sidebar margins
        self.grid_rowconfigure(0, minsize = 20)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, minsize = 20)
        self.grid_columnconfigure(1, weight = 1)

        # Header text setup and display
        self.header_text = f"Welcome {self.current_user}. Select a PDF and Note to begin!"
        self.header = tk.Label(self, text=self.header_text, font=('Times New Roman', 18))
        self.header.grid(row=0,column=1,sticky="ew")

        # Menu button setup and display
        self.menu_graphic = tk.PhotoImage(file="Assets\\Menu\\menuButton.png")
        self.menu_graphic = self.menu_graphic.subsample(4,4)
        self.logout_button = tk.Button(self, image=self.menu_graphic)
        self.logout_button.grid(row=0,column=0)

        # Frame setup for selections
        self.note_frame = tk.Frame(self)
        self.note_frame.grid_rowconfigure(0, weight=1) # Setup three rows
        self.note_frame.grid_rowconfigure(1, weight=1)
        self.note_frame.grid_rowconfigure(2, weight=1)
        self.note_frame.grid_columnconfigure(0, weight=1) # Setup one column
        self.note_frame.grid(row=1,column=1,sticky="nsew")

        # PDF selector setup
        self.pdf_options = self.application.server.get_pdfs()
        self.pdf_select = ttk.Combobox(self.note_frame, values=self.pdf_options, state="readonly")
        self.pdf_select.grid(row=0,column=0,padx=50,sticky="ew")
        self.pdf_select.set("--Select a PDF--")
        self.pdf_select.bind("<<ComboboxSelected>>", self.pdf_selected)

        # Note selector setup
        self.note_options = []
        self.note_select = ttk.Combobox(self.note_frame, values=self.note_options, state="read")
        self.note_select.grid(row=1,column=0,padx=50,sticky="ew")
        self.note_select.set("Select a PDF First")
        self.note_select.bind("<<ComboboxSelected>>", self.note_selected)

        # Button setup
        self.butt_frame = tk.Frame(self.note_frame)
        self.butt_frame.grid(row=2,column=0,sticky="nsew")
        self.butt_frame.grid_rowconfigure(0, weight=1)
        self.butt_frame.grid_columnconfigure(0, weight=1)
        self.butt_frame.grid_columnconfigure(1, weight=1)
        # Show PDF button --> open pdf without booting into editor
        self.pdf_button = tk.Button(self.butt_frame, text="Open PDF", command=self.show_pdf)
        self.pdf_button.grid(row=0,column=0,sticky="ew", padx=50)
        # Open Note button --> open note in note taking GUI
        self.note_button = tk.Button(self.butt_frame, text="Open Note", command=self.open_note)
        self.note_button.grid(row=0,column=1,sticky="ew",padx=50)

    def open_note(self, event=None):
        # No GUI right now so this will just pass
        pass

    def show_pdf(self, event=None):
        # HAYDEN
        # This relies on the pdf_selected() being implemented properly

        #Open PDF in user's default viewer.
        subprocess.Popen([self.pdf_path], shell=True)

    def note_selected(self, event=None):
        note_name = self.note_select.get()
        print(f"Selected note {note_name}")

    def pdf_selected(self, event=None):
        pdf_name = self.pdf_select.get()
        print(f"Selected {pdf_name}")

        # HAYDEN
        # Need to set the pdf and pdf_path vars local to main menu here
        # Also need to update note_options using server call

        self.pdf = pdf_name
        path = self.application.server.get_pdf_path(pdf_name)
        self.pdf_path = os.getcwd() + path
        #WILL
        #This raises an exception right now, but that looks to be aftermath of Sawyer's implementation in the AbSC, so this should work in the future.
        self.note_options = self.application.server.get_notes(pdf_name)
        

    def set_user(self, name):
        self.current_user = name

def main():
    serverObject = memory_server_component()

    win = app_window(serverObject)
    win.mainloop()
    

if __name__ == "__main__":
    main()
