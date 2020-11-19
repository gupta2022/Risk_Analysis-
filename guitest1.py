from tkinter import *
from tkinter import filedialog
base = Tk()
# Create a canvas
base.geometry('500x700')
# Function for opening the file
def file_opener():
   input = filedialog.askopenfile(initialdir="/home/gaurav/Desktop")
   print(type(input))
   print(input.name)
   #base.destroy()
   
   for i in input:
      print(i)
# Button label
x = Button(base, text ='Select a .txt/.csv file', command = lambda:file_opener())
x.pack()
mainloop()