import tkinter as tk
from guiDevServerComp import guiServerComponent
import subprocess
import os


class testGui():
    '''Class for test gui'''
    
    def __init__(self, serverObj: guiServerComponent):
        '''Init func for testGUI
        
        Creates window object and neccessary interaction
        components and starts the mainloop.

        serverObj: guiDevServerComp object used for
        psuedo backend calls
        '''
        self.server = serverObj
        
        # Window object
        self.window = tk.Tk()
        self.window.title("Test GUI Suite")


        # Frame for grid geometry for buttons
        self.bFrame = tk.Frame(self.window)
        # Adds columns to grid geometry
        self.bFrame.columnconfigure(0, weight=1)
        self.bFrame.columnconfigure(1, weight=1)

        # Creating button objects, to insert in frame use frame as window
        self.pdfButton = tk.Button(self.bFrame, text="PDF", command=self.displayPDF)
        self.pdfButton.grid(row=0, column=0)


        self.saveButton = tk.Button(self.bFrame, text="Save", command=self.saveText)
        self.saveButton.grid(row=0, column=1)
        
        # Pack frame onto window
        self.bFrame.pack(pady=10, fill='x')

        # Create textbox obj and pack onto window
        self.textField = tk.Text(self.window, font=("Arial", 14))
        self.textField.pack(padx=15)

        # Begin displaying window
        self.window.mainloop()

    def displayPDF(self):
        # Function called by PDF button on click

        print("Display PDF")
        # I put this call here to give a starting point
        # for how the interaction would work
        strPdfPath = self.server.strGetPdfPath("/TestDummies/test.pdf") # Gets path to pdf from server
        print(strPdfPath)
        # Use path from server func to open pdf here
        cwd = os.getcwd()

        #Open PDF in user's default viewer.
        subprocess.Popen([cwd+strPdfPath], shell=True)

        
        

    def saveText(self):
        # Function called by save button to save note contents

        # This is getting the text as a str from the box
        strNoteText = self.textField.get('1.0', tk.END)
        print(strNoteText)

        '''
        Calls server function
        Technically this should be json but passing str
        right now for testing purposes since json format isn't
        agreed upon right now. At some point we would have a 
        json pack function to get the json obj and set that off
        to the server after that.
        '''
        self.server.boolSendNote(strNoteText)

    def __del__(self):
        #Destructor to delete the test.txt file after testing.
        cwd = os.getcwd()
        path = "/TestDummies/test.txt"
        if (os.path.isfile(cwd+path)):
            os.remove(cwd+path)


def main():

    serverObject = guiServerComponent()

    gui = testGui(serverObject)
    

if __name__ == "__main__":
    main()
