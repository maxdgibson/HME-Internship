import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

art = r"""

    ██       ██      ███          ███        █████
    ██       ██      ████    ████        ██     
    ██████      ██   ████  ██       █████  
    ██       ██     ██       ██      ██       ██     
    ██       ██     ██                    ██      █████
                                                                                                                        ⠀⠀⠀⠀⠀
"""

# Function to increase font size for all widgets
def increase_font_size(widget, size):
    font = widget['font']
    font_family = font.split(' ')[0]
    widget.configure(font=(font_family, size))

    # Handle OptionMenu widgets separately
    if isinstance(widget, tk.OptionMenu):
        menu = widget['menu']
        menu.configure(font=(font_family, size))
# Function to test the database connection
def test_connection():
    try:
        connection = mysql.connector.connect(
            host='10.5.34.66',
            user='Admin',
            password='TheAdmin',
            database='products'
        )
        connection.close()
        return True
    except mysql.connector.Error as err:
        return False
def insert_data():
    # Get the values from the input fields
    date = datetime.now().strftime('%Y-%m-%d')
    name = name_entry.get()
    id_number = id_entry.get()
    hours = hours_entry.get()
    product = product_var.get()
    operation = operation_var.get()
    quantity = quantity_entry.get()
    # Calculate the productivity
    productivity,hours_gained = calculate_productivity()
    comments = comments_entry.get()

    # Check if any of the required fields are empty
    if not all([name, id_number, hours, product, operation, quantity]):
        messagebox.showerror('Error', 'Please fill in all required fields.')
        return

    # Confirmation pop-up
    result = messagebox.askquestion('Confirmation', 'Are you sure you want to submit?', icon='warning')
    if result == 'no':
        return

    # Establish a connection to the MySQL server
    try:
        connection = mysql.connector.connect(
            host='10.5.34.66',
            user='Admin',
            password='TheAdmin',
            database='proj1'
        )
    except mysql.connector.Error as err:
        messagebox.showerror('Error', f'Error connecting to the database: {err}')
        return

    cursor = connection.cursor()

    # SQL statement to insert data
    sql = "INSERT INTO work_data (`Date`, `Name`, `ID Number`, `Hours`, `Product`, `Operation`, `Quantity`, `Productivity`, `Hours_Gained`, `Comments`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (date, name, id_number, hours, product, operation, quantity, productivity, hours_gained, comments)

    # Execute the SQL statement
    cursor.execute(sql, values)
    connection.commit()

    # Show a success message
    messagebox.showinfo('Success', 'Data inserted successfully!')

    # Reset the input fields
    name_entry.delete(0, 'end')
    id_entry.delete(0, 'end')
    hours_entry.delete(0, 'end')
    product_var.set('select product')
    operation_var.set('Select operation')
    quantity_entry.delete(0, 'end')
    comments_entry.delete(0, 'end')

    # Close the cursor and connection
    cursor.close()
    connection.close()
    sys.exit()

# Define a function to fetch data from the database
def fetch_data_from_proj1(query, database):
    try:
        connection = mysql.connector.connect(
            host='10.5.34.66',
            user='Admin',
            password='TheAdmin',
            database='proj1'
        )

        cursor = connection.cursor()
        cursor.execute(query)

        return [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as error:
        print(f"Failed to fetch data from MySQL: {error}")
        return []  # return an empty list in case of an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data_from_products(query, database):
    try:
        connection = mysql.connector.connect(
            host='10.5.34.66',
            user='Admin',
            password='TheAdmin',
            database='products'
        )

        cursor = connection.cursor()
        cursor.execute(query)

        return [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as error:
        print(f"Failed to fetch data from MySQL: {error}")
        return []  # return an empty list in case of an error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_product_options(*args):
    # Fetch product options from database
    product_options = fetch_data_from_proj1("SELECT product_name FROM all_products", 'proj1')

    # Check if product_options is empty
    if not product_options:
        product_options = ["No Products"]

    # Clear the current product options
    product_dropdown['menu'].delete(0, 'end')

    # Set the default option
    product_var.set(product_options[0])

    # Add the product options to the dropdown menu
    for option in product_options:
        product_dropdown['menu'].add_command(label=option, command=tk._setit(product_var, option))

def update_operation_options(*args):
    selected_product = product_var.get()

    if selected_product in ['Select Product', 'No Products', 'Loading products...']:
        operation_var.set('Select Operation')  # reset operation dropdown
        operation_dropdown['menu'].delete(0, 'end')  # clear operation dropdown
        return

    # Fetch operation options from the 'products' database
    operation_options = fetch_data_from_products(f"SELECT operation FROM {selected_product}", 'products')

    # Clear the current operation options
    operation_dropdown['menu'].delete(0, 'end')

    # Set the default option if there are any operations for the selected product
    if operation_options:
        operation_var.set(operation_options[0])

        # Add the operation options to the dropdown menu
        for option in operation_options:
            operation_dropdown['menu'].add_command(label=option, command=tk._setit(operation_var, option))
    else:
        operation_var.set('Select Operation')  # default option when there are no operations
def calculate_productivity():
    quantity_entered = quantity_entry.get()
    hours_dedicated = hours_entry.get()
    selected_operation = operation_var.get()  # Assuming you have an entry field for operation name

    # Establish a connection to your MySQL database
    conn = mysql.connector.connect(
        host='10.5.34.66',
        user='Admin',
        password='TheAdmin',
        database='products'
    )
    cursor = conn.cursor()

    # Execute a query to retrieve the UPH value
    query = "SELECT UPH FROM {} WHERE Operation = %s".format(product_var.get())
    cursor.execute(query, (selected_operation,))
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

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

# Create the main window
window = tk.Tk()
window.title('                                                                                                                                         DATA ENTRY FORM')
window.geometry('980x340+440+200')
font_size = 20

# Check the database connection and show an error message if it fails
if not test_connection():
    # Send an email
    msg = MIMEMultipart()
    msg['From'] = 'mgibson@hme.com'
    msg['To'] = 'mgibson@hme.com'
    # msg['To'] = 'RepairLeadership@hme.com'
    msg['Subject'] = 'System Error'
    body = 'The system tried to make a connection to the server and was unable to. Use XAMPP to confirm the MySQL Server is running'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(msg['From'], 'Bicheal0!')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    #let the user know that they have an error and that the system is down
    messagebox.showerror('The server appears to be down, please alert a supervisor.', f' {art}')
    sys.exit()

# Initialize the variables for the dropdowns
product_var = tk.StringVar()
operation_var = tk.StringVar()

# Initialize product_options with a default value
product_options = ["Loading products..."]

# Fetch new_product_options from the database
new_product_options = fetch_data_from_proj1("SELECT product_name FROM all_products", 'proj1')

# If new_product_options is not an empty list, update product_options
if new_product_options:
    # Flatten new_product_options into a single list of strings
    product_options = new_product_options

# If product_options is still an empty list, give it a default value
if not product_options:
    product_options = ["No products available"]

# Initialize operation_options with a default value
operation_options = ["Select a product first..."]

# Set the default value for product_var
product_var.set(product_options[0])

# Create OptionMenus with default values
product_dropdown = tk.OptionMenu(window, product_var, "Loading products...")
operation_dropdown = tk.OptionMenu(window, operation_var, operation_options[0])

# Set up the dropdown options for product_dropdown
menu = product_dropdown['menu']
menu.delete(0, 'end')
for product in product_options:
    menu.add_command(label=product, command=tk._setit(product_var, product))

# Update the operation options when a product is selected
product_var.trace('w', update_operation_options)

# Widgets
# Name
name_label = tk.Label(window, text='Name:')
name_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
increase_font_size(name_label, font_size)

name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
increase_font_size(name_entry, font_size)

# ID Number
id_label = tk.Label(window, text='ID Number:')
id_label.grid(row=0, column=2, padx=10, pady=10, sticky='e')
increase_font_size(id_label, font_size)

id_entry = tk.Entry(window)
id_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')
increase_font_size(id_entry, font_size)


operation_var = tk.StringVar(window)
operation_var.set("Select Operation")
operation_dropdown = tk.OptionMenu(window, operation_var, [])
# operation
operation_label = tk.Label(window, text='Operation:')
operation_label.grid(row=2, column=2, padx=10, pady=10, sticky='e')
increase_font_size(operation_label, font_size)

operation_var = tk.StringVar(window)
operation_var.set('Select Operation')  # default option
operation_dropdown = tk.OptionMenu(window, operation_var, '')  # no initial options
operation_dropdown.configure(fg='dark blue')
operation_dropdown.grid(row=2, column=3, padx=10, pady=10, sticky='w')
increase_font_size(operation_dropdown, font_size)

# product
product_label = tk.Label(window, text='Product:')
product_label.grid(row=1, column=2, padx=10, pady=10, sticky='e')
increase_font_size(product_label, font_size)

# Fetch product options from the database
product_options = fetch_data_from_proj1("SELECT product_name FROM all_products", 'proj1') or []


product_var = tk.StringVar(window)
product_var.set('Select Product' if not product_options else product_options[0])  # default option
product_dropdown = tk.OptionMenu(window, product_var, *product_options)
product_dropdown.configure(fg='dark blue')
product_dropdown.grid(row=1, column=3, padx=10, pady=10, sticky='w')
increase_font_size(product_dropdown, font_size)

product_var.trace_add('write', update_operation_options)

# Hours
hours_label = tk.Label(window, text='Hours:')
hours_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
increase_font_size(hours_label, font_size)

hours_entry = tk.Entry(window)
hours_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
increase_font_size(hours_entry, font_size)

# Quantity
quantity_label = tk.Label(window, text='Quantity:')
quantity_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
increase_font_size(quantity_label, font_size)

quantity_entry = tk.Entry(window)
quantity_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
increase_font_size(quantity_entry, font_size)

# Comments
comments_label = tk.Label(window, text='Comments:')
comments_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
increase_font_size(comments_label, font_size)

comments_entry = tk.Entry(window)
comments_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')
increase_font_size(comments_entry, font_size)

# Submit button
submit_button = tk.Button(window, text='Submit', command=insert_data, bg='light green')
submit_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='ew')
# window.grid_columnconfigure(0, weight=1)
# window.grid_columnconfigure(3, weight=1)
increase_font_size(submit_button, font_size)

# Start the Tkinter event loop
#root.mainloop()  # Use this if your main window is 'root'
# OR
window.mainloop()  # Use this if your main window is 'window'