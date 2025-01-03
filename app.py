import mysql.connector
import os
import re
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

app.secret_key = os.urandom(24)  # Necessary for flash messages

# Set up MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Use your MySQL username
        password='Dart@SQL',  # Use your MySQL password
        database='airline_booking'  # Use your database name
    )


@app.route('/about')
def about():
    return render_template('about.html')

def is_valid_password(password):
    # Password must have at least one uppercase letter, one lowercase letter, one number, and be at least 8 characters long
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
    
    if re.match(pattern, password):
        return True
    return False

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate the password
        if not is_valid_password(password):
            flash('Password does not satify the necessary conditions', 'error')
            return render_template('signup.html')

        # Check if the username already exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            # If username doesn't exist, hash the password and store in the database
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))

        cursor.close()
        conn.close()

    return render_template('signup.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            flash('Username does not exist.', 'error')
        elif not check_password_hash(user[2], password):  # user[2] is the hashed password
            flash('Incorrect password. Please try again.', 'error')
        else:
            # If login is successful, store username in session
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('welcome'))  # Redirect to welcome page


    return render_template('login.html')

@app.route('/welcome')

def welcome():
    # Check if the 'username' exists in session (i.e., the user is logged in)
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('login'))  # Redirect to login if not logged in


@app.route('/logout')
def logout():
    session.pop('username', None)   # Remove username from session
    session.clear()  
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/book_ticket')
def book_ticket():
    return render_template('book_ticket.html')


@app.route('/search_flights', methods=['POST'])
def search_flights():
    # Get form data
    departure_city = request.form.get('departure-city')
    arrival_city = request.form.get('arrival-city')
    departure_date = request.form.get('departure-date')  # Ensure the date format is consistent

    print(departure_city, arrival_city, departure_date)
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query the database for flights matching the criteria
    query = """
    SELECT * FROM flights
    WHERE departure_airport_iata = %s
    AND arrival_airport_iata = %s
    AND departure_date = %s
    """

    cursor.execute(query, (departure_city, arrival_city, departure_date))
    flights = cursor.fetchall()

    # Process the results and convert timedelta objects to serializable format
    for flight in flights:
        if isinstance(flight['departure_time'], timedelta):
            flight['departure_time'] = flight['departure_time'].total_seconds()  # Convert to total seconds
        if isinstance(flight['arrival_time'], timedelta):
            flight['arrival_time'] = flight['arrival_time'].total_seconds()  # Convert to total seconds
        if isinstance(flight['duration'], timedelta):
            flight['duration'] = flight['duration'].total_seconds()  # Convert to total seconds

    # Check if any results were returned
    if not flights:
        print("No flights found matching the criteria.")
    else:
        print("Flights found:", flights)
        return jsonify(flights)

    cursor.close()
    conn.close() 

@app.route('/airline_details/<string:airline_id>')
def get_airline_details(airline_id):
    print(f"Requested airline_id: {airline_id}")
    conn = get_db_connection()  # Use your database connection function
    cursor = conn.cursor(dictionary=True)

    # Query flight details using airline_id
    query = "SELECT * FROM flights WHERE airline_id = %s"
    cursor.execute(query, (airline_id,))
    airline = cursor.fetchone()
    conn.close()

    # If no airline is found
    if not airline:
        return "Airline not found", 404

    return render_template('airline_details.html', flight=airline)

@app.route('/book/<string:airline_id>', methods=['GET', 'POST'])
def user_details(airline_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM flights WHERE airline_id = %s", (airline_id,))
    flight = cursor.fetchone()

    if request.method == 'POST':
        username = session.get('username')  # Get username from session
        full_name = request.form['full_name']
        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']
        aadhar = request.form['aadhar']
        passport = request.form['passport']
        pan = request.form['pan']

        insert_query = """
        INSERT INTO details (username, full_name, age, mobile, email, aadhar, passport_number, pan_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (username, full_name, age, mobile, email, aadhar, passport, pan)
        try:
            cursor.execute(insert_query, values)
            conn.commit()
            flash('Details submitted successfully!', 'success')
            return redirect('/payment')
        except Exception as e:
            conn.rollback()
            flash(f"An error occurred: {e}", 'error')

    cursor.close()
    conn.close()
    return render_template('user_details.html', flight=flight)

@app.route('/submit-details', methods=['POST'])
def submit_details():

    username = request.form['username']
    name = request.form['name']
    age = request.form['age']
    mobile = request.form['mobile']
    email = request.form['email']
    aadhar = request.form['aadhar']
    passport = request.form['passport']
    pan = request.form['pan']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the user details into the 'details' table
    query = """
    INSERT INTO details (username, name, age, mobile, email, aadhar, passport, pan)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (username, name, age, mobile, email, aadhar, passport, pan))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect to the booking page after successful insertion
    return render_template('payment.html')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Simulate payment processing
        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        amount = request.form.get('amount')

        if card_number and len(card_number) == 16 and cvv and len(cvv) == 3:
            flash("Payment Successful! Thank you for booking with SkyDart.", "success")
            return redirect(url_for('success'))  # Redirect to the success page
        else:
            flash("Payment Failed. Please check your card details.", "error")
            return redirect(url_for('payment'))  # Redirect back to payment page

    return render_template('payment.html')

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')



if __name__ == '__main__':
    app.run(debug=True)
