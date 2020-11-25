import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style(root)
# add label in the layout
style.layout('text.Horizontal.TProgressbar', 
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}), 
              ('Horizontal.Progressbar.label', {'sticky': ''})])
# set initial text
style.configure('text.Horizontal.TProgressbar', text='0 %')
# create progressbar
variable = tk.DoubleVar(root)
pbar = ttk.Progressbar(root, style='text.Horizontal.TProgressbar', variable=variable)
pbar.pack()

def increment():
    pbar.step()  # increment progressbar 
    style.configure('text.Horizontal.TProgressbar', 
                    text='{:g} %'.format(variable.get()))  # update label
    

increment()

root.mainloop()