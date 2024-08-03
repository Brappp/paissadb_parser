import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import requests
import pandas as pd
import os


DATABASE_PATH = 'housing.db'  
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
CSV_PATH = os.path.join(DOWNLOAD_DIR, 'housing.csv')
CSV_URL = 'https://paissadb.zhu.codes/csv/dump'

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# download the latest CSV 
def download_latest_csv():
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()  # Check if the request was successful
        
        with open(CSV_PATH, 'wb') as file:
            file.write(response.content)
        
        messagebox.showinfo("Download Complete", f"The latest CSV file has been downloaded to {CSV_PATH}.")
        load_csv_into_database()
    except requests.RequestException as e:
        messagebox.showerror("Download Error", str(e))

# Load the CSV data into the SQLite database
def load_csv_into_database():
    try:
        df = pd.read_csv(CSV_PATH)
        conn = sqlite3.connect(DATABASE_PATH)
        df.to_sql('housing', conn, if_exists='replace', index=False)
        conn.close()
        messagebox.showinfo("Database Updated", "The database has been updated with the latest CSV data.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def get_worlds_by_datacenter():
    return {
        "Aether": ["Adamantoise", "Cactuar", "Faerie", "Gilgamesh", "Jenova", "Midgardsormr", "Sargatanas", "Siren"],
        "Primal": ["Behemoth", "Excalibur", "Exodus", "Famfrit", "Hyperion", "Lamia", "Leviathan", "Ultros"],
        "Crystal": ["Balmung", "Brynhildr", "Coeurl", "Diabolos", "Goblin", "Malboro", "Mateus", "Zalera"],
        "Chaos": ["Cerberus", "Louisoix", "Moogle", "Omega", "Ragnarok", "Spriggan"],
        "Light": ["Lich", "Odin", "Phoenix", "Shiva", "Twintania", "Zodiark"],
        "Elemental": ["Aegis", "Atomos", "Carbuncle", "Garuda", "Gungnir", "Kujata", "Ramuh", "Tonberry", "Typhon", "Unicorn"],
        "Gaia": ["Alexander", "Bahamut", "Durandal", "Fenrir", "Ifrit", "Ridill", "Tiamat", "Ultima", "Valefor", "Yojimbo", "Zeromus"],
        "Mana": ["Anima", "Asura", "Chocobo", "Hades", "Ixion", "Mandragora", "Masamune", "Pandaemonium", "Shinryu", "Titan"],
        "Materia": ["Bismarck", "Ravana", "Sephirot", "Sophia", "Zurvan"]
    }

DATACENTERS = get_worlds_by_datacenter()
DISTRICTS = ["Mist", "The Goblet", "The Lavender Beds", "Empyreum", "Shirogane"]
WARDS = list(range(1, 31))  # Wards 1 to 30

world_var = {}

# Execute query
def execute_query():
    selected_worlds = [world for dc in DATACENTERS.values() for world in dc if world_var[world].get()]
    selected_districts = [district for district in DISTRICTS if district_var[district].get()]
    selected_ward = ward_var.get()
    days = days_var.get()
    is_owned = is_owned_var.get()
    
    if not selected_worlds or not selected_districts:
        messagebox.showerror("Selection Error", "Please select at least one world and one district.")
        return

    if not days.isdigit() or int(days) <= 0:
        messagebox.showerror("Input Error", "Please enter a valid number of days.")
        return
    
    days = int(days)

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Debugging output
        print(f"Selected worlds: {selected_worlds}")
        print(f"Selected districts: {selected_districts}")
        print(f"Selected ward: {selected_ward}")
        print(f"Days: {days}")
        print(f"Is Owned: {is_owned}")
    
        # Build the query
        query = """
        SELECT world, district, COUNT(*) as count
        FROM housing
        WHERE 
            world IN ({})
            AND district IN ({})
            AND ward_number < ?
            AND is_owned = ?
            AND last_seen >= strftime('%s', 'now') - ? * 24 * 60 * 60
        GROUP BY world, district
        ORDER BY world, district;
        """.format(
            ','.join(['?'] * len(selected_worlds)),
            ','.join(['?'] * len(selected_districts))
        )
    
        parameters = selected_worlds + selected_districts + [selected_ward, is_owned, days]

        # Debugging output
        print(f"SQL Query: {query}")
        print(f"Parameters: {parameters}")
    
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        conn.close()

        # Debugging output
        print(f"Query results: {results}")
        
        # Display the results
        result_text.delete('1.0', tk.END)
        for row in results:
            result_text.insert(tk.END, f"World: {row[0]}, District: {row[1]}, Count: {row[2]}\n")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

root = tk.Tk()
root.title("FFXIV Housing Query")

# World selection by data center
for dc, worlds in DATACENTERS.items():
    dc_frame = ttk.LabelFrame(root, text=f"Select Worlds ({dc})")
    dc_frame.pack(fill="x", padx=5, pady=5)
    
    for world in worlds:
        world_var[world] = tk.BooleanVar()
        ttk.Checkbutton(dc_frame, text=world, variable=world_var[world]).pack(side="left", padx=5, pady=5)

# District selection
district_frame = ttk.LabelFrame(root, text="Select Districts")
district_frame.pack(fill="x", padx=5, pady=5)

district_var = {district: tk.BooleanVar() for district in DISTRICTS}
for district in DISTRICTS:
    ttk.Checkbutton(district_frame, text=district, variable=district_var[district]).pack(side="left", padx=5, pady=5)

# Ward selection
ward_frame = ttk.LabelFrame(root, text="Select Ward Number")
ward_frame.pack(fill="x", padx=5, pady=5)

ward_var = tk.IntVar(value=WARDS[0])
ward_menu = ttk.OptionMenu(ward_frame, ward_var, WARDS[0], *WARDS)
ward_menu.pack(padx=5, pady=5)

# Days input
days_frame = ttk.LabelFrame(root, text="Number of Days")
days_frame.pack(fill="x", padx=5, pady=5)

days_var = tk.StringVar(value="30")
days_entry = ttk.Entry(days_frame, textvariable=days_var)
days_entry.pack(padx=5, pady=5)

# Is Owned input
is_owned_frame = ttk.LabelFrame(root, text="Is Owned")
is_owned_frame.pack(fill="x", padx=5, pady=5)

is_owned_var = tk.IntVar(value=0)
is_owned_menu = ttk.OptionMenu(is_owned_frame, is_owned_var, 0, 0, 1)
is_owned_menu.pack(padx=5, pady=5)

# Download button
download_button = ttk.Button(root, text="Download Latest CSV", command=download_latest_csv)
download_button.pack(padx=5, pady=5)

# Execute button
execute_button = ttk.Button(root, text="Execute Query", command=execute_query)
execute_button.pack(padx=5, pady=5)

# Result display
result_frame = ttk.LabelFrame(root, text="Query Results")
result_frame.pack(fill="both", expand=True, padx=5, pady=5)

result_text = tk.Text(result_frame, height=10)
result_text.pack(fill="both", expand=True, padx=5, pady=5)

# Start the main event loop
root.mainloop()
