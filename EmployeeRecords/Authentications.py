import tkinter as tk
from tkinter import messagebox
import sqlite3


class Authentication:
    def __init__(self, master):
        self.master = master
        self.master.title('Employee Record Management - Authentication')
        self.master.geometry("500x200")

        self.login_frame = tk.LabelFrame(
            self.master, text='Welcome back', padx=5, pady=5)
        self.login_frame.pack(padx=5, pady=5)

        self.signup_frame = tk.LabelFrame(
            self.master, text='Create an account', padx=5, pady=5)
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
        self.label_username = tk.Label(
            self.login_frame, text='Username: ')
        self.label_username.grid(row=0, column=0, pady=2)
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.grid(row=0, column=1, pady=2)

        self.label_password = tk.Label(
            self.login_frame, text='Password: ')
        self.label_password.grid(row=1, column=0, pady=2)
        self.entry_password = tk.Entry(self.login_frame, show='*')
        self.entry_password.grid(row=1, column=1, pady=2)

        self.login_button = tk.Button(self.login_frame, text='Login', command=self.login,
                                      bg='green', fg='white', borderwidth=2, relief="raised")
        self.login_button.grid(row=2, columnspan=2, pady=2)

        self.signup_button = tk.Button(self.login_frame, text='Signup', command=self.create_signup_page,
                                       bg='blue', fg='white', borderwidth=2, relief="raised")
        self.signup_button.grid(row=3, columnspan=2, pady=2)

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
                self.master.destroy()
                import employee_record
                employee_record.EmployeeRecord(tk.Tk())
            else:
                messagebox.showerror(
                    'Login Failed', 'Invalid username or password')
        else:
            messagebox.showerror('Error', 'All fields are required.')

    def create_signup_page(self):
        self.clear_login_page()

        self.label_new_username = tk.Label(
            self.signup_frame, text='Username: ')
        self.label_new_username.grid(row=0, column=0, pady=2)
        self.entry_new_username = tk.Entry(self.signup_frame)
        self.entry_new_username.grid(row=0, column=1, pady=2)

        self.label_new_password = tk.Label(
            self.signup_frame, text='Password: ')
        self.label_new_password.grid(row=1, column=0, pady=2)
        self.entry_new_password = tk.Entry(self.signup_frame, show='*')
        self.entry_new_password.grid(row=1, column=1, pady=2)

        self.button_create_account = tk.Button(self.signup_frame, text='Create account', command=self.create_account,
                                               bg='green', fg='white', borderwidth=2, relief="raised")
        self.button_create_account.grid(row=2, columnspan=2, pady=2)

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
