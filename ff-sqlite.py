import os
import sqlite3
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

print("Please select your Firefox cookies.sqlite file...")
source_db = filedialog.askopenfilename(
    title="Select cookies.sqlite",
    filetypes=[("SQLite Database", "*.sqlite"), ("All Files", "*.*")]
)

if not source_db:
    print("Error: No file selected. Exiting.")
    exit()

target_txt = os.path.join(os.getcwd(), "cookies.txt")

try:
    conn = sqlite3.connect(source_db)
    cursor = conn.cursor()

    cursor.execute("SELECT host, name, value, path, expiry FROM moz_cookies")
    rows = cursor.fetchall()

    with open(target_txt, "w", encoding="utf-8") as f:
        f.write(f"Total cookies found: {len(rows)}\n")
        f.write("=" * 60 + "\n\n")

        for row in rows:
            host, name, value, path, expiry = row
            f.write(f"Domain: {host}\n")
            f.write(f"Name: {name}\n")
            f.write(f"Value: {value}\n")
            f.write(f"Path: {path}\n")
            f.write(f"Expires (Timestamp): {expiry}\n")
            f.write("-" * 40 + "\n")

    print(f"Success! Data saved to:\n{target_txt}")

except sqlite3.OperationalError:
    print("Error: Could not open the database. Make sure Firefox is closed!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if "conn" in locals():
        conn.close()