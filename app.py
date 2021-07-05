
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



# create a signin route
@app.route('/signin',  methods= ['POST','GET'])
def signin():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='NorthWind')

        cursor = connection.cursor()

        cursor.execute('select * from shop_users where email = %s and password = %s',
                       (email, password))
        # check if above query found a match or not
        if cursor.rowcount == 0:
            return render_template('signin.html', error = 'Wrong Credentials')

        else:
            return redirect('/')

    else:
        return render_template('signin.html')





# here below login
# you can go to View - Tool Windows - Terminal
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth


@app.route('/mpesa_payment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return render_template('mpesa_payment.html', msg='Please Complete Payment in Your Phone')
    else:
        return render_template('mpesa_payment.html', total_amount=total_amount)







if __name__ == '__main__':
    app.run(debug=True)
















