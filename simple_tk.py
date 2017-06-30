from tkinter import *
from tkinter import filedialog
import os
from DlogProc.LoadDlogList import DlogArray
from DlogProc.CleanDlog import CleanDlog
from SubSearches.PPCLow import PPCLow
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import time

class GUI(Frame):
    def __init__(self, parent, desktop, user_stored_object):
        self.desktop = desktop
        Frame.__init__(self, parent)
        self.parent = parent
        self.user_wants_file = None
        self.input_list_file = None
        self.input_log_location = None
        self.output_name = None
        self.num_user_entered = 0
        self.user_stored_object = user_stored_object
        self.file_button_names = user_stored_object.file_names
        self.folder_button_names = user_stored_object.folder_names
        self.init_user_interface()

    def submit_button(self):
        b = Button(self.parent, text='Submit', command=self.on_submit_button)
        b.grid(column=2, row=0, rowspan=3)

    def on_submit_button(self):
        self.user_stored_object.file_names = [getattr(self, name) for name in self.file_button_names]
        self.user_stored_object.folder_names = [getattr(self, name) for name in self.folder_button_names]
        self.on_exit()

    def init_user_interface(self):
        self.grid(row=3, column=3, sticky=NSEW)
        self.parent.title("LogAnalysis")
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        file_menu = Menu(menubar)
        file_menu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=file_menu)
        [self.init_file_button(button_text) for button_text in self.file_button_names]
        [self.init_folder_button(button_text) for button_text in self.folder_button_names]

    def put_text_next_to_button(self, name, row_location):
        display_text = StringVar(self.parent, value=name)
        display = Label(self.parent, textvariable=display_text)
        if self.parent.grid_slaves(column=1):
            [widget.grid_forget() for widget in self.parent.grid_slaves(column=1) if
             widget.grid_info()['row'] == row_location]
        display.grid(row=row_location, column=1, sticky=W)
        if len(self.parent.grid_slaves(column=1)) == 3:
            self.submit_button()

    def get_folder_name(self, name, row_location):
        setattr(self, name,
                filedialog.askdirectory(initialdir=self.desktop, title='Select a {} directory'.format(name)))
        self.put_text_next_to_button(getattr(self, name), row_location)

    def get_file_name(self, name, row_location):
        setattr(self, name, filedialog.askopenfilename(initialdir=self.desktop, title="Select file",
                                                       filetypes=(("All Files", "*.*"), ("csv files", "*.csv"),
                                                                  ("text files", "*.txt"), ("xlsx files", "*.xlsx"))))
        self.put_text_next_to_button(getattr(self, name), row_location)

    def init_folder_button(self, button_text):
        b = Button(self.parent, text=button_text, width=11,
                   command=lambda: self.get_folder_name(button_text, b.grid_info()['row']))  # lambda to prevent call.
        row_count = self.get_row_position(len(self.parent.grid_slaves(column=0)))
        b.grid(row=self.get_row_position(row_count), sticky=W, column=0)

    def init_file_button(self, button_text):
        b = Button(self.parent, text=button_text, width=11,
                   command=lambda: self.get_file_name(button_text, b.grid_info()['row']))
        row_count = self.get_row_position(len(self.parent.grid_slaves(column=0)))
        b.grid(row=self.get_row_position(row_count), sticky=W, column=0)

    def on_exit(self):
        self.quit()

    def get_row_position(self, row_count):
        if row_count:
            return row_count
        else:
            return 0


class UserStoredVals:
    def __init__(self):
        self.file_names = ['Log List', 'Input Func.']
        self.folder_names = ['Log Location']
        self.dlog_list = None


def main():
    values_to_process = UserStoredVals()
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    root = Tk()
    root.geometry("400x80+300+300")
    app = GUI(root, desktop, values_to_process)
    root.mainloop()
    return values_to_process
    # now we have the dlog file location, user wishes file, and the location of the dlogs.

class GraphOrchestrator:
    def __init__(self, logs, user_values_object):
        self.logs = logs
        self.output_name = self.output_get_unique(user_values_object.file_names[0])
        self.user_values_object = user_values_object
        self.user_args_to_panda_args()
        self.pdf = matplotlib.backends.backend_pdf.PdfPages(self.output_name)
        for file_name in logs:
            print(file_name)
            test = PPCLow(user_values_object.folder_names[0], file_name)     
            if not test.plot:
                print('Error with {}'.format(file_name))
            else:
                self.pdf.savefig(test.plot)
                plt.close('all')
        self.pdf.close() 

    def output_get_unique(self, in_name):
        file_path, file_ext = os.path.splitext(in_name)
        out_name = file_path + '.pdf'
        counter = 1 
        while os.path.isfile(out_name):
            file_path, file_ext = os.path.splitext(out_name)
            out_name = file_path + '_' + str(counter) + file_ext
            counter += 1
        return out_name

    # this going to be a doozy.
    def user_args_to_panda_args(self):
        return

if __name__ == '__main__':
    user_entered_vals_object = main()
