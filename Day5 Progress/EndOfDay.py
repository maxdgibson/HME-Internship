import pymysql
import pandas as pd


def export_and_clear():
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
    df = pd.DataFrame(data, columns=columns)

    # write the DataFrame to an Excel file
    df.to_excel('work_data.xlsx', index=False)

    # clear the table
    cursor.execute("DELETE FROM work_data")

    # commit the transaction
    connection.commit()

    # close the connection
    connection.close()


# run the function
export_and_clear()