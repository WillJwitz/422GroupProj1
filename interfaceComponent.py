"""
Team 2
SQ3R ARA Interface Component
William Jurewitz, Hayden Houlihan, Kaleo Montero
Last edited --- 5/4/2025
"""

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

        self.server = serverComp # reference to server component

        self.title("SQ3R Note-Taker") # Set window title
        self.geometry("800x450") # Set window default dimensions

        self.container = tk.Frame(self) # Frame for subframes to sit in
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Creating login screen object (tk.Frame)
        self.login_screen = login(self.container, self)
        self.login_screen.grid(row=0, column=0, sticky="nsew")
        # Creating main menu screen object (tk.Frame)
        self.main_menu = main_menu(self.container, self)
        self.main_menu.grid(row=0, column=0, sticky="nsew")
        
        self.show(self.login_screen)

        #Kaleo: show error message if necessary
        if not error_message is None:
            messagebox.showwarning("SQ3R Note-Taker", error_message)

    # Raises frame object to top of screen, effectively switching menus
    def show(self, screen):
        screen.tkraise()
        if screen == self.main_menu:
            self.main_menu.selector_reset() # special reset function for main to ensure selections are reset


class login(tk.Frame):
    """ Class for the login menu.
        Child of tk.Frame as that
        facilitates the screen switching
        mechanism. Provides basic drop-down
        to select from list of users.
    """
    def __init__(self, container, app):
        # tk.Frame object init
        super().__init__(container)
        self.application = app # reference to app_window calling object to reach server function calls

        # Frame for objects to sit in, helps to center
        self.entry_field = tk.Frame(self)

        # Label to prompt user selection
        self.prompt = tk.Label(self.entry_field, text="Select User", font=("Helvetica", 20))
        self.prompt.pack()

        # Var for user selection options 
        self.user_opt = ["Student1", "Student2", "Student3"]
        # Drop down to present options
        self.user_field = ttk.Combobox(self.entry_field, values=self.user_opt, state="readonly")
        self.user_field.pack()
        # Button to log in
        self.login_butt = tk.Button(self.entry_field, text="Login", command=self.submit_user)
        self.login_butt.pack()
        # Label to display potential error messages if authentication fails
        self.error = tk.Label(self.entry_field, text="")
        self.error.pack()

        self.entry_field.pack(expand=True)

        self.user_field.bind("<Return>", self.submit_user)
        self.user_field.focus_set() # Start program with user selection 'in focus'

    def submit_user(self, event=None):
        # Get user variable selected
        user_entered = self.user_field.get().strip()
       
        if user_entered != "": # If something was actually selected, not default submitted
            auth = self.application.server.authenticate(user_entered) # authenticate with server component
            if auth: # successful authentication
                # display main menu
                self.application.main_menu.set_user(user_entered)
                self.application.show(self.application.main_menu)
            else: # unsuccessful authentication
                # present error
                self.error.config(text="Login Error, User authentication failed, try again.")
                raise Exception("Something occured when authenticating.")
        else:
            self.error.config(text="Login Error, enter a valid name.")
    
class note_menu(tk.Frame):
    """ Class for note taking menu GUI.
        tk.Frame child to facilitate screen switching.
        This menu contains the primary functionality for taking notes.
        Allows user to have a general header, along with a dynamic set
        of subheaders, each with their own unique note body.
        Facilitates numerous subheadings with a drop down, plus, and 
        minus buttons. Save and <<< button used to save files to server,
        and return the main menu."""
    
    def __init__(self, container, app, note: tuple):
        super().__init__(container)
        self.application = app # app_window reference

        #Separate note file name and dict containing notes.
        self.note = note[1] # dict
        self.note_name = note[0] # str
        self.pdf = note[2] # str
        self.pdf_path = note[3] # str

        #Grab header, subheader, and body notes from passed dict.
        self.header = self.note["header"]
        self.notes_list = self.note["notes"] # list of tuples
        self.notes_dict = {n[0]:n[1] for n in self.notes_list} # make dict of tuples
        self.sub_list = list(self.notes_dict.keys()) # list of keys aka subheaders
        self.current = "" # set currently editing to startup val

        self.just_typed = [""] # array to store what was typed into subheading selection
        self.sub_var = tk.StringVar() # var to track what is in entryfield
        self.sub_var.trace_add("write", self.on_type)

        #Font Sizes
        self.header_size = 18
        self.subheader_size = 15
        self.note_body_size = 12

        #Configure window grid with two rows and two column.
        #thin header and left sidebar
        self.grid_rowconfigure(0, minsize = 60, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, minsize=30, weight=0)
        self.grid_columnconfigure(0, minsize = 30, weight = 0)
        self.grid_columnconfigure(1, weight = 1)
       
        #Framing for top row to do sq3r tips
        self.top_frame = tk.Frame(self)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, minsize=30)
        self.top_frame.grid(row=0, column=1, sticky="ew")

        #SQ3R tips
        self.tips_frame = tips(self.top_frame)
        self.tips_frame.grid(row=0, column=0, sticky="nsew")
        self.showing = False

        #Header label
        note_words = f"Editing {self.note_name}"
        self.note_label = tk.Label(self.top_frame, text=note_words, font = ('Helvetica', 20))
        self.note_label.grid(row=0, column=0, sticky="nsew")

        #SQ3R button
        self.tips_butt = tk.Button(self.top_frame, text="SQ3R", font=('Helvetica', 10), command=self.show_tips)
        self.tips_butt.grid(row=0, column=1, sticky="nsew", padx=5)

        # Bottom bar button frame
        self.butt_frame = tk.Frame(self)
        self.butt_frame.rowconfigure(0, weight=1)
        self.butt_frame.columnconfigure(0, weight=1)
        self.butt_frame.columnconfigure(1, weight=1)
        self.butt_frame.grid(row=2, column=1)

        #Create Back Button
        self.back_button = tk.Button(self, text="<<<", font=('Helvetica', 12), command=self.back)
        self.back_button.grid(row=0, column=0, sticky="ew", padx=5)

        #Create Save Button
        self.save_butt = tk.Button(self.butt_frame, text = "SAVE", font = ('Helvetica', 10), command=self.save)
        self.save_butt.grid(row = 0, column = 0, sticky="nsew")
        
        #Create PDF Button
        self.pdf_butt = tk.Button(self.butt_frame, text="PDF", font = ('Helvetica', 10), command=self.open_pdf)
        self.pdf_butt.grid(row=0, column=1, sticky="nsew")

        #Create container for text fields.
        self.text_container = tk.Frame(self)
        self.text_container.grid_rowconfigure(0, weight=0)
        self.text_container.grid_rowconfigure(1, weight=0)
        self.text_container.grid_rowconfigure(2, weight=1)
        self.text_container.grid_columnconfigure(0, weight=1)
        self.text_container.grid(row=1, column=1, sticky="nsew")

        #Create header text area, configure, and load text.
        self.header_field = tk.Entry(self.text_container, font=('Helvetica', self.header_size))
        self.header_field.insert(tk.END, self.header)
        self.header_field.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        #Create subheader text area, etc.
        self.sub_frame = tk.Frame(self.text_container) # frame to get some buttons next to selector
        self.sub_frame.rowconfigure(0, weight= 1)
        self.sub_frame.columnconfigure(0, weight=1)
        self.sub_frame.columnconfigure(1, minsize=10)
        self.sub_frame.columnconfigure(2, minsize=10)
        self.sub_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        # Selection field for subheadings
        self.subheader_field = ttk.Combobox(self.sub_frame, textvariable=self.sub_var, font=('Helvetica', self.subheader_size), values=self.sub_list)
        self.subheader_field.set("Select note section, or type new subheader and press enter.") # Default text
        self.subheader_field.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.subheader_field.bind("<<ComboboxSelected>>", self.sub_select)
        self.subheader_field.bind("<Return>", self.sub_select)
        

        # Button to make new subheading and note
        self.add_butt = tk.Button(self.sub_frame, text = "+", font = ('Helvetica', 10), command=self.add_subnote)
        self.add_butt.grid(row=0, column=1, sticky="nsew", padx=2)
        
        # Button to delete current subheading and note
        self.delete_butt = tk.Button(self.sub_frame, text = "-", font = ('Helvetica', 10), command=self.remove_subnote)
        self.delete_butt.grid(row=0, column=2, sticky="nsew", padx=2)
        
        # Create note field
        self.note_field = tk.Text(self.text_container, font=('Helvetica', self.note_body_size), wrap="word", height=10)
        self.note_field.insert(tk.END, "")
        self.note_field.grid(row=2, column=0, pady=5, sticky="nsew", padx=10)
  
        if self.notes_dict:
            self.subheader_field.set(list(self.notes_dict.keys())[0])
            self.note_field.insert(tk.END, self.notes_dict[list(self.notes_dict.keys())[0]])
            self.current = list(self.notes_dict.keys())[0]

    # Function to get called when subheading field is typed in or changed
    def on_type(self, *args):
        new = self.subheader_field.get() # get new entry data
        if new != "" and new not in self.sub_list: # if it is a unique new subheader
            self.just_typed[0] = new # set var to what was just typed

    # Called by + button
    def add_subnote(self, event=None):
        selected = self.subheader_field.get().strip() # new selected or entered subheader
        body = self.note_field.get("1.0", "end-1c") # current note body
        # Save current subheading and body if it is not the default or empty
        if selected != "Select note section, or type new subheader and press enter." and selected != "":
            self.notes_dict[selected] = body
        
        # Reset entry area for new subheading
        self.subheader_field.set("")
        self.note_field.delete("1.0", tk.END)
        self.note_field.insert(tk.END, "")

        self.current = ""
        self.sub_list = list(self.notes_dict.keys())
        self.subheader_field.config(values=self.sub_list)

    # Removes a subheading and related note body
    def remove_subnote(self, event=None):

        selected = self.subheader_field.get().strip() # deleting this subheading
        del self.notes_dict[selected] # remove it from internal storage dict
        
        # Reset entry area
        self.subheader_field.set("")
        self.note_field.delete("1.0", tk.END)
        self.note_field.insert(tk.END, "")

        self.current = ""
        self.sub_list = list(self.notes_dict.keys())
        self.subheader_field.config(values=self.sub_list)

    # Called when a subheading is selected from the drop down
    def sub_select(self, event=None):
        selected = self.subheader_field.get().strip() # new selected or entered subheader
        body = self.note_field.get("1.0", "end-1c") # potentially contains old notes

        print(f"selcted: {selected}, current: {self.current}") # debug print

        # Edge case
        if selected == "":
            print("Can't handle blank name")
            return

        if self.current == "": # new note of some kind
            if self.just_typed[0] not in self.notes_dict and self.just_typed[0] != "": # check if just_typed has tracked a new subheader, since it would have been overridden by selection
                self.notes_dict[self.just_typed[0]] = body # save new note dict
                self.just_typed[0] = "" # reset just typed var

            if selected in self.notes_dict: # if newly selected exits (it should) switch to view it
                self.note_field.delete("1.0", tk.END)
                self.note_field.insert(tk.END, self.notes_dict[selected])
            else: # catch case, selected should exist however if it doesn't it will be saved
                self.notes_dict[selected] = body
            self.current = selected

        elif self.current != "": # just entered or selected note, not first time or pre-existing note file
            self.notes_dict[self.current] = body
            if selected in self.notes_dict:
                self.note_field.delete("1.0", tk.END)
                self.note_field.insert(tk.END, self.notes_dict[selected])
            else:
                self.notes_dict[selected] = ""
                self.note_field.delete("1.0", tk.END)
            self.current = selected
        
        self.sub_list = list(self.notes_dict.keys())
        self.subheader_field.config(values=self.sub_list)
                
    def save(self, event = None):
        sub = self.subheader_field.get()
        body = self.note_field.get("1.0", "end-1c")
        self.notes_dict[sub] = body
        note = {}
        note["header"] = self.header_field.get()
        note["notes"] = list(self.notes_dict.items())

        server = self.application.server
        server.send_note(self.pdf, self.note_name, note)
        print("note saved")

    def show_tips(self, event=None):
        if self.showing is True:
            self.note_label.tkraise()
            self.showing = False
        elif self.showing is False:
            self.tips_frame.tkraise()
            self.showing = True

    def back(self, event=None):
        #go back to previous menu
        self.save()
        self.application.show(self.application.main_menu)
        self.destroy()
    
    def open_pdf(self, event=None):
        #Open PDF in user's default viewer.
        if self.pdf_path != "":
            subprocess.Popen([self.pdf_path], shell=True)
        else:
            print("No pdf selected.")
    
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
        self.header = tk.Label(self, text=self.header_text, font=('Helvetica', 20))
        self.header.grid(row=0,column=1,sticky="ew")

        # Menu button setup and display
        self.logout_button = tk.Button(self, text="<<<", font=('Helvetica', 12), command=self.logout)
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
        self.pdf_label = tk.Label(self.pdf_selector_frame, text="Select a PDF file from the dropdown.", font=("Helvetica", 18))
        self.pdf_label.pack(fill="both")
        self.pdf_options = self.application.server.get_pdfs()
        self.pdf_select = ttk.Combobox(self.pdf_selector_frame, values=self.pdf_options, state="readonly")
        self.pdf_select.pack(fill="both", padx=100)
        self.pdf_select.set("--Select a PDF--")
        self.pdf_select.bind("<<ComboboxSelected>>", self.pdf_selected)
        self.pdf_selector_frame.grid(row=0, column=0, padx=50, sticky="ew")

        # Note selector setup
        self.note_selector_frame = tk.Frame(self.note_frame)
        self.note_options = []
        self.note_label = tk.Label(self.note_selector_frame, text="Select note document, or enter new name.", font=("Helvetica", 18))
        self.note_label.pack(fill="both")
        self.note_select = ttk.Combobox(self.note_selector_frame, values=self.note_options, state="normal")
        self.note_select.pack(fill="both", padx=100)
    
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

    def selector_reset(self):
        # Reset main menu when you back out of note menu
        self.pdf_select.set("--Select a PDF--")
        self.pdf = ""
        self.pdf_path = ""
        self.note_select.set("")
        self.note_select.config(values=[])
        self.note_name = ""
        self.note_dict = None
        self.note_frame = None

    def open_note(self, event=None):

        self.note_name = self.note_select.get().strip()
        if self.pdf != "": # cant open note w/o a pdf to associate
            if self.note_name != "": # pickup when no note name selected or entered
                self.note_dict = self.application.server.get_note_file(self.pdf, self.note_name) # get note dict, creates new if note does not exist
                if "header" not in self.note_dict:
                    self.note_dict["header"] = "Header"
                    self.note_dict["notes"] = []


                packed = (self.note_name, self.note_dict, self.pdf, self.pdf_path)

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
        print("note options: ")
        [print(x) for x in self.note_options]
        self.note_select.config(values=self.note_options) # ensure list is reset

    def set_user(self, name):
        self.current_user = name
        self.header.config(text=f"Welcome {self.current_user}. Select a PDF and Note to begin!")

    def logout(self, event=None):
        self.current_user = "temp" # reset to default val
        self.application.show(self.application.login_screen)

class tips(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        #Text for each section
        self.s = "Survey: Skim over the chapter reading the highlighted headers, subheaders, and topic sentences. Study figures, and get a general sense of the chapter's focus."
        self.q = "Question: Form questions that you think may be answered in the reading. Try to form questions for each subheader you looked at."
        self.read = "Read: Read the rest of the text mindfully and try to answer your questions."
        self.recite = "Recite: After reading each section, stop. Try and answer the questions you asked in your own words, without looking at the material." 
        self.review = "Review: After reading the whole chapter or section test your memory by attempting to answer your questions without looking at your notes."
        self.tips_list = [self.s, self.q, self.read, self.recite, self.review]
        self.tips_iter = 0

        #Grid setup for displaying tips
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=20)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, minsize=20)

        #Back button
        self.back_butt = tk.Button(self, text="<", font=('Helvetica', 10), command=lambda: self.iter(i = -1))
        self.back_butt.grid(row=0, column=0, sticky="ew")

        #Forward button
        self.for_butt = tk.Button(self, text=">", font=('Helvetica', 10), command=lambda: self.iter(i = 1))
        self.for_butt.grid(row=0, column=2, sticky="ew")

        #Text display
        self.text = tk.Label(self, text=self.tips_list[self.tips_iter], font=('Helvetica', 15), wraplength=300)
        self.text.grid(row=0, column=1, sticky="nsew")
        self.text.bind("<Configure>", self.update_wrap)

    def iter(self, i, event=None):
        self.tips_iter = (self.tips_iter + i)%5
        self.text.config(text=self.tips_list[self.tips_iter])

    def update_wrap(self, event):
        # Set wraplength to a fraction of the current window width
        self.text.config(wraplength=event.width - 40)

"""
def main():
    serverObject = local_server_component("TestDummies", "TestStorage")

    win = app_window(serverObject, "Running test version, please run app from main.py")
    win.mainloop()
    

if __name__ == "__main__":
    main()
"""