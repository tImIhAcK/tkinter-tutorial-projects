import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import ttkbootstrap as ttkb
from employee_record import EmployeeRecord


class Authentication(ttkb.Window):
    def __init__(self):
        super().__init__()
        self.title('Employee Record Management - Authentication')
        self.geometry("500x200")

        self.login_frame = tk.LabelFrame(
            self, text='Welcome back', padx=5, pady=5)
        self.login_frame.pack(padx=5, pady=5)

        self.signup_frame = tk.LabelFrame(
            self, text='Create an account', padx=5, pady=5)
        self.signup_frame.pack(padx=5, pady=5)

        self.create_db_connection()
        self.create_table()
        self.create_admin_user()

        self.create_login_page()

    def create_db_connection(self):
        self.conn = sqlite3.connect('employee.db')
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )""")
        self.conn.commit()

    def create_admin_user(self):
        self.cur.execute("SELECT * FROM users WHERE username=?", ('admin',))
        admin_user = self.cur.fetchone()
        if not admin_user:
            self.cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin'))
            self.conn.commit()

    def create_login_page(self):
        # Username label and entry
        self.label_username = ttkb.Label(
            self.login_frame, text='Username:', font=("Cascade", 10))
        self.label_username.grid(row=0, column=0, pady=5, padx=5, sticky='e')
        self.entry_username = ttkb.Entry(self.login_frame)
        self.entry_username.grid(row=0, column=1, pady=5, padx=5, sticky='w')

        # Password label and entry
        self.label_password = ttkb.Label(
            self.login_frame, text='Password:', font=("Cascade", 10))
        self.label_password.grid(row=1, column=0, pady=5, padx=5, sticky='e')
        self.entry_password = ttkb.Entry(self.login_frame, show='*')
        self.entry_password.grid(row=1, column=1, pady=5, padx=5, sticky='w')

       # Create the login button with the custom style
        self.login_button = ttkb.Button(
            self.login_frame, text='Login', command=self.login, bootstyle="success")
        self.login_button.grid(row=2, columnspan=2, pady=2, ipadx=110)

        # Create the signup button with the custom style
        self.signup_button = ttkb.Button(
            self.login_frame, text='Signup', command=self.create_signup_page, bootstyle="primary, link")
        self.signup_button.grid(row=3, columnspan=2, pady=2, ipadx=110)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            self.cur.execute(
                "SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = self.cur.fetchone()

            if user:
                messagebox.showinfo('Login Successful',
                                    f'Welcome, {username}!')
                # Create an instance of EmployeeRecord
                employee_record_window = EmployeeRecord()
                employee_record_window.mainloop()  # Open the EmployeeRecord window
            else:
                messagebox.showerror(
                    'Login Failed', 'Invalid username or password')
        else:
            messagebox.showerror('Error', 'All fields are required.')

    def create_signup_page(self):
        self.clear_login_page()

        self.label_new_username = ttkb.Label(
            self.signup_frame, text='Username: ', font=("Cascade", 10))
        self.label_new_username.grid(row=0, column=0, pady=2)
        self.entry_new_username = ttkb.Entry(self.signup_frame)
        self.entry_new_username.grid(row=0, column=1, pady=2)

        self.label_new_password = ttkb.Label(
            self.signup_frame, text='Password: ', font=("Cascade", 10))
        self.label_new_password.grid(row=1, column=0, pady=2)
        self.entry_new_password = ttkb.Entry(self.signup_frame, show='*')
        self.entry_new_password.grid(row=1, column=1, pady=2)

        self.signup_button = ttkb.Button(
            self.signup_frame, text='Create account', command=self.create_account, style="success")
        self.signup_button.grid(row=3, columnspan=2, pady=2, ipadx=110)

    def create_account(self):
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()

        if new_username and new_password:
            self.cur.execute(
                "SELECT * FROM users WHERE username=?", (new_username,))
            existing_user = self.cur.fetchone()
            if existing_user:
                messagebox.showerror('Error', 'Username already exists')
            else:
                self.cur.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)', (new_username, new_password))
                self.conn.commit()
                messagebox.showinfo('Account Created',
                                    'Account created successfully')
                self.clear_signup_page()
                self.create_login_page()
        else:
            messagebox.showerror('Error', 'All fields are required')

    def clear_login_page(self):
        self.label_username.grid_forget()
        self.entry_username.grid_forget()
        self.label_password.grid_forget()
        self.entry_password.grid_forget()
        self.login_button.grid_forget()
        self.signup_button.grid_forget()
        self.login_frame.destroy()

        # Recreate the signup frame after destroying it
        self.login_frame = tk.LabelFrame(
            self.master, text='Welcome back', padx=5, pady=5)
        self.login_frame.pack(padx=5, pady=5)

    def clear_signup_page(self):
        self.label_new_username.grid_forget()
        self.entry_new_username.grid_forget()
        self.label_new_password.grid_forget()
        self.entry_new_password.grid_forget()
        self.button_create_account.grid_forget()
        self.signup_frame.destroy()

        # Recreate the signup frame after destroying it
        self.signup_frame = tk.LabelFrame(
            self.master, text='Create an account', padx=5, pady=5)
        self.signup_frame.pack(padx=5, pady=5)

# "estheroyinyedee@gmail.com"
