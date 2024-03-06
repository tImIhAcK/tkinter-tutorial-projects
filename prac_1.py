import tkinter as tk


root = tk.Tk()

root.title("DEMO 1")
root.geometry('800x600')

label = tk.Label(root, text='This is a demo app', background='green')
label.pack(padx=10, pady=10)

input1 = tk.Entry(root)
input1.pack(padx=10, pady=10)

input1 = tk.Entry(root, font='Arial')
input1.pack(padx=10, pady=10)

root.mainloop()
