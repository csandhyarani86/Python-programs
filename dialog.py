from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw() 
filename = askopenfilename() 
print(filename)
filename1 = askopenfilename()
print filename1
