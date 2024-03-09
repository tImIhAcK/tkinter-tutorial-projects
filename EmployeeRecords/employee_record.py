import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


class EmployeeRecord(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Employee Record Management - Record')
        self.geometry("850x400")
        self.minsize(650, 400)

        self.list_record_frame = tk.LabelFrame(
            self, text='Employee Record', padx=5, pady=5)
        self.list_record_frame.pack(padx=5, pady=5)

        self.create_db_connection()
        self.create_table()

        self.list_employee()

        # Add a button for adding a new record
        self.add_record_button = ttk.Button(
            self, text='Add New Record', command=self.add_new_record)
        self.add_record_button.pack(side='left', padx=5, pady=10)

        self.edit_record_button = ttk.Button(
            self, text='Edit Selected Record', command=self.edit_record)
        self.edit_record_button.pack(side='left', padx=5, pady=10)

        self.delete_record_button = ttk.Button(
            self, text='Delete Selected Record', command=self.delete_record)
        self.delete_record_button.pack(side='left', padx=5, pady=10)

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
        self.scrollbar = ttk.Scrollbar(
            self.list_record_frame, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='x')

        self.tree.configure(xscrollcommand=self.scrollbar.set)

        self.tree.column('id', width=30, anchor='c')
        self.tree.column('firstname', width=120, anchor='sw')
        self.tree.column('lastname', width=120, anchor='sw')
        self.tree.column('department', width=140, anchor='sw')
        self.tree.column('position', width=140, anchor='sw')

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
            # Insert the buttons into the Treeview
            self.tree.insert("", "end", values=(*record,))

        # Pack the Treeview widget
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def add_new_record(self):
        # Create a new window for adding a new record
        self.add_record_window = tk.Toplevel(self)
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
            self.edit_record_button.destroy()
            self.delete_record_button.destroy()

            # Refresh the table after adding a new record
            self.recreate()
        else:
            messagebox.showwarning('Info', 'All fields are required')

    def edit_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_record = self.tree.item(selected_item)['values']
            selected_record_id = self.tree.item(selected_item)['values'][0]
            self.edit_employee(selected_record_id, selected_record)
        else:
            messagebox.showwarning('No Record Selected',
                                   'Please select a record to edit.')

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            if messagebox.askyesno('Confirm Deletion', 'Are you sure you want to delete this record?'):
                selected_record_id = self.tree.item(selected_item)['values'][0]
                self.delete_employee(selected_record_id)
        else:
            messagebox.showwarning('No Record Selected',
                                   'Please select a record to delete.')

    def edit_employee(self, row_id, record):
        # Create a new window or dialog for editing the user details
        self.edit_window = tk.Toplevel(self)
        self.edit_window.title('Edit Employee')
        self.edit_window.geometry("300x200")

        self.edit_firstname_label = ttk.Label(
            self.edit_window, text='Firstname: ')
        self.edit_firstname_label.grid(row=0, column=0)
        self.edit_firstname_entry = ttk.Entry(self.edit_window)
        self.edit_firstname_entry.grid(row=0, column=1, padx=5, pady=5)
        self.edit_firstname_entry.insert(0, record[1])  # Set placeholder value

        self.edit_lastname_label = ttk.Label(
            self.edit_window, text='Lastname: ')
        self.edit_lastname_label.grid(row=1, column=0)
        self.edit_lastname_entry = ttk.Entry(self.edit_window)
        self.edit_lastname_entry.grid(row=1, column=1, padx=5, pady=5)
        self.edit_lastname_entry.insert(0, record[2])  # Set placeholder value

        self.edit_department_label = ttk.Label(
            self.edit_window, text='Department: ')
        self.edit_department_label.grid(row=2, column=0)
        self.edit_department_entry = ttk.Entry(self.edit_window)
        self.edit_department_entry.grid(row=2, column=1, padx=5, pady=5)
        self.edit_department_entry.insert(
            0, record[3])  # Set placeholder value

        self.edit_position_label = ttk.Label(
            self.edit_window, text='Position: ')
        self.edit_position_label.grid(row=3, column=0)
        self.edit_position_entry = ttk.Entry(self.edit_window)
        self.edit_position_entry.grid(row=3, column=1, padx=5, pady=5)
        self.edit_position_entry.insert(0, record[4])  # Set placeholder value

        self.save_button = ttk.Button(
            self.edit_window, text='Save', command=lambda: self.save_changes(row_id))
        self.save_button.grid(row=4, column=1, padx=5, pady=5)

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
        self.conn.commit()
        messagebox.showinfo("Successfully updated",
                            "Employee record updated successfully")

        # Close the edit window
        self.edit_window.destroy()
        self.list_record_frame.destroy()
        self.add_record_button.destroy()
        self.edit_record_button.destroy()
        self.delete_record_button.destroy()

        # Refresh the table after adding a new record
        self.recreate()

    def delete_employee(self, row_id):
        # Implement the logic for deleting the user based on the selected row ID
        self.cur.execute("DELETE FROM employee WHERE id=?", (row_id,))
        self.conn.commit()

        self.list_record_frame.destroy()
        self.add_record_button.destroy()
        self.edit_record_button.destroy()
        self.delete_record_button.destroy()

        self.recreate()

    def recreate(self):
        self.list_record_frame = tk.LabelFrame(
            self, text='Employee Record', padx=5, pady=5)
        self.list_record_frame.pack(padx=5, pady=5)

        self.list_employee()

        self.add_record_button = ttk.Button(
            self, text='Add New Record', command=self.add_new_record)
        self.add_record_button.pack(side='left', padx=5, pady=10)

        self.edit_record_button = ttk.Button(
            self, text='Edit Selected Record', command=self.edit_record)
        self.edit_record_button.pack(side='left', padx=5, pady=10)

        self.delete_record_button = ttk.Button(
            self, text='Delete Selected Record', command=self.delete_record)
        self.delete_record_button.pack(side='left', padx=5, pady=10)
