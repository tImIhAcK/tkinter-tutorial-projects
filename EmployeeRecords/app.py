import tkinter as tk
from authentication import Authentication

if __name__ == '__main__':
    root = tk.Tk()
    app = Authentication(root)
    root.mainloop()
