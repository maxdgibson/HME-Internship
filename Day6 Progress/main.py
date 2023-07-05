
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

art = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡴⠖⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠲⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⡆⢀⠀⠀⠀⢤⢾⣱⣜⣾⣧⣶⣶⣶⣿⣷⣷⣶⣦⣤⣄⡀⣼⣞⣆⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⡿⡏⡇⡄⢀⣼⣷⣿⣿⣿⣿⣿⣿⡿⠿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⣢⡀⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⡇⠀⠀⣤⠻⡽⣼⣿⣿⣿⣿⡿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠷⢦⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠀⠀⠀⣌⢷⣿⣿⡿⠟⢋⡡⠀⠀⢀⣠⣤⣴⣶⣿⣿⣿⣿⣿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⣈⡙⠶⣤⡀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠀⠀⢦⣸⠛⠛⢁⡀⣀⣈⢀⣴⣾⣿⣿⣿⠏⣿⢿⣿⣿⣿⡏⠈⢻⣿⠿⣿⣶⣔⢿⣦⣠⣮⣽⠛⠀⠀⠙⢦⠀⠀
⠀⠀⠀⠀⠀⢿⠀⣠⠞⢩⣴⣿⡿⡿⣯⣷⣿⣿⣿⣿⣿⠏⢠⡿⢸⣿⣿⡟⠀⠀⠀⢻⡆⠘⣿⣿⣷⣝⠺⣿⣦⠀⠀⠀⠀⠀⢳⡀
⠀⠀⠀⠀⠀⣨⠟⠁⠐⢷⡹⠋⣰⣿⣿⣿⣿⣿⣿⣿⠏⠀⢸⠃⢸⣿⡟⠀⠀⠀⠀⠸⡇⠀⠘⣿⣿⣿⣷⣄⡁⠀⠀⠀⠀⠀⠈⡇
⠀⠀⠀⣠⠞⠁⠀⠀⠀⠈⢀⣼⣿⣿⣿⣿⠏⢸⣿⠇⠀⠠⠏⠀⢸⠏⠀⠀⠀⠀⠀⠀⠇⠀⠀⢸⣿⣿⣏⠉⡉⡀⠀⠀⠀⠀⣰⡇
⠀⠀⡼⠁⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⡟⠀⢸⡟⠀⠀⠀⠀⠘⡏⣀⣿⡒⡿⠀⠀⠀⣀⠀⠀⠈⣿⣿⣿⣧⣿⣿⡆⠀⠀⣠⠏⠀
⠀⣼⠃⠀⢀⣶⣖⡄⠀⣾⣿⣿⣿⣿⣿⠃⠀⢸⣛⣲⣦⣤⣤⣤⣴⡟⠙⣷⣤⣤⠴⠾⠥⣤⡀⠀⣿⣿⡿⠿⣿⣿⠃⢀⡴⠁⠀⠀
⢸⡇⠀⠀⣼⣸⣻⢀⢰⣿⣿⣿⣿⣿⣿⠀⠸⢿⣶⣶⣦⠶⠋⡼⠟⠀⠀⡏⠉⣟⠻⣿⠿⣋⠁⠀⣿⣿⣮⣨⡾⣣⡼⠋⠀⠀⠀⠀
⢸⡇⠀⠀⣿⣿⢸⡻⣸⣿⡟⣭⢿⣿⡽⠄⠀⠀⠀⠀⠀⠀⠀⣠⣶⡀⠀⢻⣲⡦⣉⡋⠙⠏⠀⢸⠋⣞⣹⠗⠋⠁⠀⠀⠀⠀⠀⠀
⠘⣇⠀⠀⢿⣾⣯⣝⠮⢹⣇⠇⣷⡹⣧⠀⠀⠀⠀⢀⡠⠚⠀⠀⠈⠁⠀⠘⠉⠀⠀⠙⢦⠀⠀⢸⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⣆⠈⡪⠽⣿⣽⠶⠚⠻⣮⣙⠳⢿⡄⠀⠀⠀⠋⠀⠀⢀⣠⠤⠤⠤⠤⢄⣀⠀⠀⠈⠇⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⢶⣍⢻⠒⢺⠾⠩⠽⡇⣈⣙⣶⣷⡀⠀⠀⢀⡤⠚⠉⢀⣤⢴⢶⣤⣄⠉⠙⠲⢤⡀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠉⠋⠉⠉⠉⠉⠉⠀⠀⠀⠈⠻⣦⣀⡉⢀⡠⠞⠉⢠⠏⠘⡄⠻⡍⠲⢦⣤⠷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡶⣤⣤⣄⣀⣤⣥⣤⣶⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡏⠛⠿⢿⣿⣿⡿⣿⡃⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⠇⠀⠀⠀⠉⢻⣿⣿⣣⢿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣴⣶⣿⣿⣯⠀⠀⠀⠀⠀⠀⠘⠛⠋⠈⠋⠙⣿⣷⣦⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⣀⣼⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀
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
            user='remote_user',
            password='password',
            database='proj1'
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
            # host='localhost',
            host='10.5.34.66',
            user='remote_user',
            password='password',
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
    product_var.set(product_options[0])
    operation_var.set('Select operation')
    quantity_entry.delete(0, 'end')
    comments_entry.delete(0, 'end')

    # Close the cursor and connection
    cursor.close()
    connection.close()

def update_product_options(*args):
    selected_focus = focus_var.get()

    # Clear the current product options
    product_dropdown['menu'].delete(0, 'end')

    # Determine the product options based on the selected focus
    if selected_focus == 'TECH DATA':
        product_options = ['Bases', 'PCB', 'Nexeo', 'CU/TSP']
    elif selected_focus == 'REWORK DATA':
        product_options = ['Belt Packs', 'Headsets', '3M', 'Chargers', 'Sub Assys']
    else:
        product_options = []

    # Set the default option
    product_var.set(product_options[0])

    # Fetch font family and size from product_dropdown
    font = product_dropdown.cget('font')
    font_family = font.split(' ')[0]
    size = int(font.split(' ')[1])

    # Add the product options to the dropdown menu
    for option in product_options:
        product_dropdown['menu'].add_command(label=option, command=tk._setit(product_var, option), font=(font_family, size))

def update_operation_options(*args):
    selected_product = product_var.get()

    # Clear the current operation options
    operation_dropdown['menu'].delete(0, 'end')

    # Determine the operation options based on the selected product
    if selected_product == 'Bases':
        operation_options = ['BS6X00', 'BS6000', 'BS7X00', 'Console', 'Router', 'Pro Aud']
    elif selected_product == 'PCB':
        operation_options = ['PCBHS6', 'PRGPCBAIO', 'PCBAIO', 'PCBHS7', 'PCBCHG', 'PCBBSX', 'PCBIB7']
    elif selected_product == 'Nexeo':
        operation_options = ['RT7000', 'IB7000', 'SM7000']
    elif selected_product == 'CU/TSP':
        operation_options = ['CU TEST', 'CU50', 'TSP TEST', 'PCBTSP']
    elif selected_product == 'Belt Packs':
        operation_options = ['COM6000', 'COM6X00']
    elif selected_product == 'Headsets':
        operation_options = ['HS6000', 'AIO', 'WIRED', 'HS7000']
    elif selected_product == '3M':
        operation_options = ['3MG5 POD', '3MG5 BAND', '3MXT-1']
    elif selected_product == 'Chargers':
        operation_options = ['AC40', 'AC50', 'AC70']
    elif selected_product == 'Sub Assys':
        operation_options = ['MIC BOOM', '7000MB', 'DND7000', 'SUBAIO', 'DND AIO', 'DND HS6000']
    else:
        operation_options = []

    # Fetch font family and size from operation_dropdown
    font = operation_dropdown.cget('font')
    font_family = font.split(' ')[0]
    size = int(font.split(' ')[1])

    # Add the operation options to the dropdown menu
    for option in operation_options:
        operation_dropdown['menu'].add_command(label=option, command=tk._setit(operation_var, option), font=(font_family, size))


def calculate_productivity():
    quantity_entered = quantity_entry.get()
    hours_dedicated = hours_entry.get()
    selected_operation = operation_var.get()  # Assuming you have an entry field for operation name

    # List of product names and their UPH values
    operation_uph = {
        'BS6X00': 1.2,
        'BS6000': 0.6,
        'BS7X00': None,
        'Console': 1,
        'Router': 0.9,
        'Pro Aud': 0.4,
        'PCBHS6': 4,
        'PRGPCBAIO': 30,
        'PCBAIO': 7.5,
        'PCBHS7': None,
        'PCBCHG': 3.2,
        'PCBBSX': 1.3,
        'PCBIB7': 2.0,
        'RT7000': None,
        'IB7000': 2.5,
        'SM7000': None,
        'CU TEST': 4,
        'CU50': 4,
        'TSP TEST': 4,
        'PCBTSP': 4,
        'COM6000': 6,
        'COM6X00': 2.7,
        'HS6000': 3.6,
        'AIO': 6.7,
        'WIRED': 4.0,
        'HS7000': None,
        '3MG5 POD': 8,
        '3MG5 BAND': 6,
        '3MXT-1': 4,
        'AC40': 3,
        'AC50': 5.5,
        'AC70': 5.5,
        'MIC BOOM': 15,
        '7000MB': None,
        'DND7000': None,
        'SUBAIO': None,
        'DND AIO': None,
        'DND HS6000': None
    }
    uph_value = operation_uph[selected_operation]
    if uph_value is not None:
        hg = float(quantity_entered) * uph_value
        productivity = (hg / float(hours_dedicated)) * 100
        productivity = round(productivity, 2)
        return productivity,hg
    else:
        return "N/A","N/A"

# Create the main window
window = tk.Tk()
window.title('Data Entry Form')
window.geometry('950x400')
font_size = 20

# Check the database connection and show an error message if it fails
if not test_connection():
    # Send an email
    msg = MIMEMultipart()
    msg['From'] = 'mgibson@hme.com'
    msg['To'] = 'mgibson@hme.com'
    # msg['To'] = 'RepairLeadership@hme.com'
    msg['Subject'] = 'System Error'
    body = 'The system tried to make a connection to the server and was unable to. : ( no MySQL Server'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(msg['From'], 'Bicheal0!')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    #let the user know that they have an error and that the system is down
    messagebox.showerror('Pain', art)
    sys.exit()

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

# Focus
focus_label = tk.Label(window, text='Page:')
focus_label.grid(row=1, column=2, padx=10, pady=10, sticky='e')
increase_font_size(focus_label, font_size)

focus_options = ['TECH DATA', 'REWORK DATA']
focus_var = tk.StringVar(window)
focus_var.set(focus_options[0])
focus_dropdown = tk.OptionMenu(window, focus_var, *focus_options)
focus_dropdown.configure(fg='dark blue')
focus_dropdown.grid(row=1, column=3, padx=10, pady=10, sticky='w')
increase_font_size(focus_dropdown, font_size)

focus_var.trace_add('write', update_product_options)

# product
product_label = tk.Label(window, text='Product:')
product_label.grid(row=2, column=2, padx=10, pady=10, sticky='e')
increase_font_size(product_label, font_size)

product_options = ['Bases', 'PCB', 'Nexeo', 'CU/TSP']  # initial options
product_var = tk.StringVar(window)
product_var.set('Select Product')  # default option
product_dropdown = tk.OptionMenu(window, product_var, *product_options)
product_dropdown.configure(fg='dark blue')
product_dropdown.grid(row=2, column=3, padx=10, pady=10, sticky='w')
increase_font_size(product_dropdown, font_size)

product_var.trace_add('write', update_operation_options)

# Hours
hours_label = tk.Label(window, text='Hours:')
hours_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
increase_font_size(hours_label, font_size)

hours_entry = tk.Entry(window)
hours_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
increase_font_size(hours_entry, font_size)

# operation
operation_label = tk.Label(window, text='Operation:')
operation_label.grid(row=3, column=2, padx=10, pady=10, sticky='e')
increase_font_size(operation_label, font_size)

operation_var = tk.StringVar(window)
operation_var.set('Select Operation')  # default option
operation_dropdown = tk.OptionMenu(window, operation_var, '')  # no initial options
operation_dropdown.configure(fg='dark blue')
operation_dropdown.grid(row=3, column=3, padx=10, pady=10, sticky='w')
increase_font_size(operation_dropdown, font_size)


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

window.mainloop()