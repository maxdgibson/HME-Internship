import os
import pymysql
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def export_and_clear():
    try:
        # establish connection to your mysql server
        connection = pymysql.connect(host='10.5.34.66',
                                    user='remote_user',
                                    password='password',
                                    database='proj1')

        # create a cursor object
        cursor = connection.cursor()

        # define columns
        columns = ['Date', 'Name', 'ID Number', 'Hours', 'Product', 'Operation',
                'Quantity', 'Productivity', 'Hours_Gained', 'Comments']

        # execute the SQL query
        cursor.execute("SELECT * FROM work_data")

        # fetch all rows from the last executed SQL statement
        data = cursor.fetchall()

        # create a pandas DataFrame from the MySQL data
        df_new = pd.DataFrame(data, columns=columns)

        # if the excel file already exists, read it, concatenate the new data, and write it back
        filename = r'C:\Users\mgibson\OneDrive - HM Electronics, Inc\Desktop\work_data.xlsx'
        if os.path.isfile(filename):
            df_old = pd.read_excel(filename)
            df_old['Date'] = pd.to_datetime(df_old['Date']).dt.date  # format 'Date' as date without time
            df_new = pd.concat([df_old, df_new])

        # write the DataFrame to an Excel file
        df_new.to_excel(filename, index=False)

        # clear the table
        cursor.execute("DELETE FROM work_data")

        # commit the transaction
        connection.commit()

        # Send an email
        msg = MIMEMultipart()
        msg['From'] = 'mgibson@hme.com'
        msg['To'] = 'mgibson@hme.com'
        #msg['To'] = 'RepairLeadership@hme.com'
        msg['Subject'] = 'End of Day Report'
        body = 'All data was exported and deleted for today!'
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(msg['From'], 'Bicheal0!')
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    except Exception as e:
        # Send an email
        msg = MIMEMultipart()
        msg['From'] = 'mgibson@hme.com'
        msg['To'] = 'mgibson@hme.com'
        # msg['To'] = 'RepairLeadership@hme.com'
        msg['Subject'] = 'Data Upload Error'
        body = 'The system tried to make a connection to the server and was unable to. : ( no MySQL Server'
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(msg['From'], 'Bicheal0!')
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

        ("Error occurred:", e)

    finally:
        # close the connection
        connection.close()

# run the function
export_and_clear()
