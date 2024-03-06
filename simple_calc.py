import tkinter as tk
from math import sqrt, pi

root = tk.Tk()
root.title('Basic Calculator')


def button_clicked(number):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, str(current) + str(number))


def clear_entry():
    entry.delete(0, tk.END)


def addition():
    first_number = entry.get()
    global f_num
    global math
    math = "addition"
    f_num = float(first_number)
    entry.delete(0, tk.END)


def subtraction():
    first_number = entry.get()
    global f_num
    global math
    math = "subtraction"
    f_num = float(first_number)
    entry.delete(0, tk.END)


def multiplication():
    first_number = entry.get()
    global f_num
    global math
    math = "multiplication"
    f_num = float(first_number)
    entry.delete(0, tk.END)


def division():
    first_number = entry.get()
    global f_num
    global math
    math = "division"
    f_num = float(first_number)
    entry.delete(0, tk.END)


def equal():
    second_number = entry.get()
    entry.delete(0, tk.END)

    if math == "addition":
        entry.insert(0, f_num + float(second_number))

    if math == "subtraction":
        entry.insert(0, f_num - float(second_number))

    if math == "multiplication":
        entry.insert(0, f_num * float(second_number))

    if math == "division":
        entry.insert(0, f_num / float(second_number))


def modulus():
    first_number = entry.get()
    second_number = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, int(first_number) % int(second_number))


def square():
    number = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, float(number) ** 2)


def square_root():
    number = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, sqrt(float(number)))


def pie():
    entry.delete(0, tk.END)
    entry.insert(0, pi)


def percent():
    first_number = entry.get()
    second_number = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, float(first_number) * float(second_number) / 100)


def main():
    global entry
    entry = tk.Entry(root, width=55, borderwidth=5)
    entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

    button_1 = tk.Button(root, text="1", padx=30, pady=20,
                         command=lambda: button_clicked(1))
    button_2 = tk.Button(root, text="2", padx=30, pady=20,
                         command=lambda: button_clicked(2))
    button_3 = tk.Button(root, text="3", padx=30, pady=20,
                         command=lambda: button_clicked(3))
    button_4 = tk.Button(root, text="4", padx=30, pady=20,
                         command=lambda: button_clicked(4))
    button_5 = tk.Button(root, text="5", padx=30, pady=20,
                         command=lambda: button_clicked(5))
    button_6 = tk.Button(root, text="6", padx=30, pady=20,
                         command=lambda: button_clicked(6))
    button_7 = tk.Button(root, text="7", padx=30, pady=20,
                         command=lambda: button_clicked(7))
    button_8 = tk.Button(root, text="8", padx=30, pady=20,
                         command=lambda: button_clicked(8))
    button_9 = tk.Button(root, text="9", padx=30, pady=20,
                         command=lambda: button_clicked(9))
    button_0 = tk.Button(root, text="0", padx=30, pady=20,
                         command=lambda: button_clicked(0))
    button_add = tk.Button(root, text="+", padx=30, pady=20, command=addition)
    button_sub = tk.Button(root, text="-", padx=31,
                           pady=20, command=subtraction)
    button_mul = tk.Button(root, text="x", padx=30,
                           pady=20, command=multiplication)
    button_div = tk.Button(root, text="/", padx=31, pady=20, command=division)
    button_equal = tk.Button(root, text="=", padx=30,
                             pady=20, bg='orange', fg='white', command=equal)
    button_clear = tk.Button(root, text="C", padx=30,
                             pady=20, bg='red', fg='white', command=clear_entry)
    button_mod = tk.Button(root, text="mod", padx=22, pady=20, command=modulus)
    button_sqr = tk.Button(root, text="x^2", padx=23, pady=20, command=square)
    button_sqrt = tk.Button(root, text="Sqrt", padx=22,
                            pady=20, command=square_root)
    button_dot = tk.Button(root, text=".", padx=31, pady=20,
                           command=lambda: button_clicked('.'))
    button_open_brac = tk.Button(
        root, text="(", padx=31, pady=20, command=lambda: button_clicked('('))
    button_clos_brac = tk.Button(
        root, text=")", padx=31, pady=20, command=lambda: button_clicked(')'))
    button_pie = tk.Button(root, text="pi", padx=23,
                           pady=20, command=pie)
    button_percent = tk.Button(
        root, text="%", padx=29, pady=20, command=percent)

    # Display
    button_1.grid(row=4, column=0)
    button_2.grid(row=4, column=1)
    button_3.grid(row=4, column=2)
    button_sub.grid(row=4, column=3)
    button_equal.grid(row=4, column=4, rowspan=2)

    button_4.grid(row=3, column=0)
    button_5.grid(row=3, column=1)
    button_6.grid(row=3, column=2)
    button_mul.grid(row=3, column=3)
    button_sqrt.grid(row=3, column=4)

    button_7.grid(row=2, column=0)
    button_8.grid(row=2, column=1)
    button_9.grid(row=2, column=2)
    button_div.grid(row=2, column=3)
    button_sqr.grid(row=2, column=4)

    button_0.grid(row=5, column=0)
    button_dot.grid(row=5, column=1)
    button_add.grid(row=5, column=3)
    button_percent.grid(row=5, column=2)

    button_clear.grid(row=1, column=0)
    button_open_brac.grid(row=1, column=1)
    button_clos_brac.grid(row=1, column=2)
    button_mod.grid(row=1, column=3)
    button_pie.grid(row=1, column=4)


if __name__ == '__main__':
    main()
    root.mainloop()
