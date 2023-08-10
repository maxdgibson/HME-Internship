from tkinter import *
import tkinter as tk
import mysql.connector
from mysql.connector import Error
from tkinter import OptionMenu, font, StringVar

# Connect to the database
DATABASE_CONFIG = {
    "host": "10.5.34.39",
    "user": "Admin",
    "password": "TheAdmin",
    "database": "productivitytrack"
}

# Connect to the database
def create_conn():
    conn = None
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        if conn.is_connected():
            print("Successfully connected to database")
    except Error as e:
        print(f"Error: {e}")
    return conn

# Fetch data from database
def db_query_func(query, database):
    try:
        DATABASE_CONFIG['database'] = database
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results  # Just return the fetched rows directly
    except mysql.connector.Error as error:
        print(f"Failed to fetch data from MySQL: {error}")
        return []  # Return an empty list in case of an error
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def execute_update(query, database, values=None):
    try:
        DATABASE_CONFIG['database'] = 'productivitytrack'
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        cursor.execute(query, values)
        connection.commit()

        return True

    except mysql.connector.Error as error:
        print(f"Failed to update data in MySQL: {error}")
        return False

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def update_product_options(product_dropdown, product_var):
    # Fetch product options from database
    product_options = db_query_func("SELECT product_name FROM all_products", 'productivitytrack')

    # Check if product_options is empty
    if not product_options:
        product_options = ["No Products"]
    else:
        # Extract string values from tuple
        product_options = [item[0] for item in product_options]

    # Clear the current product options
    product_dropdown['menu'].delete(0, 'end')

    # Set the default option
    product_var.set(product_options[0])

    # Add the product options to the dropdown menu
    for option in product_options:
        product_dropdown['menu'].add_command(label=option, command=tk._setit(product_var, option))


def update_operation_options(product_var, operation_dropdown, operation_var):
    selected_product = product_var.get()

    if selected_product in ['Select Product', 'No Products', 'Loading products...']:
        operation_var.set('Select Operation')  # reset operation dropdown
        operation_dropdown['menu'].delete(0, 'end')  # clear operation dropdown
        return

    # Fetch operation options from the 'products' database
    query = f"SELECT operation FROM `{selected_product}`"
    operation_options = db_query_func(query, 'products')

    # Clear the current operation options
    operation_dropdown['menu'].delete(0, 'end')

    # Set the default option if there are any operations for the selected product
    if operation_options:
        operation_var.set(operation_options[0][0])  # set the first operation as default

        # Add the operation options to the dropdown menu
        for option in operation_options:
            operation_dropdown['menu'].add_command(label=option[0], command=tk._setit(operation_var, option[0]))
    else:
        operation_var.set('Select Operation')  # default option when there are no operations

def calculate_productivity(quantity_entered, hours_dedicated, selected_operation, product_var):
    conn = mysql.connector.connect(
        host='10.5.34.39',
        user='remote_user',
        password='remoteuser',
        database='products'
    )
    cursor = conn.cursor()

    # Execute a query to retrieve the UPH value
    query = "SELECT UPH FROM {} WHERE Operation = %s".format(product_var)
    cursor.execute(query, (selected_operation,))
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    if quantity_entered == '0':
        return 0, 0

    if result is not None:
        uph_value = result[0]
        if uph_value == 'N/A':
            return "N/A", "N/A"
        else:
            hg = float(quantity_entered) * float(uph_value)
            productivity = (hg / float(hours_dedicated)) * 100
            productivity = round(productivity, 2)
            return productivity, hg
    else:
        return "N/A", "N/A"

def update_and_close(window, table, original_id, new_id, new_name, new_hours, new_quantity, new_product, new_operation,
                     original_entry_time):
    Productivity, Hours_Gained = calculate_productivity(new_quantity, new_hours, new_operation, new_product)

    # SQL Update Command with added Entry_Time condition
    update_query = ("""UPDATE work_data
                            SET `ID Number` = %s, 
                                Name = %s, 
                                Hours = %s, 
                                Quantity = %s,
                                Product = %s,
                                Operation = %s, 
                                Productivity = %s,
                                Hours_Gained = %s
                            WHERE `ID Number` = %s 
                            AND `Entry_Time` = %s;""")

    values = (
        new_id, new_name, new_hours, new_quantity, new_product, new_operation, Productivity, Hours_Gained, original_id,
        original_entry_time)

    # Execute Update
    success = execute_update(update_query, DATABASE_CONFIG['database'], values)
    if success:
        print("Data successfully updated!")
    else:
        print("Error updating the data.")

    window.destroy()

    # Refresh the table data
    table.refresh()

class Table:

    def __init__(self, root):
        # Code to fetch data from MySQL
        self.frame = Frame(root)
        self.frame.pack(fill='both', expand='true')

        self.canvas = Canvas(self.frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand='true')

        # Added padding here
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y, padx=(10,0))  # Added padding to the x-direction

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.on_configure)
        self.scrollable_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.lst = db_query_func("SELECT Name, `ID Number`, Hours, Quantity, Product, Operation, Entry_Time FROM work_data", 'productivitytrack')


        # Check if the list has data
        if self.lst:
            total_columns = len(self.lst[0])
        else:
            total_columns = 0  # or another appropriate value
            print("The fetched data list is empty. Please verify your database or query.")

        total_rows = len(self.lst)

        headers = ['Name', 'ID Number', 'Hours', 'Quantity', 'Product', 'Operation', 'Entry Time', ' ']

        # Adjusted font size here
        for j in range(len(headers)):
            e = Label(self.scrollable_frame, text=headers[j], width=15, fg='black', font=('Arial', 12, 'bold'))
            e.grid(row=0, column=j)

        # Adjusted font size and Entry width here
        for i in range(1, total_rows + 1):
            for j in range(total_columns):
                self.e = Entry(self.scrollable_frame, width=15, fg='blue', font=('Arial', 12, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i - 1][j])

            # Adjusted button font size
            edit_button = Button(self.scrollable_frame, text="Edit",
                                 font=('Arial', 12, 'bold'),
                                 command=self.create_edit_command(self.lst[i - 1]))
            edit_button.grid(row=i, column=total_columns, padx=30, pady=5)

    def delete(self):
        """Delete all children (rows) from the table."""
        self.treeview.delete(*self.treeview.get_children())

    def refresh(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.lst = db_query_func("SELECT Name, `ID Number`, Hours, Quantity, Product, Operation, Entry_Time FROM work_data", 'productivitytrack')

        if self.lst:
            total_columns = len(self.lst[0])
        else:
            total_columns = 0  # or another appropriate value
            print("The fetched data list is empty. Please verify your database or query.")

        total_rows = len(self.lst)

        headers = ['Name', 'ID Number', 'Hours', 'Quantity', 'Product', 'Operation', 'Entry Time', ' ']

        # Adjusted font size here
        for j in range(len(headers)):
            e = Label(self.scrollable_frame, text=headers[j], width=15, fg='black', font=('Arial', 12, 'bold'))
            e.grid(row=0, column=j)

        # Adjusted font size and Entry width here
        for i in range(1, total_rows + 1):
            for j in range(total_columns):
                self.e = Entry(self.scrollable_frame, width=15, fg='blue', font=('Arial', 12, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, self.lst[i - 1][j])

            # Adjusted button font size
            edit_button = Button(self.scrollable_frame, text="Edit",
                                 font=('Arial', 12, 'bold'),
                                 command=self.create_edit_command(self.lst[i - 1]))
            edit_button.grid(row=i, column=total_columns, padx=30, pady=5)

    def create_edit_command(self, row):
        #print(row)

        def command():
            self.edit_row(row, self)

        return command

    def edit_row(self, row, table_instance):
        #print(f"Editing row: {row}")
        #print(type(row))

        # Create a new window
        edit_window = Toplevel(root)
        edit_window.geometry('400x400')  # Change this if you want to adjust the size of the edit window
        edit_window.title(f"Edit Data for:  {row[0]}")

        font_size = 20  # Change this to adjust the font size

        # Hidden Entry for Entry_Time
        entry_time_entry = Entry(edit_window)
        #print(row)
        entry_time_entry.insert(0, row[6])  # Entry_Time

        id_num_label = Label(edit_window, text="ID Number", font=('Arial', font_size, 'bold'))
        id_num_label.pack()
        id_num_entry = Entry(edit_window, font=('Arial', font_size))
        id_num_entry.insert(0, row[1])  # ID Number
        id_num_entry.pack()

        name_label = Label(edit_window, text="Name", font=('Arial', font_size, 'bold'))
        name_label.pack()
        name_entry = Entry(edit_window, font=('Arial', font_size))
        name_entry.insert(0, row[0])  # Name
        name_entry.pack()

        hours_label = Label(edit_window, text="Hours", font=('Arial', font_size, 'bold'))
        hours_label.pack()
        hours_entry = Entry(edit_window, font=('Arial', font_size))
        hours_entry.insert(0, row[2])  # Hours
        hours_entry.pack()

        custom_font = font.Font(size=15)  # Adjust the size value as needed

        quantity_label = Label(edit_window, text="Quantity", font=('Arial', font_size, 'bold'))
        quantity_label.pack()
        quantity_entry = Entry(edit_window, font=('Arial', font_size))
        quantity_entry.insert(0, row[3])  # Quantity
        quantity_entry.pack()

        default_font = font.nametofont("TkDefaultFont")
        bigger_font = font.Font(font=default_font, size=12)  # Adjust the size value as needed

        # Operation Dropdown
        operation_var = StringVar()
        operation_dropdown = OptionMenu(edit_window, operation_var, 'Select Operation')
        operation_dropdown.config(font=bigger_font)
        operation_dropdown.pack()

        # Product Dropdown
        product_var = StringVar()
        product_var.trace('w', lambda *args: update_operation_options(product_var, operation_dropdown, operation_var))
        product_dropdown = OptionMenu(edit_window, product_var, "")
        product_dropdown.config(font=bigger_font)
        product_dropdown.pack()
        update_product_options(product_dropdown, product_var)

        update_button = Button(edit_window, text="Update",
                               font=('Arial', 18, 'bold'),
                               command=lambda: update_and_close(edit_window, table_instance, row[1],
                                                                id_num_entry.get(),
                                                                name_entry.get(),
                                                                hours_entry.get(),
                                                                quantity_entry.get(),
                                                                product_var.get(),
                                                                operation_var.get(),
                                                                row[6]))  # This is the Entry_Time
        update_button.pack()
    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

root = Tk()
root.geometry("1240x600")
root.title("                                                                                                                                            EDIT USER ENTRY FORM")
t = Table(root)
root.mainloop()
