import os
import csv
from tkinter import messagebox

from config import DEFAULT_SAMPLES_DIR, DB_FILES, DEFAULT_COLLEGES, DEFAULT_PROGRAMS, DEFAULT_STUDENTS


def initialize_database():
    """Initializes local CSV files if they do not exist."""
    os.makedirs(DEFAULT_SAMPLES_DIR, exist_ok=True)
    for key, filepath in DB_FILES.items():
        if not os.path.exists(filepath):
            if key == 'colleges':
                save_data(filepath, ['code', 'name'], DEFAULT_COLLEGES)
            elif key == 'programs':
                save_data(filepath, ['code', 'name', 'collegeCode'], DEFAULT_PROGRAMS)
            elif key == 'students':
                save_data(filepath, ['id', 'firstname', 'lastname', 'programCode', 'year', 'gender'], DEFAULT_STUDENTS)


def load_data(filename):
    """Loads CSV data into a list of dictionaries."""
    data = []
    if not os.path.exists(filename):
        return data

    try:
        with open(filename, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if any(row.values()):
                    data.append(dict(row))
    except Exception as exc:
        print(f"Error reading database file {filename}: {exc}")
    return data


def save_data(filename, headers, rows):
    """Writes list of dictionaries to a CSV file."""
    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: row.get(k, '') for k in headers})
    except Exception as exc:
        messagebox.showerror("Database Save Error", f"Failed to save to {filename}:\n{exc}")
