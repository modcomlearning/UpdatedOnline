
from flask import *
# create a Flask app
app = Flask(__name__)
# __name__ means __main__ app
# database name    flickerdb
# Table name  Items
# User  root
# Host  localhost
# Password  empty

import pymysql
@app.route('/')
def home():
    # Step 1: connect to your database
    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='flickerdb')
    # Step 2: Create a cursor to execute SQL
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Items')

    # Step 3:  Get the rows from cursor
    rows = cursor.fetchall()

    # Step 4: Forward above rows to home.html to be displayed to users
    return render_template('home.html', rows = rows)


# We create /single route
# This will display a single product and its details
@app.route('/single/<id>')
def single(id):
    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='flickerdb')
    # Step 2: Create a cursor to execute SQL
    cursor = connection.cursor()
    # below %s is an id placeholder, means string
    cursor.execute('SELECT * FROM Items WHERE ProductID = %s ', (id))

    # Step 3:  Get the row returned from cursor
    row = cursor.fetchone()

    # Step 4: Forward above row to single.html to be displayed to users
    return render_template('single.html', row=row)



@app.route('/signup', methods= ['POST','GET'])
def signup():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        phone = request.form['phone']
        # above, we extracted the 4 inputs from the form
        if password != confirm:
            return render_template('signup.html', error='Passwords do not Match')

        elif len(password) < 8:
            return render_template('signup.html', error= 'Password must be 8 -xters')

        else:
            # we now save our email, password, phone
            connection = pymysql.connect(host='localhost', user='root', password='',
                                         database='NorthWind')

            cursor = connection.cursor()
            # create an insert query to insert data to shop_users
            cursor.execute('insert into shop_users(email,password,phone)values(%s,%s,%s)',
                           (email, password, phone))
            connection.commit() # write the record to the table
            return render_template('signup.html', success='Thank you for Registering.')

    else: # this shows the form if user is not posting
        return render_template('signup.html')














if __name__ == '__main__':
    app.run(debug=True)
















