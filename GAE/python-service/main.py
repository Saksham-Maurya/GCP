import os
import pymysql
from flask import Flask, render_template, request

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def getvalue():
    py_fname = request.form['firstname']
    py_lname = request.form['lastname']
    py_email = request.form['email']
    py_mobno = request.form['mobno']
    py_feedback = request.form['subject']
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)
    cursor = cnx.cursor()
    insquery = ("INSERT INTO customer (First_name, Last_name, Email, Mobile_no, Feedback) "
            "VALUES (%s, %s, %s, %s, %s)")
    val = (py_fname, py_lname, py_email, py_mobno, py_feedback)                         
    cursor.execute(insquery, val)
    cnx.commit()
    rowcnt = str(cursor.rowcount) + " record inserted successfully"
    cnx.close()
    return(rowcnt)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,debug=True)