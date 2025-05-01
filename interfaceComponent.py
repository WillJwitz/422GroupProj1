import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from localServerComponent import local_server_component
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
    

    def __init__(self, serverComp, error_message : str = None):
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

        # Frame for objects to sit in, helps to center
        self.entry_field = tk.Frame(self)

        # Label to prompt user selection
        self.prompt = tk.Label(self.entry_field, text="Select User")
        self.prompt.pack()

        self.username = ""
        self.user_opt = ["Student1", "Student2", "Student3"]
        self.user_field = ttk.Combobox(self.entry_field, values=self.user_opt, state="readonly")
        self.user_field.pack()

        self.login_butt = tk.Button(self.entry_field, text="Login", command=self.submit_user)
        self.login_butt.pack()

        self.error = tk.Label(self.entry_field, text="")
        self.error.pack()

        self.entry_field.pack(expand=True)

        self.user_field.bind("<Return>", self.submit_user)
        self.user_field.focus_set()

    def submit_user(self, event=None):
        
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
            self.application.main_menu.set_user(user_entered)
            self.application.show(self.application.main_menu)
        else:
            #WILL
            #Not sure if we even want to handle this error, so feel free to change or completely remove the else part.
            self.error.config(text="Login Error, User authentication failed, try again.")
            raise Exception("Something occured when authenticating.")
        
        pass
    
class note_menu(tk.Frame):
    def __init__(self, container, app, note: tuple):
        super().__init__(container)
        self.application = app
        self.container = container

        #Separate note file name and dict containing notes.
        self.note = note[1] # dict
        self.note_name = note[0] # str


        #Grab header, subheader, and body notes from passed dict.
        self.header = self.note["header"]
        self.subheader = self.note["subheader"]
        self.note_body = self.note["note_body"]

        #Font Sizes
        self.header_size = 18
        self.subheader_size = 15
        self.note_body_size = 12

        #Configure window grid with four rows and one column.
        self.grid_rowconfigure(0, minsize = 30, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, minsize = 20, weight = 1)
        self.grid_columnconfigure(1, weight = 1)


        #Create a scrollbar.
        """ #WILL
        #Not sure how to get this to scroll properly, so I'll leave that to you.
        #Same with the decision on whether we even want to scroll.
        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.scroll.grid(row=0, column=2, rowspan=3, sticky="nse")"""
       

        #Create a label for top row (note name?)
        
        #WILL
        #Label area blows up really large when full-screening.
        note_words = f"Editing {self.note_name}"
        self.note_label = tk.Label(self, text=note_words, font = ('Times New Roman', 18))

        self.note_label.grid_rowconfigure(0, weight = 1)
        self.note_label.grid_columnconfigure(0, weight = 1)
        self.note_label.grid(row=0, column=1)

        #Create Save Button

        #Looks strange when small and messes with other elements.  Really just a placeholder until you get to it.
        self.save_butt = tk.Button(self, width = 6, text = "SAVE", font = ('Times New Roman', 18))

        self.save_butt.grid(row = 2, column = 0, sticky="s")
        
        #Create container for text fields.
        self.text_container = tk.Frame(self)

        self.text_container.grid_columnconfigure(0, weight = 1)
        self.text_container.grid_rowconfigure(0, weight = 1)
        self.text_container.grid_rowconfigure(1, weight = 1)
        self.text_container.grid_rowconfigure(2, weight = 1)
        self.text_container.grid(row=1, column=1, sticky="nsew")

        #Create header text area, configure, and load text.
        self.header_field = tk.Text(self.text_container, height = 1, font = ('Times New Roman', self.header_size))

        self.header_field.insert(tk.END, self.header)
        self.header_field.grid_rowconfigure(0, weight=1)
        self.header_field.grid_columnconfigure(0, weight=1)
        self.header_field.grid(row=0,column=0,sticky="nsew")


        #Create subheader text area, etc.
        self.subheader_field = tk.Text(self.text_container, height = 1 , font = ('Times New Roman', self.subheader_size))

        self.subheader_field.insert(tk.END, self.subheader)
        self.subheader_field.grid_rowconfigure(0, weight=1)
        self.subheader_field.grid_columnconfigure(0, weight=1)
        self.subheader_field.grid(row=1,column=0,sticky="nsew")

        #Create note text area, etc.
        self.note_field = tk.Text(self.text_container, font = ('Times New Roman', self.note_body_size))
        
        self.note_field.insert(tk.END, self.note_body)
        self.note_field.grid_rowconfigure(0, weight=1)
        self.note_field.grid_columnconfigure(0, weight=1)
        self.note_field.grid(row=2,column=0,sticky="nsew")

        #WILL
        #This is what I came up with in the time I had after the meeting.
        #Hopefully this skeleton helps.
        #Let me know when/if there's anything else I can do here.
        #A lot of this stuff is just estimates of how I think stuff will look.
            #You have more tkinter experience, so just edit as much as you want.
    
class main_menu(tk.Frame):
    def __init__(self, container, app):

        # Establish Parent and essential vars
        super().__init__(container)
        self.application = app
        self.current_user = "temp"
        self.container = container

        self.pdf = "" # str for pdf name
        self.pdf_path = "" # str for pdf path
        self.note_name = "" # str for note name
        self.note_dict = None # var for note dict object
        self.note_menu = None # note_menu obj to be filled by open_note
        

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
        self.pdf_selector_frame = tk.Frame(self.note_frame)
        self.pdf_label = tk.Label(self.pdf_selector_frame, text="Select a PDF file from the dropdown.", font=("Times New Roman", 14))
        self.pdf_label.pack(fill="both")
        self.pdf_options = self.application.server.get_pdfs()
        self.pdf_select = ttk.Combobox(self.pdf_selector_frame, values=self.pdf_options, state="readonly")
        self.pdf_select.pack(fill="both")
        self.pdf_select.set("--Select a PDF--")
        self.pdf_select.bind("<<ComboboxSelected>>", self.pdf_selected)
        self.pdf_selector_frame.grid(row=0, column=0, padx=50, sticky="ew")

        # Note selector setup
        self.note_selector_frame = tk.Frame(self.note_frame)
        self.note_options = []
        self.note_label = tk.Label(self.note_selector_frame, text="Select note document, or enter name for new note.", font=("Times New Roman", 14))
        self.note_label.pack(fill="both")
        self.note_select = ttk.Combobox(self.note_selector_frame, values=self.note_options, state="normal")
        self.note_select.pack(fill="both")
    
        self.note_select.bind("<<ComboboxSelected>>", self.note_selected)
        self.note_selector_frame.grid(row=1, column=0, padx=50, sticky="ew")

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

        self.note_name = self.note_select.get().strip()
        if self.pdf != "": # cant open note w/o a pdf to associate
            if self.note_name != "": # pickup when no note name selected or entered
                self.note_dict = self.application.server.get_note_file(self.pdf, self.note_name) # get note dict, creates new if note does not exist
                if "header" not in self.note_dict:

                    self.note_dict["header"] = "Header"
                    self.note_dict["subheader"] = "Subheader"
                    self.note_dict["note_body"] = "Note text"

                    
                    packed = (self.note_name, self.note_dict)

                    # init note menu with note_json
                    self.note_menu = note_menu(self.container, self.application, packed)
                    self.note_menu.grid(row=0, column=0, sticky="nsew")
                    self.application.show(self.note_menu)
            else:
                print("Invalid note name.")
        else:
            print("No pdf selected. Not opening note.")

    def show_pdf(self, event=None):
        #Open PDF in user's default viewer.
        if self.pdf_path != "":
            subprocess.Popen([self.pdf_path], shell=True)
        else:
            print("No pdf selected.")

    def note_selected(self, event=None):
        self.note_name = self.note_select.get()
        print(f"Selected note {self.note_name}")

    def pdf_selected(self, event=None):
        # get selected pdf
        pdf_name = self.pdf_select.get()
        print(f"Selected {pdf_name}") # debug log

        self.pdf = pdf_name # set class var
        path = self.application.server.get_pdf_path(pdf_name) # get path to selected pdf
        self.pdf_path = os.getcwd() + "/" + path # proper formatting
        
        self.note_options = self.application.server.get_notes(pdf_name) # load list of associated notes
        self.note_select.config(values=self.note_options) # ensure list is reset

    def set_user(self, name):
        self.current_user = name
        self.header.config(text=f"Welcome {self.current_user}. Select a PDF and Note to begin!")

def main():
    serverObject = local_server_component("TestDummies", "TestStorage")

    win = app_window(serverObject)
    win.mainloop()
    

if __name__ == "__main__":
    main()
