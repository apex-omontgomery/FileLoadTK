from tkinter import *
from tkinter import filedialog
import os
import pdb
class GUI(Frame):
    def __init__(self, parent, desktop):
        self.desktop = desktop
        Frame.__init__(self, parent)
        self.parent = parent
        self.user_wants_file = None
        self.input_list_file = None
        self.input_log_location = None
        self.output_name = None
        self.num_user_entered = 0
        self.file_button_names = ['Log List', 'User Spec']
        self.folder_button_names = ['Log Location']
        self.initUI()
    
    def submit_button(self):
        b = Button(self.parent, text='Submit', command=self.onExit )     
        b.grid(column=2, row=0, rowspan=3 )
    
    def initUI(self):
        self.grid(row=3,column=3, sticky=NSEW)
        self.parent.title("LogAnalysis")
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)
        [self.init_file_button(button_text) for button_text in self.file_button_names]
        [self.init_folder_button(button_text) for button_text in self.folder_button_names]        
        #self.string_entry()
    
    def put_text_next_to_button(self, name, row_location):
        display_text = StringVar(self.parent, value=name)
        display = Label(self.parent, textvariable=display_text)      
        if self.parent.grid_slaves(column=1):
            [widget.grid_forget() for widget in self.parent.grid_slaves(column=1) if widget.grid_info()['row'] == row_location]      
        display.grid(row=row_location, column=1,sticky=W)         
        if len(self.parent.grid_slaves(column = 1)) == 3:
            self.submit_button()            
        
    def get_folder_name(self, name, row_location):
        setattr(self, name, filedialog.askdirectory( initialdir=self.desktop, title='Select a {} directory'.format(name)))
        self.put_text_next_to_button(getattr(self,name), row_location)
        
    def get_file_name(self, name, row_location):        
        setattr(self, name, filedialog.askopenfilename(initialdir=self.desktop, title="Select file",
                                               filetypes=(("All Files", "*.*"), ("csv files", "*.csv"),
                                                          ("text files", "*.txt"), ("xlsx files", "*.xlsx"))))
        self.put_text_next_to_button(getattr(self,name), row_location)
        
    def init_folder_button(self, button_text):
        b = Button(self.parent, text=button_text, width=11, 
                    command=lambda: self.get_folder_name(button_text, b.grid_info()['row'] )) # lambda to prevent call. 
        row_count = self.get_row_position(len(self.parent.grid_slaves(column = 0)))
        b.grid(row=self.get_row_position(row_count), sticky=W, column=0)
        
    def init_file_button(self, button_text):
        b = Button(self.parent, text=button_text, width=11, 
                    command=lambda: self.get_file_name(button_text, b.grid_info()['row']) )  
        row_count = self.get_row_position(len(self.parent.grid_slaves(column = 0)))          
        b.grid(row=self.get_row_position(row_count),sticky=W, column=0)

    def onExit(self):
        self.quit()
    
    def get_row_position(self, row_count):
        if row_count:
            return row_count
        else:
            return 0

def main():
    Desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    root = Tk()
    root.geometry("400x80+300+300")
    #root.resizable(False, False)
    app = GUI(root, Desktop )
    root.mainloop()


if __name__ == '__main__':
    main()
