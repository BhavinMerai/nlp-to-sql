Overview
This project is designed to demonstrate a QnA system for generating SQL queries based on natural language questions. The system utilizes a pre-trained T5 model for text-to-SQL conversion and interacts with a PostgreSQL database containing stock market data (NIFTY 50 and NIFTY BANK).

Files
main.py: The main entry point for the application. It reads stock market data from CSV files, sets up a PostgreSQL database, creates tables, inserts sample data, and launches a Streamlit app for user interaction.
utils.py: Contains utility functions and classes used in the project.
app.py: Implements a Streamlit app for user interaction. Users can input a natural language question, and the app generates an SQL query, executes it on the database, and displays the result.

Dependencies
Python 3.x
PostgreSQL
psycopg2: PostgreSQL adapter for Python
pandas: Data manipulation library
streamlit: Web app framework
transformers: Library for state-of-the-art natural language processing
Setup
Install dependencies:
bash
Copy code
pip install psycopg2 pandas streamlit transformers
Set up a PostgreSQL database and configure the connection parameters in main.py:

python
Copy code
# Database configuration
DB_NAME = "nifty"
DB_USER = "postgres"
DB_PASSWORD = "admin"
Run the main script to initialize the database, create tables, insert sample data, and launch the Streamlit app:

bash
Copy code
python main.py
Usage
Input a natural language question in the provided text box.

Click the "Ask the question" button to generate an SQL query.

The generated SQL query and the result will be displayed on the Streamlit app.

Notes
The application uses a pre-trained T5 model (juierror/flan-t5-text2sql-with-schema-v2) for text-to-SQL conversion. Make sure the model is available and properly configured in the TextToSQLConverter class.

Adjust file paths in main.py to point to the actual location of your CSV files.

Ensure that PostgreSQL is installed and running, and the connection details in main.py are accurate.

The sample data provided is limited to the first 10 records for both NIFTY 50 and NIFTY BANK for demonstration purposes. Modify the code as needed for your use case.