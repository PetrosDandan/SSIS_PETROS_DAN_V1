#!/usr/bin/env python3
"""
Simple Student Information System (SSIS)
Built for MSU-IIT (Mindanao State University - Iligan Institute of Technology) course CCC151.
A lightweight, modern, offline-first Python desktop application using Tkinter and CSV databases.
"""

import os
import re
import csv
import shutil
import tkinter as tk
from tkinter import ttk, messagebox

# --- CONFIGURATION & DATABASE CONSTANTS ---
# Store samples inside public/samples and use them directly to avoid duplicate copies
DEFAULT_SAMPLES_DIR = os.path.join('public', 'samples')

DB_FILES = {
    'colleges': os.path.join(DEFAULT_SAMPLES_DIR, 'colleges.csv'),
    'programs': os.path.join(DEFAULT_SAMPLES_DIR, 'programs.csv'),
    'students': os.path.join(DEFAULT_SAMPLES_DIR, 'students.csv')
}

DEFAULT_COLLEGES = [
    {"code": "CCS", "name": "College of Computer Studies"},
    {"code": "COE", "name": "College of Engineering"},
    {"code": "CEBA", "name": "College of Economics, Business and Accountancy"},
    {"code": "CHS", "name": "College of Health Sciences"},
    {"code": "CED", "name": "College of Education"},
    {"code": "CASS", "name": "College of Arts and Social Sciences"}
]

DEFAULT_PROGRAMS = [
    {"code": "BSCS", "name": "BS Computer Science", "collegeCode": "CCS"},
    {"code": "BSIT", "name": "BS Information Technology", "collegeCode": "CCS"},
    {"code": "BSCE", "name": "BS Civil Engineering", "collegeCode": "COE"},
    {"code": "BSBA", "name": "BS Business Administration", "collegeCode": "CEBA"},
    {"code": "BSN", "name": "BS Nursing", "collegeCode": "CHS"},
    {"code": "BSED", "name": "BS Education", "collegeCode": "CED"},
    {"code": "AB-EL", "name": "AB English Language", "collegeCode": "CASS"}
]

DEFAULT_STUDENTS = [
    {"id": "2021-0001", "firstname": "Juan", "lastname": "Dela Cruz", "programCode": "BSCS", "year": "3", "gender": "Male"},
    {"id": "2022-0042", "firstname": "Maria", "lastname": "Santos", "programCode": "BSIT", "year": "2", "gender": "Female"},
    {"id": "2020-0123", "firstname": "Jose", "lastname": "Reyes", "programCode": "BSCE", "year": "4", "gender": "Male"},
    {"id": "2023-0005", "firstname": "Ana", "lastname": "Garcia", "programCode": "BSBA", "year": "1", "gender": "Female"},
    {"id": "2021-0999", "firstname": "Antonio", "lastname": "Luna", "programCode": "BSN", "year": "3", "gender": "Male"}
]


# --- DATABASE OPERATIONS ---
def initialize_database():
    """Initializes local CSV files if they do not exist in the working directory."""
    # Ensure samples directory exists and create missing sample CSVs from defaults
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
            # Filter empty lines
            for row in reader:
                if any(row.values()):
                    data.append(dict(row))
    except Exception as e:
        print(f"Error reading database file {filename}: {e}")
    return data


def save_data(filename, headers, rows):
    """Writes list of dictionaries to a CSV file."""
    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for r in rows:
                # Keep only valid headers keys
                writer.writerow({k: r.get(k, '') for k in headers})
    except Exception as e:
        messagebox.showerror("Database Save Error", f"Failed to save to {filename}:\n{e}")


# --- MAIN APPLICATION FRAMEWORK ---
class SSISApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Initialize database files
        initialize_database()

        # Window Branding & Configuration
        self.title("Simple Student Information System (SSIS)")
        self.geometry("1024x680")
        self.minimum_width = 850
        self.minimum_height = 550
        self.minsize(self.minimum_width, self.minimum_height)
        
        # Applet Active States
        self.current_view = 'students'  # 'students' | 'programs' | 'colleges'
        self.search_field = 'all'
        self.sort_field = None
        self.sort_direction = True  # True = Ascending, False = Descending

        # Apply Visual Hierarchy Colors & Custom UI Aesthetics
        self.brand_red = "#800000"       # Institutional Maroon
        self.brand_red_hover = "#600000" # Institutional Dark Maroon
        self.bg_light = "#f8f9fa"        # Soft White Canvas
        self.border_gray = "#e2e8f0"     # Light borders
        self.text_dark = "#1e293b"       # Charcoal black
        self.text_muted = "#64748b"      # Muted gray

        self.setup_styles()
        self.build_ui()
        self.load_active_view_data()

    def setup_styles(self):
        """Sets up high-quality, professional styling guidelines."""
        self.configure(bg=self.bg_light)
        
        # Configure standard Treeview themes
        style = ttk.Style()
        style.theme_use('clam')
        
        # Treeview formatting
        style.configure("Treeview", 
                        background="#ffffff", 
                        foreground=self.text_dark, 
                        rowheight=28, 
                        fieldbackground="#ffffff",
                        font=("Segoe UI", 10))
        
        style.map("Treeview", 
                  background=[('selected', self.brand_red)], 
                  foreground=[('selected', '#ffffff')])
        
        # Treeview Headings theme
        style.configure("Treeview.Heading", 
                        background="#f1f5f9", 
                        foreground="#475569", 
                        padding=8, 
                        font=("Segoe UI", 9, "bold"),
                        borderwidth=0)
        
        style.map("Treeview.Heading", 
                  background=[('active', '#e2e8f0')],
                  foreground=[('active', '#0f172a')])

        # Scrollbar formatting
        style.configure("Vertical.TScrollbar", gripcount=0, background="#cbd5e1", bordercolor="#f8f9fa", troughcolor="#f8f9fa")
        style.configure("Horizontal.TScrollbar", gripcount=0, background="#cbd5e1", bordercolor="#f8f9fa", troughcolor="#f8f9fa")

    def build_ui(self):
        """Builds a cohesive single-screen layout with spacious margins and clear tabs."""
        # Clean Header Frame
        header = tk.Frame(self, bg=self.brand_red, height=75)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="STUDENT INFORMATION SYSTEM (SSIS)", 
                               font=("Segoe UI", 15, "bold"), fg="#ffffff", bg=self.brand_red)
        title_label.pack(anchor=tk.W, padx=24, pady=(13, 0))
        
        subtitle_label = tk.Label(header, text="Academic Database Launcher", 
                                  font=("Segoe UI", 9), fg="#fbcfe8", bg=self.brand_red)
        subtitle_label.pack(anchor=tk.W, padx=24, pady=(0, 10))

        # Main Body Layout
        body = tk.Frame(self, bg=self.bg_light)
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)
        
        # --- TAB NAVIGATION BAR ---
        nav_frame = tk.Frame(body, bg=self.bg_light)
        nav_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 16))
        
        self.nav_btns = {}
        for view_key, label in [('students', 'Students Database'), ('programs', 'Programs Database'), ('colleges', 'Colleges Directory')]:
            btn = tk.Button(nav_frame, text=label, font=("Segoe UI", 10, "bold"), 
                            bd=0, activebackground=self.border_gray, cursor="hand2", padx=20, pady=8)
            btn.pack(side=tk.LEFT, padx=(0, 6))
            btn.config(command=lambda k=view_key: self.switch_view(k))
            self.nav_btns[view_key] = btn

        # --- CONTROLS COMPONENT TRAY ---
        controls_card = tk.LabelFrame(body, bg="#ffffff", bd=1, relief=tk.SOLID, highlightthickness=0)
        controls_card.config(highlightbackground=self.border_gray, fg=self.text_muted)
        controls_card.pack(fill=tk.X, side=tk.TOP, ipady=12, ipadx=10, pady=(0, 16))
        
        # Left Side search controls inside Card UI
        search_container = tk.Frame(controls_card, bg="#ffffff")
        search_container.pack(side=tk.LEFT, padx=16, pady=4)
        
        tk.Label(search_container, text="Search Field:", font=("Segoe UI", 9, "bold"), fg=self.text_dark, bg="#ffffff").pack(side=tk.LEFT, padx=(0, 6))
        self.search_col_combo = ttk.Combobox(search_container, state="readonly", font=("Segoe UI", 9), width=15)
        self.search_col_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.search_col_combo.bind("<<ComboboxSelected>>", self.on_search_field_change)

        tk.Label(search_container, text="Query:", font=("Segoe UI", 9, "bold"), fg=self.text_dark, bg="#ffffff").pack(side=tk.LEFT, padx=(0, 6))
        
        # Clean Search Entry
        self.search_val_var = tk.StringVar()
        self.search_entry = tk.Entry(search_container, textvariable=self.search_val_var, 
                                     font=("Segoe UI", 10), bg="#f1f5f9", relief=tk.FLAT, bd=0, width=28)
        self.search_entry.pack(side=tk.LEFT, ipady=5, ipadx=6)
        self.search_val_var.trace_add("write", lambda *args: self.filter_data())
        
        # Clear Query Button Action
        self.btn_clear_search = tk.Button(search_container, text="Clear", font=("Segoe UI", 8, "bold"),
                                          bg="#e2e8f0", fg=self.text_dark, activebackground="#cbd5e1", bd=0, cursor="hand2")
        self.btn_clear_search.pack(side=tk.LEFT, padx=8, ipady=2, ipadx=8)
        self.btn_clear_search.config(command=self.clear_search_field)

        # Right Side Action triggers inside control frame
        actions_container = tk.Frame(controls_card, bg="#ffffff")
        actions_container.pack(side=tk.RIGHT, padx=16, pady=4)
        
        self.btn_add = tk.Button(actions_container, text="+ Add Record", font=("Segoe UI", 9, "bold"),
                                 bg=self.brand_red, fg="#ffffff", activebackground=self.brand_red_hover, 
                                 activeforeground="#ffffff", bd=0, cursor="hand2")
        self.btn_add.config(command=self.open_add_dialog, padx=14, pady=5)
        self.btn_add.pack(side=tk.RIGHT, padx=4)

        # --- DATA CANVAS & TREEVIEW STORAGE CONTAINER ---
        table_container = tk.Frame(body, bg="#ffffff", bd=1, relief=tk.SOLID, highlightthickness=0)
        table_container.config(highlightbackground=self.border_gray)
        table_container.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=(0, 16))

        # Vertical / Horizontal Grid scrolling 
        v_scroll = ttk.Scrollbar(table_container, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(table_container, columns=(), show="headings", 
                                 yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)
        
        v_scroll.pack(fill=tk.Y, side=tk.RIGHT)
        h_scroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Double click to edit selected record easily
        self.tree.bind("<Double-1>", lambda event: self.open_edit_dialog())

        # --- BOTTOM RECORD CRUD CONTROLS ACTION PANEL ---
        bottom_panel = tk.Frame(body, bg=self.bg_light)
        bottom_panel.pack(fill=tk.X, side=tk.TOP)
        
        # Left action modifiers
        left_ops = tk.Frame(bottom_panel, bg=self.bg_light)
        left_ops.pack(side=tk.LEFT)

        self.btn_edit = tk.Button(left_ops, text="Edit Details", font=("Segoe UI", 9, "bold"),
                                  bg="#ffffff", fg=self.text_dark, activebackground="#f1f5f9", 
                                  relief=tk.SOLID, bd=1, cursor="hand2")
        self.btn_edit.config(command=self.open_edit_dialog, padx=14, pady=6)
        self.btn_edit.grid(row=0, column=0, padx=4)

        self.btn_delete = tk.Button(left_ops, text="Delete Record", font=("Segoe UI", 9, "bold"),
                                    bg="#fecdd3", fg="#be123c", activebackground="#fca5a5", 
                                    relief=tk.SOLID, bd=1, cursor="hand2")
        self.btn_delete.config(command=self.delete_selected_record, padx=14, pady=6)
        self.btn_delete.grid(row=0, column=1, padx=4)

        # Right control restore reset 
        right_ops = tk.Frame(bottom_panel, bg=self.bg_light)
        right_ops.pack(side=tk.RIGHT)

        self.btn_reset = tk.Button(right_ops, text="Reset to CSV defaults", font=("Segoe UI", 9, "bold"),
                                   bg="#ffffff", fg=self.text_dark, activebackground="#f1f5f9", 
                                   relief=tk.SOLID, bd=1, cursor="hand2")
        self.btn_reset.config(command=self.reset_database_to_csv, padx=14, pady=6)
        self.btn_reset.grid(row=0, column=0, padx=4)

        # Initial Nav Highlights Styling
        self.update_nav_tabs()

    # --- VIEW SWITCHER & SEARCH RE-POPULATOR ---
    def switch_view(self, key):
        """Swaps active table, updates search fields, reset sorts, and load records."""
        if self.current_view == key:
            return
        self.current_view = key
        self.sort_field = None
        self.sort_direction = True
        self.search_field = 'all'
        self.search_val_var.set('')
        
        self.update_nav_tabs()
        self.load_active_view_data()

    def update_nav_tabs(self):
        """Applies dynamic high-contrast highlighted design tabs to reflect current view State."""
        for key, btn in self.nav_btns.items():
            if key == self.current_view:
                btn.config(bg=self.brand_red, fg="#ffffff", activebackground=self.brand_red, relief=tk.FLAT)
            else:
                btn.config(bg="#ffffff", fg=self.text_dark, activebackground="#f1f5f9", relief=tk.SOLID, bd=1)

    def load_active_view_data(self):
        """Compiles structure headers, sets sorting functions, loads active view CSV data."""
        # Setup table headers depending on tab Selection. Add interactive sort triggers.
        if self.current_view == 'students':
            self.headers = [
                {"col": "id", "text": "Student ID", "width": 120},
                {"col": "firstname", "text": "First Name", "width": 180},
                {"col": "lastname", "text": "Last Name", "width": 180},
                {"col": "gender", "text": "Gender", "width": 100},
                {"col": "programCode", "text": "Program Code", "width": 120},
                {"col": "year", "text": "Year Level", "width": 100}
            ]
            self.search_fields_metadata = [
                {"val": "all", "text": "All Columns"},
                {"val": "id", "text": "Student ID"},
                {"val": "firstname", "text": "First Name"},
                {"val": "lastname", "text": "Last Name"},
                {"val": "gender", "text": "Gender"},
                {"val": "programCode", "text": "Program"},
                {"val": "year", "text": "Year Level"}
            ]
        elif self.current_view == 'programs':
            self.headers = [
                {"col": "code", "text": "Program Code", "width": 140},
                {"col": "name", "text": "Program Course Name", "width": 380},
                {"col": "collegeCode", "text": "College Code", "width": 160}
            ]
            self.search_fields_metadata = [
                {"val": "all", "text": "All Columns"},
                {"val": "code", "text": "Program Code"},
                {"val": "name", "text": "Program Name"},
                {"val": "collegeCode", "text": "College Code"}
            ]
        else: # colleges
            self.headers = [
                {"col": "code", "text": "College Code", "width": 160},
                {"col": "name", "text": "Academic Division Name", "width": 520}
            ]
            self.search_fields_metadata = [
                {"val": "all", "text": "All Columns"},
                {"val": "code", "text": "College Code"},
                {"val": "name", "text": "College Name"}
            ]

        # Reset Combobox search items
        self.search_col_combo['values'] = [x['text'] for x in self.search_fields_metadata]
        # Match previous selection if valid, else default to "All" (index 0)
        found_idx = 0
        for i, f in enumerate(self.search_fields_metadata):
            if f['val'] == self.search_field:
                found_idx = i
                break
        self.search_col_combo.current(found_idx)

        # Clear and reconstruct column schemas in virtual Treeview grid
        self.tree.config(columns=[h['col'] for h in self.headers])
        for col in [h['col'] for h in self.headers]:
            self.tree.column(col, anchor=tk.W)

        # Render Header elements with clickable sort callback binding
        for h in self.headers:
            col_id = h['col']
            col_text = h['text']
            
            # Format custom visual sort direction symbol triggers
            suffix = "   ⇅"
            if self.sort_field == col_id:
                suffix = "   ▲" if self.sort_direction else "   ▼"
            
            self.tree.heading(col_id, text=col_text + suffix, anchor=tk.W, 
                              command=lambda c=col_id: self.trigger_sort(c))
            self.tree.column(col_id, width=h['width'], minwidth=60, stretch=tk.YES)

        self.filter_data()

    # --- LIVE SEARCH & LIVE DATA FILTERING SYSTEM ---
    def on_search_field_change(self, event=None):
        """Synchronizes selected textual search field dropdown filter state."""
        sel_name = self.search_col_combo.get()
        for f in self.search_fields_metadata:
            if f['text'] == sel_name:
                self.search_field = f['val']
                break
        self.filter_data()

    def clear_search_field(self):
        """Clears text entries instantly and triggers re-filtering."""
        self.search_val_var.set('')
        self.filter_data()

    def filter_data(self):
        """Retrieves active raw dataset, filters by query, applies sorting, renders rows."""
        # Fetch fresh database state
        filename = DB_FILES[self.current_view]
        raw_items = load_data(filename)
        query = self.search_val_var.get().strip().lower()

        # Apply Search Filtering rules matching All or specific column attributes
        filtered_items = []
        if not query:
            filtered_items = raw_items
        else:
            for r in raw_items:
                if self.search_field == 'all':
                    # Search across all row attributes
                    match = False
                    for val in r.values():
                        if val and query in str(val).lower():
                            match = True
                            break
                    if match:
                        filtered_items.append(r)
                else:
                    field_val = r.get(self.search_field, '')
                    if field_val and query in str(field_val).lower():
                        filtered_items.append(r)

        # --- SORTING COMPUTATION ---
        if self.sort_field:
            def sort_key(row_dict):
                val = row_dict.get(self.sort_field, '')
                # Int cast try for numeric sort e.g. Year
                if self.current_view == 'students' and self.sort_field == 'year':
                    try:
                        return (int(val), "")
                    except ValueError:
                        pass
                return (str(val).lower().strip(), "")
            
            filtered_items.sort(key=sort_key, reverse=not self.sort_direction)

        # Populate Tkinter Treeview Widget Row-by-Row
        # Clear existing visual items
        for child in self.tree.get_children():
            self.tree.delete(child)

        # Render items with clean alternating highlight tags to keep design distinct
        for idx, item in enumerate(filtered_items):
            row_vals = [item.get(h['col'], '') for h in self.headers]
            # Primary Key acts as the Virtual GUI Row ID identifier to allow surgical tracebacks
            pk = 'id' if self.current_view == 'students' else 'code'
            pk_val = item[pk]
            
            tag = 'even_row' if idx % 2 == 0 else 'odd_row'
            self.tree.insert('', tk.END, iid=pk_val, values=row_vals, tags=(tag,))

        # Style tag row colors alternating subtly
        self.tree.tag_configure('even_row', background='#ffffff')
        self.tree.tag_configure('odd_row', background='#f8fafc')

    def trigger_sort(self, column_id):
        """Handles sorting configuration state toggle on column header header clicks."""
        if self.sort_field == column_id:
            self.sort_direction = not self.sort_direction
        else:
            self.sort_field = column_id
            self.sort_direction = True
        
        self.load_active_view_data()

    # --- CRUD ACTIONS FOR DELETE OPERATIONS ---
    def delete_selected_record(self):
        """Executes delete record request with safety alerts and integrity rules."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please click on a row inside the database table to delete.")
            return

        pk_val = selected[0] # Grab Row database primary key
        pk_field = 'id' if self.current_view == 'students' else 'code'
        singular_name = 'student' if self.current_view == 'students' else 'program' if self.current_view == 'programs' else 'college'

        # --- DATABASE INTEGRITY ASSESSMENTS (CASCADE SAFETIES) ---
        if self.current_view == 'programs':
            # Assess if students currently belong to Program code about to be deleted
            students = load_data(DB_FILES['students'])
            assigned_students = [s for s in students if s.get('programCode', '').upper() == pk_val.upper()]
            if assigned_students:
                messagebox.showerror(
                    "Integrity Restriction", 
                    f"Cascade Deletion Blocked!\n\nCannot delete program Code \"{pk_val}\" "
                    f"because there are {len(assigned_students)} student(s) currently enrolled in it.\n\n"
                    f"Please re-assign or delete those student files first."
                )
                return

        elif self.current_view == 'colleges':
            # Assess if academic program blocks belong to Colleges folder about to be deleted
            programs = load_data(DB_FILES['programs'])
            assigned_programs = [p for p in programs if p.get('collegeCode', '').upper() == pk_val.upper()]
            if assigned_programs:
                messagebox.showerror(
                    "Integrity Restriction", 
                    f"Cascade Deletion Blocked!\n\nCannot delete college folder \"{pk_val}\" "
                    f"because it has {len(assigned_programs)} academic program(s) attached to it.\n\n"
                    f"Please delete or update those courses first to safe keep student files."
                )
                return

        # Double check user intent confirmation
        confirm = messagebox.askyesno(
            "Confirm Record Deletion", 
            f"Are you absolutely certain you want to permanently delete the {singular_name} entry with key: \"{pk_val}\"?",
            icon='warning'
        )
        if not confirm:
            return

        # Perform deletion and rewrite CSV
        current_csv = DB_FILES[self.current_view]
        all_records = load_data(current_csv)
        filtered_records = [r for r in all_records if r[pk_field].upper() != pk_val.upper()]

        # Generate headers signature
        if self.current_view == 'students':
            cols = ['id', 'firstname', 'lastname', 'programCode', 'year', 'gender']
        elif self.current_view == 'programs':
            cols = ['code', 'name', 'collegeCode']
        else:
            cols = ['code', 'name']

        save_data(current_csv, cols, filtered_records)
        self.filter_data() # Refresh UI instantly
        messagebox.showinfo("Delete Complete", f"Success! The database entry with ID \"{pk_val}\" was deleted.")

    # --- DIALOG / MODAL FORM COMPILER (ADD / EDIT) ---
    def open_add_dialog(self):
        """Aggregates modal controls to generate a new entry."""
        FormDialog(self, title=f"Create New {self.current_view.capitalize()} Record", mode='add')

    def open_edit_dialog(self):
        """Finds row identifiers, grab fields, and spins editable popup matching key parameters."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Edit Missing selection", "Please click a row from the dataset table grid to edit details.")
            return
        pk_val = selected[0]
        FormDialog(self, title=f"Edit {self.current_view.capitalize()} Record - ID: {pk_val}", mode='edit', target_pk=pk_val)

    # --- INITIAL CLEAN DEFAULTS RE-SEEDER ACTION ---
    def reset_database_to_csv(self):
        """Forces clean factory restore from /public/samples CSV resources."""
        confirm = messagebox.askyesno(
            "System Database Reset",
            f"You are requesting to wipe out current modifications inside storage and reset the entire "
            f"\"{self.current_view}\" table to original sample default records.\n\nAre you sure you wish to proceed?",
            icon='warning'
        )
        if not confirm:
            return

        filepath = DB_FILES[self.current_view]
        try:
            # Overwrite the sample file directly with hardcoded defaults
            if self.current_view == 'colleges':
                save_data(filepath, ['code', 'name'], DEFAULT_COLLEGES)
            elif self.current_view == 'programs':
                save_data(filepath, ['code', 'name', 'collegeCode'], DEFAULT_PROGRAMS)
            elif self.current_view == 'students':
                save_data(filepath, ['id', 'firstname', 'lastname', 'programCode', 'year', 'gender'], DEFAULT_STUDENTS)

            self.filter_data()
            messagebox.showinfo("Reset Successful", f"Database successfully overwritten! Loaded defaults catalog for \"{self.current_view}\".")
        except Exception as e:
            messagebox.showerror("Overwrite Failed", f"Operational issue occurred during rewrite files:\n{e}")


# --- FORM POPUP FOR ADD/EDIT OPERATION ---
class FormDialog(tk.Toplevel):
    def __init__(self, parent, title, mode='add', target_pk=None):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.target_pk = target_pk
        self.current_view = parent.current_view

        self.title(title)
        self.configure(bg="#ffffff")
        self.resizable(False, False)
        
        # Center relative to parent coordinates
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 150, parent.winfo_rooty() + 80))
        
        # Lock visual focus (Modal state behaviour)
        self.transient(parent)
        self.grab_set()

        # Setup dialog window widgets
        self.build_modal_inputs()

    def build_modal_inputs(self):
        """Creates elegant, neatly arranged stacked form layouts depending on the active View."""
        form_frame = tk.Frame(self, bg="#ffffff", padx=24, pady=24)
        form_frame.pack(fill=tk.BOTH, expand=True)

        self.inputs = {}

        # 1. STUDENTS FORM STRUCTURE
        if self.current_view == 'students':
            # Grab programs data for dropdown references
            programs_db = load_data(DB_FILES['programs'])
            program_options = [p['code'] for p in programs_db if p.get('code')]

            fields = [
                {"name": "id", "label": "Student ID Number (enforce format YYYY-NNNN):", "type": "entry"},
                {"name": "firstname", "label": "Student First Name:", "type": "entry"},
                {"name": "lastname", "label": "Student Last Name:", "type": "entry"},
                {"name": "gender", "label": "Gender:", "type": "combo", "opts": ["Male", "Female", "Other"]},
                {"name": "programCode", "label": "Academic Program Affiliation:", "type": "combo", "opts": program_options},
                {"name": "year", "label": "Current enrolled Year Level:", "type": "combo", "opts": ["1", "2", "3", "4", "5"]}
            ]
            
            # Warn if parent is missing programs
            if not program_options:
                messagebox.showerror(
                    "Referential Constraint Warning", 
                    "There are no active Program Codes inside the directory database!\n\n"
                    "By guidelines, a Student must belong to a valid program. Please close this "
                    "window and create a Program first."
                )
                self.destroy()
                return

        # 2. PROGRAMS FORM STRUCTURE
        elif self.current_view == 'programs':
            # Grab colleges data for collegeCode referencing 
            colleges_db = load_data(DB_FILES['colleges'])
            college_options = [c['code'] for c in colleges_db if c.get('code')]

            fields = [
                {"name": "code", "label": "Program Code (ex. BSCS, BSIT):", "type": "entry"},
                {"name": "name", "label": "Complete Program Degree Name:", "type": "entry"},
                {"name": "collegeCode", "label": "Associated Academic College Code:", "type": "combo", "opts": college_options}
            ]

            # Warn if parent is missing colleges
            if not college_options:
                messagebox.showerror(
                    "Referential Constraint Warning", 
                    "There are no colleges registered in the Colleges directory!\n\n"
                    "By guidelines, a program must belong to a college. Please close this "
                    "window and create a College entry first."
                )
                self.destroy()
                return

        # 3. COLLEGES FORM
        else: # colleges
            fields = [
                {"name": "code", "label": "College division Code (ex. CCS, COE):", "type": "entry"},
                {"name": "name", "label": "Division / College Academic Department Title:", "type": "entry"}
            ]

        # Populate Input Widgets stacked cleanly in a responsive vertical layout
        current_idx = 0
        for f in fields:
            lbl = tk.Label(form_frame, text=f['label'], font=("Segoe UI", 9, "bold"), fg=self.parent.text_dark, bg="#ffffff")
            lbl.grid(row=current_idx, column=0, sticky=tk.W, pady=(8, 3))
            current_idx += 1

            if f['type'] == 'entry':
                var = tk.StringVar()
                widget = tk.Entry(form_frame, textvariable=var, font=("Segoe UI", 10), bg="#f8fafc", relief=tk.SOLID, bd=1)
                widget.grid(row=current_idx, column=0, sticky=tk.EW, pady=(0, 10), ipady=4)
                self.inputs[f['name']] = var
                
                # Freeze primary key editing if we are in Edit mode
                pk_to_freeze = 'id' if self.current_view == 'students' else 'code'
                if self.mode == 'edit' and f['name'] == pk_to_freeze:
                    widget.config(state="disabled", bg="#e2e8f0", fg=self.parent.text_muted)

            elif f['type'] == 'combo':
                var = tk.StringVar()
                widget = ttk.Combobox(form_frame, textvariable=var, state="readonly", font=("Segoe UI", 10))
                # Explicit combobox option loading
                widget['values'] = f['opts']
                widget.grid(row=current_idx, column=0, sticky=tk.EW, pady=(0, 10))
                self.inputs[f['name']] = var

            current_idx += 1

        # Populate default fields values immediately if doing updates
        if self.mode == 'edit':
            self.load_editable_data_values()

        # Action command footer
        actions = tk.Frame(form_frame, bg="#ffffff")
        actions.grid(row=current_idx, column=0, sticky=tk.E, pady=(15, 0))

        btn_cancel = tk.Button(actions, text="Cancel", font=("Segoe UI", 9, "bold"),
                               bg="#ffffff", fg=self.parent.text_dark, activebackground="#f1f5f9", 
                               relief=tk.SOLID, bd=1, cursor="hand2")
        btn_cancel.config(command=self.destroy, padx=14, pady=6)
        btn_cancel.pack(side=tk.RIGHT, padx=4)

        btn_save = tk.Button(actions, text="Save Changes" if self.mode == 'edit' else "Add Entry", 
                             font=("Segoe UI", 9, "bold"), bg=self.parent.brand_red, fg="#ffffff", 
                             activebackground=self.parent.brand_red_hover, activeforeground="#ffffff", bd=0, cursor="hand2")
        btn_save.config(command=self.submit_form_details, padx=20, pady=6)
        btn_save.pack(side=tk.RIGHT, padx=4)

        form_frame.columnconfigure(0, weight=1)

    def load_editable_data_values(self):
        """Loads parameters matching Primary Key indexes back to inputs interface."""
        all_records = load_data(DB_FILES[self.current_view])
        pk_field = 'id' if self.current_view == 'students' else 'code'
        
        target = None
        for r in all_records:
            if r.get(pk_field, '').upper() == self.target_pk.upper():
                target = r
                break
        
        if target:
            for field, var in self.inputs.items():
                var.set(target.get(field, ''))

    def submit_form_details(self):
        """Checks for input rules, processes inserts/updates, rewrites persistent backend database."""
        # Collate values 
        data_packet = {}
        for f_name, var in self.inputs.items():
            val = var.get().strip()
            if not val:
                messagebox.showerror("Incomplete Forms", f"Inputs required!\n\nThe column \"{f_name}\" cannot be left blank.")
                return
            data_packet[f_name] = val

        filename = DB_FILES[self.current_view]
        all_records = load_data(filename)
        pk_field = 'id' if self.current_view == 'students' else 'code'

        # Force format constraint matching for Student ID keys
        if self.current_view == 'students':
            id_val = data_packet['id']
            # Regular Expression enforcing YYYY-NNNN standard format
            if not re.match(r'^\d{4}-\d{4}$', id_val):
                messagebox.showerror(
                    "Format Validation Error", 
                    "Invalid Student ID!\n\nStandard ID must be structured in YYYY-NNNN (e.g., 2021-0001)."
                )
                return

        # Check duplicated keys under INSERT operational states
        if self.mode == 'add':
            pk_val = data_packet[pk_field]
            if any(r.get(pk_field, '').upper() == pk_val.upper() for r in all_records):
                messagebox.showerror(
                    "Conflict Discovered", 
                    f"Action aborted!\n\nA record inside the \"{self.current_view}\" "
                    f"tables already contains the Primary Key code: \"{pk_val}\"."
                )
                return
            
            # Insert entry 
            all_records.append(data_packet)
        else:
            # Edit update flow
            idx_to_replace = -1
            for i, r in enumerate(all_records):
                if r.get(pk_field, '').upper() == self.target_pk.upper():
                    idx_to_replace = i
                    break
            
            if idx_to_replace != -1:
                # Merge old PK with newly edited data
                all_records[idx_to_replace] = data_packet
            else:
                messagebox.showerror("Error", "The target data packet could not be resolved inside database records.")
                return

        # Prepare headers format and overwrite persistence CSV
        if self.current_view == 'students':
            cols = ['id', 'firstname', 'lastname', 'programCode', 'year', 'gender']
        elif self.current_view == 'programs':
            cols = ['code', 'name', 'collegeCode']
        else:
            cols = ['code', 'name']

        save_data(filename, cols, all_records)
        
        # Reload table listings 
        self.parent.filter_data()
        self.destroy()


# --- COMMAND LINE LAUNCHER BINDING ---
if __name__ == "__main__":
    app = SSISApp()
    app.mainloop()
