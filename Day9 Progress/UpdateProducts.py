import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import mysql.connector
from tkinter import Toplevel
import easygui

# Set a constant for the font
FONT = ("Arial", 20)

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title=None, prompt=None, initialvalue=None):
        super().__init__(parent)
        self.title(title or "")
        self.result = None
        self.font = FONT

        tk.Label(self, text=prompt, font=self.font).pack(padx=10, pady=10)

        self.entry = tk.Entry(self, font=self.font)
        self.entry.insert(0, initialvalue or "")
        self.entry.pack(padx=10, fill="x")

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="OK", font=self.font, command=self.ok).pack(side="left", padx=10)
        tk.Button(button_frame, text="Cancel", font=self.font, command=self.cancel).pack(side="right")

    def ok(self):
        self.result = self.entry.get()
        self.destroy()

    def cancel(self):
        self.destroy()

class Application(tk.Frame):
    def __init__(self, master=None, product_name=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.table_name = product_name
        self.create_widgets()

    def create_widgets(self):
        self.conn = mysql.connector.connect(
            host='10.5.34.66',
            user='Admin',
            password='TheAdmin',
            database='products'
        )
        self.cursor = self.conn.cursor()

        rename_button = tk.Button(self, text='Rename Product', command=self.rename_table, font=FONT)
        rename_button.pack(side="top")

        self.refresh_data()

        add_button = tk.Button(self, text='Add New', command=self.add_row, font=FONT)
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

        label = tk.Label(frame, text=f'Operation: {operation}, UPH: {uph}', width=70, font=FONT)
        label.pack(side="left")

        edit_button = tk.Button(frame, text='Edit', command=lambda: self.edit_row(operation), font=FONT)
        edit_button.pack(side="left")

        delete_button = tk.Button(frame, text='Delete', command=lambda: self.delete_row(operation), font=FONT)
        delete_button.pack(side="left")

    def edit_row(self, operation):
        # Ask for new values for the row
        dialog = CustomDialog(self.master, title="Input", prompt="New Operation", initialvalue=operation)
        self.wait_window(dialog)
        new_operation = dialog.result

        dialog = CustomDialog(self.master, title="Input", prompt="New UPH")
        self.wait_window(dialog)
        new_uph = dialog.result

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
        dialog = CustomDialog(self.master, title="Input", prompt="New operation")
        self.wait_window(dialog)
        new_operation = dialog.result

        dialog = CustomDialog(self.master, title="Input", prompt="New UPH")
        self.wait_window(dialog)
        new_uph = dialog.result

        if new_operation is not None and new_uph is not None:
            self.cursor.execute(f"INSERT INTO {self.table_name} (Operation, UPH) VALUES (%s, %s)",
                                (new_operation, new_uph))
            self.conn.commit()
            self.refresh_data()

    def rename_table(self):
        dialog = CustomDialog(self.master, title="Input", prompt="New table name")
        self.wait_window(dialog)
        new_table_name = dialog.result

        if new_table_name:
            # Connect to proj1 database
            conn_proj1 = mysql.connector.connect(
                host='10.5.34.66',
                user='Admin',
                password='TheAdmin',
                database='proj1'
            )
            cursor_proj1 = conn_proj1.cursor()

            # Update the product name in all_products table in proj1 database
            cursor_proj1.execute("UPDATE all_products SET product_name = %s WHERE product_name = %s",
                                 (new_table_name, self.table_name))
            conn_proj1.commit()

            # Close proj1 connection
            cursor_proj1.close()
            conn_proj1.close()

            # Rename the table in the products database
            self.cursor.execute(f"RENAME TABLE {self.table_name} TO {new_table_name}")
            self.conn.commit()

            self.table_name = new_table_name
            self.refresh_data()


class HomePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.conn = mysql.connector.connect(
            host='10.5.34.66',
            user='Admin',
            password='TheAdmin',
            database='products'
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute("SHOW TABLES")
        for table in self.cursor.fetchall():
            self.create_product_row(table[0])

        add_button = tk.Button(self, text='Add New', command=self.add_product, font=FONT)
        add_button.pack(side="top")

    def edit_product(self, product_name):
        # Destroy the current frame and create a new Application frame
        for widget in self.master.winfo_children():
            widget.destroy()
        app = Application(self.master, product_name)
        app.pack()

    def create_product_row(self, product_name):
        frame = tk.Frame(self)
        frame.pack(side="top", fill="x")

        label = tk.Label(frame, text=f'Product: {product_name}', width=70, font=FONT)
        label.pack(side="left")

        edit_button = tk.Button(frame, text='Edit', command=lambda: self.edit_product(product_name), font=FONT)
        edit_button.pack(side="left")

        delete_button = tk.Button(frame, text='Delete', command=lambda: self.delete_product(product_name), font=FONT)
        delete_button.pack(side="left")

    def add_product(self):
        dialog = CustomDialog(self.master, title="Input", prompt="New product name")
        self.wait_window(dialog)
        new_product = dialog.result

        if new_product:
            # Create new table for the product in products database
            self.cursor.execute(f"CREATE TABLE {new_product} (Operation VARCHAR(25), UPH VARCHAR(25))")
            self.conn.commit()

            # Connect to proj1 database
            conn_proj1 = mysql.connector.connect(
                host='10.5.34.66',
                user='Admin',
                password='TheAdmin',
                database='proj1'
            )
            cursor_proj1 = conn_proj1.cursor()

            # Add product to the all_products table in proj1 database
            cursor_proj1.execute("INSERT INTO all_products (product_name) VALUES (%s)", (new_product,))
            conn_proj1.commit()

            # Close proj1 connection
            cursor_proj1.close()
            conn_proj1.close()

            # Refresh the homepage to reflect the changes
            self.refresh_homepage()

    def delete_product(self, product_name):
        if messagebox.askokcancel("Confirm", "Are you sure you want to delete this product?"):
            # Connect to proj1 database
            conn_proj1 = mysql.connector.connect(
                host='10.5.34.66',
                user='Admin',
                password='TheAdmin',
                database='proj1'
            )
            cursor_proj1 = conn_proj1.cursor()

            # Delete the product from all_products table in proj1 database
            cursor_proj1.execute("DELETE FROM all_products WHERE product_name = %s", (product_name,))
            conn_proj1.commit()

            # Close proj1 connection
            cursor_proj1.close()
            conn_proj1.close()

            # Drop the product table in the products database
            self.cursor.execute(f"DROP TABLE IF EXISTS {product_name}")
            self.conn.commit()

            # Refresh the homepage to reflect the changes
            self.refresh_homepage()

    def refresh_homepage(self):
        # Clear the existing data first
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):  # We only want to destroy frames, not buttons
                widget.destroy()
        self.create_widgets()


root = tk.Tk()
home = HomePage(master=root)
home.mainloop()