# Simple Student Information System (SSIS)

A standalone, modern, and high-performance **Student Information System** desktop application built with **Python 3** and **Tkinter**, using raw **CSV** flat files as the primary persistent database.

This application is customized for student requirements at **MSU-IIT (Mindanao State University - Iligan Institute of Technology)**, providing full CRUDL (Create, Read, Update, Delete, List) capabilities.

---

## ⚡ 1-Click Standalone Desktop Launch (Zero Setup!)

Since **Node.js, NPM, Vite, React, and local web servers are forbidden**, this application runs as a **native standalone desktop window** on your computer. It requires **zero installation of third-party modules** (it uses Python's built-in `tkinter` and `csv` library!).

### Option A: The 1-Click Launcher (Windows)
1. Double-click the **`run.bat`** file located in the folder.
2. It will check if Python is installed, verify your files, and immediately open the database system in a standalone GUI window!

### Option B: Run via VS Code Terminal
1. Open VS Code in this directory.
2. Open your terminal (`Ctrl + ` `) and run:
   ```bash
   python ssis.py
   ```

---

## 📂 Database & CSV Structure

The system reads and writes to local CSV database files in real-time. On first launch, the program will look for the CSV templates in your directory. If they don't exist, it will auto-populate them in your root directory from the defaults:

*   **`colleges.csv`**: Contains College items (`code,name`)
*   **`programs.csv`**: Contains academic degree courses (`code,name,collegeCode`)
*   **`students.csv`**: Contains student records (`id,firstname,lastname,programCode,year,gender`)

---

## 🎨 Professional Key Features

1.  **Strict Integrity Rules (Referential Constraints)**:
    *   **Student ID Format**: Validated securely using Regex (`YYYY-NNNN` format. e.g. `2021-0001`). No misformatted IDs allowed!
    *   **Program Constraint**: You cannot save a student to a program code that doesn't exist.
    *   **College Constraint**: You cannot save a program into a college code that doesn't exist.
    *   **Delete Cascase Protection**: 
        *   You cannot delete a program if active students are enrolled in it.
        *   You cannot delete a college if academic programs are registered under it.
2.  **Live Search (Filtered Type)**:
    *   As you type in the text form, your table filters records instantly! You can filter by "All Fields" or select a specific column (e.g. Student ID, College, Gender).
3.  **Interactive Column-Click Sorting**:
    *   Click on any column heading (e.g., Name, ID, Year) to sort all entries dynamically in ascending or descending order.
4.  **IIT Colors Branding**:
    *   Styled with professional IIT deep maroon (`#800000`) accents, alternating list highlights, flat controls, and clear feedback alerts.
