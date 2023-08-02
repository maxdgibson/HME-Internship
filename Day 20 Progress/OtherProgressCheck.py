import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date
from datetime import time
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

def test_connection():
    try:
        connection = mysql.connector.connect(
            host='10.5.34.39',
            user='remote_user',
            password='remoteuser',
            database='productivitytrack'
        )
        connection.close()
        return True
    except mysql.connector.Error as err:
        return False

def check_information(event=None):  # Added an optional event parameter to handle the key press event
    user_id = entry.get()

    # If the entry is empty or not an integer
    if not user_id or not user_id.isdigit():
        entry.delete(0, 'end')
        error_window = tk.Toplevel(root)
        error_window.geometry("400x100+130+255")  # Adjust window size and position
        error_label = tk.Label(error_window, text="Please Enter a Valid ID Number",
                               font=("Arial", 20))
        error_label.pack(pady=10)  # Add padding to vertically center the message

        ok_button = tk.Button(error_window, text="OK", font=("Arial", 20), command=error_window.destroy, height=10,
                              width=5, bg='light coral')
        ok_button.pack(pady=10)  # Add padding to vertically center the button

        return  # Stop the function here

    cnx = mysql.connector.connect(
        host='10.5.34.39',
        user='remote_user',
        password='remoteuser',
        database='productivitytrack'
    )

    cursor = cnx.cursor()
    current_date = date.today()

    query = f"SELECT Operation, Hours, Quantity, Productivity, Comments FROM work_data WHERE `ID Number` = '{user_id}' AND Date = '{current_date}'"

    cursor.execute(query)
    result = cursor.fetchall()

    # Close the main Tkinter window
    root.destroy()

    if len(result) > 0:
        # find the longest entry
        longest_entry = max(result, key=lambda entry: len(str(entry)))
        longest_length = len(str(longest_entry))

        # base size and increase by length of longest entry
        result_window_width = 775 + longest_length * 6
        result_window_height = 350

        result_window = tk.Tk()
        result_window.title("YOUR WORK TODAY FOR: " + user_id)
        result_window.geometry(f"{result_window_width}x{result_window_height}+0+200")
        result_window.option_add("*Font", "Arial 20")

        headers = ["  OPERATION  ", "  HOURS  ", "  QUANTITY  ", "  PRODUCTIVITY  ", "  COMMENTS  "]
        for i, header in enumerate(headers):
            tk.Label(result_window, text=header).grid(row=0, column=i)

        # Add separator after headers
        separator = tk.Label(result_window, text="", bg="grey")
        separator.grid(row=1, column=0, columnspan=5, sticky="we")

        for row, (operation, hours, quantity, productivity, comments) in enumerate(result, start=1):
            tk.Label(result_window, text=operation).grid(row=row * 2 + 1, column=0)
            tk.Label(result_window, text=hours).grid(row=row * 2 + 1, column=1)
            tk.Label(result_window, text=quantity).grid(row=row * 2 + 1, column=2)
            tk.Label(result_window, text=productivity).grid(row=row * 2 + 1, column=3)
            tk.Label(result_window, text=comments).grid(row=row * 2 + 1, column=4)  # display quantity

            # Add separator after each row of data
            separator = tk.Label(result_window, text="", bg="grey")
            separator.grid(row=row * 2 + 2, column=0, columnspan=5, sticky="we")

        result_window.mainloop()

    else:
        error_window = tk.Tk()
        error_window.title("                             " + user_id+ " No Information Found For " + user_id)
        error_window.geometry("500x100+0+200")  # Modify size and position here
        tk.Label(error_window, text="Nothing Today for ID Number: " + user_id, font=("Arial", 20)).pack()
        error_window.mainloop()

        sys.exit()

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
#Widgets / System layout
root = tk.Tk()
root.title("                                                    Enter User ID:")
root.geometry("450x200+0+200")  # Increase the window size to accommodate the larger font
root.option_add("*Font", "Arial 30")  # Apply this font size to all widgets by default

tk.Label(root, text="User ID Progress Check").pack()
entry = tk.Entry(root, font="Arial 30", justify='center')  # Set the font size for the entry field and justify to center
entry.pack()
entry.bind('<Return>', check_information)  # Bind the Return key to call check_information function

check_button = tk.Button(root, text="Check", command=check_information, font="Arial 20", bg='light green')  # Set the font size for the button
check_button.pack(pady=20)  # Added pady here

root.mainloop()