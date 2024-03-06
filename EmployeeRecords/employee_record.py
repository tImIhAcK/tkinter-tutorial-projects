import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


class EmployeeRecord:
    def __init__(self, master):
        self.master = master
        self.master.title('Employee Record Management - Record')
        self.master.geometry("500x400")

        self.list_record_frame = tk.LabelFrame(
            self.master, text='Employee Record', padx=5, pady=5)
        self.list_record_frame.pack(padx=5, pady=5)

        self.create_db_connection()
        self.create_table()

        self.list_employee()

    def create_db_connection(self):
        self.conn = sqlite3.connect('employee.db')
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            deparment TEXT NOT NULL,
            position TEXT NOT NULL
        )""")
        self.conn.commit()

    def list_employee(self):
        # Create a Treeview widget
        tree = ttk.Treeview(self.list_record_frame, columns=(
            "id", "firstname", "lastname", "department", "position", "actions"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("firstname", text="First Name")
        tree.heading("lastname", text="Last Name")
        tree.heading("department", text="Department")
        tree.heading("position", text="Position")
        tree.heading("actions", text="Actions")  # New column for actions

        # Retrieve data from the database
        self.cur.execute("SELECT * FROM employee")
        data = self.cur.fetchall()

        # Insert data into the Treeview
        for record in data:
            # Adding an empty string as a placeholder for actions
            tree.insert("", "end", values=(*record, ""))

        # Add buttons for each row
        for row_id in tree.get_children():
            edit_button = tk.Button(self.list_record_frame, text="Edit", bg='orange', fg="white", borderwidth=2, relief='solid',
                                    command=lambda row=row_id: self.edit_employee(row))
            delete_button = tk.Button(
                self.list_record_frame, text="Delete", bg='red', fg="white", borderwidth=2, relief='solid', command=lambda row=row_id: self.delete_employee(row))
            tree.set(row_id, "Actions", "")
            tree.window_create(row_id, window=edit_button)
            tree.set(row_id, "Actions", "")
            tree.window_create(row_id, window=delete_button)

        # Pack the Treeview widget
        tree.pack()

    def edit_employee(self, row_id):
        # Retrieve the data of the selected row
        item = self.cur.execute("SELECT * FROM employee WHERE id=?", (row_id,))
        data = self.cur.fetchone()

        # Create a new window or dialog for editing the user details
        edit_window = tk.Toplevel(self.master)
        edit_window.title('Edit Employee')
        edit_window.geometry("300x200")

        # self.edit_id_entry = ttk.Entry(edit_window)
        # self.edit_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.edit_firstname_entry = ttk.Entry(edit_window)
        self.edit_firstname_entry.grid(row=1, column=1, padx=5, pady=5)

        self.edit_lastname_entry = ttk.Entry(edit_window)
        self.edit_lastname_entry.grid(row=2, column=1, padx=5, pady=5)

        self.edit_department_entry = ttk.Entry(edit_window)
        self.edit_department_entry.grid(row=3, column=1, padx=5, pady=5)

        self.edit_position_entry = ttk.Entry(edit_window)
        self.edit_position_entry.grid(row=4, column=1, padx=5, pady=5)

        self.save_button = ttk.Button(
            edit_window, text='Save', command=lambda: self.save_changes(row_id))
        self.save_button.grid(row=5, column=1, padx=5, pady=5)

    def save_changes(self, row_id):
        edited_data = (
            self.edit_firstname_entry.get(),
            self.edit_lastname_entry.get(),
            self.edit_department_entry.get(),
            self.edit_position_entry.get()
        )
        # Update the employee data in the database
        self.cur.execute(
            """ UPDATE employee SET firstname=?, lastname=?, department=?, position=? WHERE id=? """, edited_data + (row_id,))
        self.conn.commit()

    def delete_employee(self, row_id):
        # Implement the logic for deleting the user based on the selected row ID
        self.cur.execute("DELETE FROM employee WHERE id=?", (row_id,))
        self.conn.commit()
        # Refresh the table after deletion
        self.list_employee()
