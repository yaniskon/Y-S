# import os
# os.startfile('C:/Users/konst/Documents/Y-S/dsd.txt', 'print') 
import os
import tempfile

# pdf = "C:\Users\konst\Documents\Y-S\d325e.pdf"
filename = tempfile.mktemp("d325e.pdf")
# f1 = open(filename, 'ab')
# f1.write(pdf)

open (filename , "w").write("you sing very nice!")
 #print(filename)
os.startfile(filename, "print")
#os.startfile("C:\Users\konst\Documents\Y-S\d325e.pdf", "print")