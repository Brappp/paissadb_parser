# FFXIV Housing Query Tool

This script provides a GUI tool to query Final Fantasy XIV housing data. Key features include:

1. **Download Latest CSV:**
   - Downloads the latest housing data CSV from a specified URL.
   - Saves the CSV to a local directory.

2. **Load CSV into Database:**
   - Reads the downloaded CSV using pandas.
   - Loads the data into an SQLite database.

3. **Execute Query:**
   - Allows users to select worlds, districts, ward numbers, and other parameters.
   - Executes SQL queries on the database based on user selections.
   - Displays results in the GUI.

4. **GUI:**
   - Built using tkinter and ttk.
   - Provides interactive elements for parameter selection and displays query results.

**Usage:**
- Run the script to open the GUI.
- Download the latest CSV and load it into the database.
- Select query parameters and execute the query to view results.



## Setup Guide

1. **Install Python:**
   - python 3x

2. **Install Required Libraries:**
   - Install the required Python libraries using pip:
     ```sh
     pip install tkinter pandas requests
     ```

3. **Run the Script:**
   - Save the script to a file, for example, `ffxiv_housing_query.py`.
   - Open a terminal or command prompt.
   - Navigate to the directory where the script is saved.
   - Run the script with:
     ```sh
     python ffxiv_housing_query.py
     ```

4. **Using the Tool:**
   - The GUI will open.
   - Click "Download Latest CSV" to download and load the latest housing data.
   - Select your query parameters (worlds, districts, wards, etc.).
   - Click "Execute Query" to display the results.

