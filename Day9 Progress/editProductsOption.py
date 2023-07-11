import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import mysql.connector


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.table_name = 'prodnametest'
        self.create_widgets()

    def create_widgets(self):
        # Database connection
        self.conn = mysql.connector.connect(
            host='10.5.34.66',
            user='Admin',
            password='TheAdmin',
            database='proj1'
        )
        self.cursor = self.conn.cursor()

        # Button to rename the table
        rename_button = tk.Button(self, text='Rename Product', command=self.rename_table)
        rename_button.pack(side="top")

        # Load existing data
        self.refresh_data()

        # Button to add a new row
        add_button = tk.Button(self, text='Add New', command=self.add_row)
        add_button.pack(side="top")

    def refresh_data(self):
        # Clear the existing data first
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):  # We only want to destroy frames, not buttons
                widget.destroy()

        # Fetch data from the table
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        for row in self.cursor.fetchall():
            # Create row with buttons
            self.create_row(row[0], row[1])  # Assuming the first column is operation and the second is UPH

    def create_row(self, operation, uph):
        frame = tk.Frame(self)
        frame.pack(side="top", fill="x")

        label = tk.Label(frame, text=f'Operation: {operation}, UPH: {uph}', width=70)
        label.pack(side="left")

        edit_button = tk.Button(frame, text='Edit', command=lambda: self.edit_row(operation))
        edit_button.pack(side="left")

        delete_button = tk.Button(frame, text='Delete', command=lambda: self.delete_row(operation))
        delete_button.pack(side="left")

    def edit_row(self, operation):
        # Here you could ask for new values for the row and update it in the database
        new_operation = simpledialog.askstring("Input", "New Operation", initialvalue=operation)
        new_uph = simpledialog.askstring("Input", "New UPH")

        if new_operation is not None and new_uph is not None:
            self.cursor.execute(f"UPDATE {self.table_name} SET Operation = %s, UPH = %s WHERE Operation = %s",
                                (new_operation, new_uph, operation))
            self.conn.commit()
            self.refresh_data()

    def delete_row(self, operation):
        if messagebox.askokcancel("Confirm", "Are you sure you want to delete this row?"):
            self.cursor.execute(f"DELETE FROM {self.table_name} WHERE Operation = %s", (operation,))
            self.conn.commit()
            self.refresh_data()

    def add_row(self):
        new_operation = simpledialog.askstring("Input", "New operation")
        new_uph = simpledialog.askstring("Input", "New UPH")

        if new_operation is not None and new_uph is not None:
            self.cursor.execute(f"INSERT INTO {self.table_name} (Operation, UPH) VALUES (%s, %s)",
                                (new_operation, new_uph))
            self.conn.commit()
            self.refresh_data()

    def rename_table(self):
        new_table_name = simpledialog.askstring("Input", "New table name")
        if new_table_name:
            self.cursor.execute(f"RENAME TABLE {self.table_name} TO {new_table_name}")
            self.conn.commit()
            self.table_name = new_table_name
            self.refresh_data()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
