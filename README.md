
# Airline Booking System

This is an Airline Booking System built with **Flask**, designed to help users search for available flights and book tickets. The project includes a simple web interface with a search functionality, where users can select cities, dates, and view flight details.

## Features
- **Search Flights**: Users can search for flights by selecting the departure and arrival cities, as well as the travel date.
- **Flight Details**: Displays flight information such as airline name, departure and arrival times, price, and duration.
- **User Interface**: The interface includes a user-friendly form to select cities and dates, powered by **Select2** for dropdowns.
  
## Project Structure
Airline Booking/<br/>
│<br/>
├── app.py # Main Flask application file<br/>
├── static/ # Static files (CSS, JS, images)<br/>
│ └── images/ # Folder for images<br/>
├── templates/ # HTML templates<br/> 
│ └── ... # Your HTML files<br/>
├── requirements.txt # List of Python dependencies<br/>
└── README.md # Project overview<br/>


## Steps to Run the Airline Booking Project
### **1. Clone the Repository**

- Open a terminal and run the following commands:
  ```bash
  git clone https://github.com/yourusername/DevDart.git
  cd DevDart
  ```

### **2. Install Python**

- Ensure Python 3.x is installed on their system.
- Verify the installation by running:
  ```bash
  python --version
  ```

### **3. Set Up a Virtual Environment (Optional but Recommended)**

- Create a virtual environment:
  ```bash
  python -m venv venv
  ```
- Activate the virtual environment:
  - On Windows:
    ```bash
    venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

### **4. Install Dependencies**

- Install the required Python libraries:
  ```bash
  pip install -r requirements.txt
  ```

### **5. Set Up the Database**

- Install MySQL if not already installed.
- Open MySQL and execute the following commands:
  ```sql
  CREATE DATABASE airline_booking;
  ```
- Set up the `flights` table by running:
  ```sql
  CREATE TABLE flights (
      airline_id INT AUTO_INCREMENT PRIMARY KEY,
      airline_name VARCHAR(255),
      departure_airport_iata VARCHAR(3),
      departure_city VARCHAR(255),
      arrival_airport_iata VARCHAR(3),
      arrival_city VARCHAR(255),
      departure_date DATE,
      departure_time TIME,
      arrival_date DATE,
      arrival_time TIME,
      duration TIME,
      price DECIMAL(10, 2)
  );
  ```
- Update the `app.py` file with the appropriate MySQL credentials:
  ```python
  db = mysql.connector.connect(
      host="localhost",
      user="your_username",
      password="your_password",
      database="airline_booking"
  )
  ```

### **6. Run the Application**

- Start the Flask development server:
  ```bash
  python app.py
  ```
- Open a browser and navigate to:
  ```
  http://127.0.0.1:5000/
  ```

---

## Contributing
If you'd like to contribute to this project:

- Fork the repository.
- Create a new branch (git checkout -b feature-name).
- Make your changes and commit them (git commit -am 'Add feature').
- Push to your branch (git push origin feature-name).
- Open a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
Pathmhajam 
(Git : DART-0050)
