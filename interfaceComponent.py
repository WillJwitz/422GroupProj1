import tkinter as tk
from memoryServerComponent import memory_server_component
import subprocess
import os

class app_window(tk.Tk):
    """Class to define the application window.
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

        self.entryField = tk.Frame(self)

        self.prompt = tk.Label(self.entryField, text="Enter Username")
        self.prompt.pack()

        self.username = ""
        self.userField = tk.Entry(self.entryField,textvariable=self.username )
        self.userField.pack()

        self.error = tk.Label(self.entryField, text="")
        self.error.pack()

        self.entryField.pack(expand=True)

        self.userField.bind("<Return>", self.submit_user)
        self.userField.focus_set()

    def submit_user(self, event=None):
        print("ENTER")
        # HAYDEN
        # Use servercomponent to set user
        # Use main_menu.set_user to change user for that class
        # use self.application to access main_menu

        
        # display main menu
        # use self.application.show
        self.application.show(self.application.main_menu)
        pass


class main_menu(tk.Frame):
    def __init__(self, container, app):
        super().__init__(container)
        self.current_user = "temp"

        self.user_label = tk.Label(self, text=self.current_user)
        self.user_label.pack(fill="both", expand=True )

    def set_user(self, name):
        self.current_user = name

def main():
    serverObject = memory_server_component()

    win =  app_window(serverObject)
    win.mainloop()
    

if __name__ == "__main__":
    main()