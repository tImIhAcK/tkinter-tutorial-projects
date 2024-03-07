import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


class EmployeeRecord:
    def __init__(self, master):
        self.master = master
        self.master.title('Employee Record Management - Record')
        self.master.geometry("1250x500")

        self.list_record_frame = tk.LabelFrame(
            self.master, text='Employee Record', padx=5, pady=5)
        self.list_record_frame.pack(padx=5, pady=5)

        self.create_db_connection()
        self.create_table()

        self.list_employee()

        # Add a button for adding a new record
        self.add_record_button = ttk.Button(
            self.master, text='Add New Record', command=self.add_new_record)
        self.add_record_button.pack(pady=10, ipadx=120)

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
        self.tree = ttk.Treeview(self.list_record_frame, columns=(
            "id", "firstname", "lastname", "department", "position"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("firstname", text="First Name")
        self.tree.heading("lastname", text="Last Name")
        self.tree.heading("department", text="Department")
        self.tree.heading("position", text="Position")

        # Retrieve data from the database
        self.cur.execute("SELECT * FROM employee")
        data = self.cur.fetchall()

        # Insert data into the Treeview
        for record in data:
            # Adding an empty string as a placeholder for actions
            self.tree.insert("", "end", values=(*record,))

        # Pack the Treeview widget
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame for action buttons
        self.button_frame = tk.Frame(self.list_record_frame)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert buttons for each row
        for row_id in self.tree.get_children():
            # Bind double click to edit employee
            self.tree.bind(
                "<Double-1>", lambda row=row_id: self.edit_employee(row))
            row_frame = tk.Frame(self.button_frame)
            row_frame.pack(fill=tk.X)

            edit_button = tk.Button(row_frame, text="Edit", bg='orange', fg="white", relief='solid',
                                    command=lambda row=row_id: self.edit_employee(row))
            edit_button.pack(side=tk.LEFT, padx=1, pady=1)

            delete_button = tk.Button(row_frame, text="Delete", bg='red', fg="white", relief='solid',
                                      command=lambda row=row_id: self.delete_employee(row))
            delete_button.pack(side=tk.LEFT, padx=1, pady=1)

    def add_new_record(self):
        # Create a new window for adding a new record
        self.add_record_window = tk.Toplevel(self.master)
        self.add_record_window.title('Add New Employee Record')
        self.add_record_window.geometry("300x200")

        # Create entry fields for adding a new record
        self.new_firstname_label = ttk.Label(
            self.add_record_window, text='Firstname: ')
        self.new_firstname_label.grid(row=0, column=0)
        self.new_firstname_entry = ttk.Entry(self.add_record_window)
        self.new_firstname_entry.grid(row=0, column=1, padx=5, pady=5)

        self.new_lastname_label = ttk.Label(
            self.add_record_window, text='Lastname: ')
        self.new_lastname_label.grid(row=1, column=0)
        self.new_lastname_entry = ttk.Entry(self.add_record_window)
        self.new_lastname_entry.grid(row=1, column=1, padx=5, pady=5)

        self.new_department_label = ttk.Label(
            self.add_record_window, text='Department: ')
        self.new_department_label.grid(row=2, column=0)
        self.new_department_entry = ttk.Entry(self.add_record_window)
        self.new_department_entry.grid(row=2, column=1, padx=5, pady=5)

        self.new_postion_label = ttk.Label(
            self.add_record_window, text='Position: ')
        self.new_postion_label.grid(row=3, column=0)
        self.new_position_entry = ttk.Entry(self.add_record_window)
        self.new_position_entry.grid(row=3, column=1, padx=5, pady=5)

        self.save_new_button = ttk.Button(
            self.add_record_window, text='Save', command=self.save_new_record)
        self.save_new_button.grid(
            row=4, column=0, columnspan=2, ipadx=50, padx=5, pady=5)

    def save_new_record(self):
        if self.new_firstname_entry.get() and self.new_lastname_entry.get() and self.new_department_entry.get() and self.new_position_entry.get():
            new_data = (
                self.new_firstname_entry.get(),
                self.new_lastname_entry.get(),
                self.new_department_entry.get(),
                self.new_position_entry.get()
            )
            # Insert the new employee record into the database
            self.cur.execute(
                """ INSERT INTO employee (firstname, lastname, deparment, position) VALUES (?, ?, ?, ?) """, new_data)
            self.conn.commit()
            messagebox.showinfo(
                "Record Added", "New employee record added successfully")

            # Close the add record window
            self.add_record_window.destroy()
            self.list_record_frame.destroy()
            self.add_record_button.destroy()

            # Refresh the table after adding a new record
            self.list_record_frame = tk.LabelFrame(
                self.master, text='Employee Record', padx=5, pady=5)
            self.list_record_frame.pack(padx=5, pady=5)

            self.list_employee()
            self.add_record_button = ttk.Button(
                self.master, text='Add New Record', command=self.add_new_record)
            self.add_record_button.pack(pady=10, ipadx=120)
        else:
            messagebox.showwarning('Info', 'All fields are required')

    def edit_employee(self, row_id):
        # Retrieve the data of the selected row
        item = self.cur.execute("SELECT * FROM employee WHERE id=?", (row_id,))
        data = self.cur.fetchone()

        # Create a new window or dialog for editing the user details
        self.edit_window = tk.Toplevel(self.master)
        self.edit_window.title('Edit Employee')
        self.edit_window.geometry("300x200")

        self.edit_firstname_entry = ttk.Entry(self.edit_window)
        self.edit_firstname_entry.grid(row=1, column=1, padx=5, pady=5)

        self.edit_lastname_entry = ttk.Entry(self.edit_window)
        self.edit_lastname_entry.grid(row=2, column=1, padx=5, pady=5)

        self.edit_department_entry = ttk.Entry(self.edit_window)
        self.edit_department_entry.grid(row=3, column=1, padx=5, pady=5)

        self.edit_position_entry = ttk.Entry(self.edit_window)
        self.edit_position_entry.grid(row=4, column=1, padx=5, pady=5)

        self.save_button = ttk.Button(
            self.edit_window, text='Save', command=lambda: self.save_changes(row_id))
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
            """ UPDATE employee SET firstname=?, lastname=?, deparment=?, position=? WHERE id=? """, edited_data + (row_id,))
        if self.conn.commit():
            messagebox.showinfo("Successfully updated",
                                "Employee record updated successfully")
        else:
            messagebox.showinfo("Error", "An unknown error occured")

        # Close the edit window
        self.edit_window.destroy()

    def delete_employee(self, row_id):
        # Implement the logic for deleting the user based on the selected row ID
        self.cur.execute("DELETE FROM employee WHERE id=?", (row_id,))
        self.conn.commit()
        # Refresh the table after deletion
        self.list_employee()
