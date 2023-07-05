import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date
from datetime import time
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

def check_information(event=None):  # Added an optional event parameter to handle the key press event
    user_id = entry.get()

    cnx = mysql.connector.connect(
        host='10.5.34.66',
        user='remote_user',
        password='password',
        database='proj1'
    )

    cursor = cnx.cursor()
    current_date = date.today()

    query = f"SELECT Operation, Hours, Productivity, Comments FROM work_data WHERE `ID Number` = '{user_id}' AND Date = '{current_date}'"

    cursor.execute(query)
    result = cursor.fetchall()

    # Close the main Tkinter window
    root.destroy()

    if len(result) > 0:
        # find the longest entry
        longest_entry = max(result, key=lambda entry: len(str(entry)))
        longest_length = len(str(longest_entry))

        # base size and increase by length of longest entry
        result_window_width =  620 + longest_length * 6
        result_window_height = 350

        result_window = tk.Tk()
        result_window.title("Information")
        result_window.geometry(f"{result_window_width}x{result_window_height}")
        result_window.option_add("*Font", "Arial 20")

        headers = ["  OPERATION  ", "  HOURS  ", "  PRODUCTIVITY  ", "  COMMENTS  "]
        for i, header in enumerate(headers):
            tk.Label(result_window, text=header).grid(row=0, column=i)

        # Add separator after headers
        separator = tk.Label(result_window, text="", bg="grey")
        separator.grid(row=1, column=0, columnspan=4, sticky="we")

        for row, (operation, hours, productivity, comments) in enumerate(result, start=1):
            tk.Label(result_window, text=operation).grid(row=row * 2 + 1, column=0)
            tk.Label(result_window, text=hours).grid(row=row * 2 + 1, column=1)
            tk.Label(result_window, text=productivity).grid(row=row * 2 + 1, column=2)
            tk.Label(result_window, text=comments).grid(row=row * 2 + 1, column=3)

            # Add separator after each row of data
            separator = tk.Label(result_window, text="", bg="grey")
            separator.grid(row=row * 2 + 2, column=0, columnspan=4, sticky="we")

        result_window.mainloop()

    else:
        messagebox.showinfo("No Information", "No information found for the given user ID and current date.")

    cursor.close()
    cnx.close()

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
    messagebox.showerror('Error', 'Looks like the server is down. TUFF my b')
    sys.exit()
#Widgets / System layout

root = tk.Tk()
root.title("Check Information")
root.geometry("400x200")  # Increase the window size to accommodate the larger font
root.option_add("*Font", "Arial 30")  # Apply this font size to all widgets by default

tk.Label(root, text="Enter User ID:").pack()
entry = tk.Entry(root, font="Arial 30", justify='center')  # Set the font size for the entry field and justify to center
entry.pack()
entry.bind('<Return>', check_information)  # Bind the Return key to call check_information function

check_button = tk.Button(root, text="Check", command=check_information, font="Arial 20")  # Set the font size for the button
check_button.pack()

root.mainloop()
