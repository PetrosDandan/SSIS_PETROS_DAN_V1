import tkinter as tk
from tkinter import ttk, messagebox

from config import DB_FILES, DEFAULT_COLLEGES, DEFAULT_PROGRAMS, DEFAULT_STUDENTS
from database import initialize_database, load_data, save_data
from dialogs import FormDialog


class SSISApp(tk.Tk):
    def __init__(self):
        super().__init__()

        initialize_database()

        self.title("Simple Student Information System (SSIS)")
        self.geometry("1024x680")
        self.minimum_width = 850
        self.minimum_height = 550
        self.minsize(self.minimum_width, self.minimum_height)

        self.current_view = 'students'
        self.search_field = 'all'
        self.sort_field = None
        self.sort_direction = True

        self.brand_red = "#800000"
        self.brand_red_hover = "#600000"
        self.bg_light = "#f8f9fa"
        self.border_gray = "#e2e8f0"
        self.text_dark = "#1e293b"
        self.text_muted = "#64748b"

        self.setup_styles()
        self.build_ui()
        self.load_active_view_data()

    def setup_styles(self):
        self.configure(bg=self.bg_light)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background="#ffffff",
                        foreground=self.text_dark,
                        rowheight=28,
                        fieldbackground="#ffffff",
                        font=("Segoe UI", 10))
        style.map("Treeview",
                  background=[('selected', self.brand_red)],
                  foreground=[('selected', '#ffffff')])
        style.configure("Treeview.Heading",
                        background="#f1f5f9",
                        foreground="#475569",
                        padding=8,
                        font=("Segoe UI", 9, "bold"),
                        borderwidth=0)
        style.map("Treeview.Heading",
                  background=[('active', '#e2e8f0')],
                  foreground=[('active', '#0f172a')])
        style.configure("Vertical.TScrollbar", gripcount=0, background="#cbd5e1", bordercolor="#f8fafa", troughcolor="#f8fafa")
        style.configure("Horizontal.TScrollbar", gripcount=0, background="#cbd5e1", bordercolor="#f8fafa", troughcolor="#f8fafa")

    def build_ui(self):
        header = tk.Frame(self, bg=self.brand_red, height=75)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title_label = tk.Label(header, text="STUDENT INFORMATION SYSTEM (SSIS)",
                               font=("Segoe UI", 15, "bold"), fg="#ffffff", bg=self.brand_red)
        title_label.pack(anchor=tk.W, padx=24, pady=(13, 0))

        subtitle_label = tk.Label(header, text="Academic Database Launcher",
                                  font=("Segoe UI", 9), fg="#fbcfe8", bg=self.brand_red)
        subtitle_label.pack(anchor=tk.W, padx=24, pady=(0, 10))

        body = tk.Frame(self, bg=self.bg_light)
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)

        nav_frame = tk.Frame(body, bg=self.bg_light)
        nav_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 16))

        self.nav_btns = {}
        for view_key, label in [('students', 'Students Database'), ('programs', 'Programs Database'), ('colleges', 'Colleges Directory')]:
            btn = tk.Button(nav_frame, text=label, font=("Segoe UI", 10, "bold"),
                            bd=0, activebackground=self.border_gray, cursor="hand2", padx=20, pady=8)
            btn.pack(side=tk.LEFT, padx=(0, 6))
            btn.config(command=lambda k=view_key: self.switch_view(k))
            self.nav_btns[view_key] = btn

        controls_card = tk.LabelFrame(body, bg="#ffffff", bd=1, relief=tk.SOLID, highlightthickness=0)
        controls_card.config(highlightbackground=self.border_gray, fg=self.text_muted)
        controls_card.pack(fill=tk.X, side=tk.TOP, ipady=12, ipadx=10, pady=(0, 16))

        search_container = tk.Frame(controls_card, bg="#ffffff")
        search_container.pack(side=tk.LEFT, padx=16, pady=4)

        tk.Label(search_container, text="Search Field:", font=("Segoe UI", 9, "bold"), fg=self.text_dark, bg="#ffffff").pack(side=tk.LEFT, padx=(0, 6))
        self.search_col_combo = ttk.Combobox(search_container, state="readonly", font=("Segoe UI", 9), width=15)
        self.search_col_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.search_col_combo.bind("<<ComboboxSelected>>", self.on_search_field_change)

        tk.Label(search_container, text="Query:", font=("Segoe UI", 9, "bold"), fg=self.text_dark, bg="#ffffff").pack(side=tk.LEFT, padx=(0, 6))

        self.search_val_var = tk.StringVar()
        self.search_entry = tk.Entry(search_container, textvariable=self.search_val_var,
                                     font=("Segoe UI", 10), bg="#f1f5f9", relief=tk.FLAT, bd=0, width=28)
        self.search_entry.pack(side=tk.LEFT, ipady=5, ipadx=6)
        self.search_val_var.trace_add("write", lambda *args: self.filter_data())

        self.btn_clear_search = tk.Button(search_container, text="Clear", font=("Segoe UI", 8, "bold"),
                                          bg="#e2e8f0", fg=self.text_dark, activebackground="#cbd5e1", bd=0, cursor="hand2")
        self.btn_clear_search.pack(side=tk.LEFT, padx=8, ipady=2, ipadx=8)
        self.btn_clear_search.config(command=self.clear_search_field)

        actions_container = tk.Frame(controls_card, bg="#ffffff")
        actions_container.pack(side=tk.RIGHT, padx=16, pady=4)

        self.btn_add = tk.Button(actions_container, text="+ Add Record", font=("Segoe UI", 9, "bold"),
                                 bg=self.brand_red, fg="#ffffff", activebackground=self.brand_red_hover,
                                 activeforeground="#ffffff", bd=0, cursor="hand2")
        self.btn_add.config(command=self.open_add_dialog, padx=14, pady=5)
        self.btn_add.pack(side=tk.RIGHT, padx=4)

        table_container = tk.Frame(body, bg="#ffffff", bd=1, relief=tk.SOLID, highlightthickness=0)
        table_container.config(highlightbackground=self.border_gray)
        table_container.pack(fill=tk.BOTH, expand=True, side=tk.TOP, pady=(0, 16))

        v_scroll = ttk.Scrollbar(table_container, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(table_container, columns=(), show="headings",
                                 yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        v_scroll.pack(fill=tk.Y, side=tk.RIGHT)
        h_scroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", lambda event: self.open_edit_dialog())

        bottom_panel = tk.Frame(body, bg=self.bg_light)
        bottom_panel.pack(fill=tk.X, side=tk.TOP)

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

        right_ops = tk.Frame(bottom_panel, bg=self.bg_light)
        right_ops.pack(side=tk.RIGHT)

        self.btn_reset = tk.Button(right_ops, text="Reset to CSV defaults", font=("Segoe UI", 9, "bold"),
                                   bg="#ffffff", fg=self.text_dark, activebackground="#f1f5f9",
                                   relief=tk.SOLID, bd=1, cursor="hand2")
        self.btn_reset.config(command=self.reset_database_to_csv, padx=14, pady=6)
        self.btn_reset.grid(row=0, column=0, padx=4)

        self.update_nav_tabs()

    def switch_view(self, key):
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
        for key, btn in self.nav_btns.items():
            if key == self.current_view:
                btn.config(bg=self.brand_red, fg="#ffffff", activebackground=self.brand_red, relief=tk.FLAT)
            else:
                btn.config(bg="#ffffff", fg=self.text_dark, activebackground="#f1f5f9", relief=tk.SOLID, bd=1)

    def load_active_view_data(self):
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
        else:
            self.headers = [
                {"col": "code", "text": "College Code", "width": 160},
                {"col": "name", "text": "Academic Division Name", "width": 520}
            ]
            self.search_fields_metadata = [
                {"val": "all", "text": "All Columns"},
                {"val": "code", "text": "College Code"},
                {"val": "name", "text": "College Name"}
            ]

        self.search_col_combo['values'] = [x['text'] for x in self.search_fields_metadata]
        found_idx = next((i for i, f in enumerate(self.search_fields_metadata) if f['val'] == self.search_field), 0)
        self.search_col_combo.current(found_idx)

        self.tree.config(columns=[h['col'] for h in self.headers])
        for col in [h['col'] for h in self.headers]:
            self.tree.column(col, anchor=tk.W)

        for h in self.headers:
            col_id = h['col']
            col_text = h['text']
            suffix = "   ⇅"
            if self.sort_field == col_id:
                suffix = "   ▲" if self.sort_direction else "   ▼"
            self.tree.heading(col_id, text=col_text + suffix, anchor=tk.W,
                              command=lambda c=col_id: self.trigger_sort(c))
            self.tree.column(col_id, width=h['width'], minwidth=60, stretch=tk.YES)

        self.filter_data()

    def on_search_field_change(self, event=None):
        sel_name = self.search_col_combo.get()
        for f in self.search_fields_metadata:
            if f['text'] == sel_name:
                self.search_field = f['val']
                break
        self.filter_data()

    def clear_search_field(self):
        self.search_val_var.set('')
        self.filter_data()

    def filter_data(self):
        filename = DB_FILES[self.current_view]
        raw_items = load_data(filename)
        query = self.search_val_var.get().strip().lower()

        filtered_items = []
        if not query:
            filtered_items = raw_items
        else:
            for record in raw_items:
                if self.search_field == 'all':
                    if any(val and query in str(val).lower() for val in record.values()):
                        filtered_items.append(record)
                else:
                    field_val = record.get(self.search_field, '')
                    if field_val and query in str(field_val).lower():
                        filtered_items.append(record)

        if self.sort_field:
            def sort_key(item):
                value = item.get(self.sort_field, '')
                if self.current_view == 'students' and self.sort_field == 'year':
                    try:
                        return (int(value), "")
                    except ValueError:
                        pass
                return (str(value).lower().strip(), "")
            filtered_items.sort(key=sort_key, reverse=not self.sort_direction)

        for child in self.tree.get_children():
            self.tree.delete(child)

        for idx, item in enumerate(filtered_items):
            row_vals = [item.get(h['col'], '') for h in self.headers]
            pk = 'id' if self.current_view == 'students' else 'code'
            pk_val = item[pk]
            tag = 'even_row' if idx % 2 == 0 else 'odd_row'
            self.tree.insert('', tk.END, iid=pk_val, values=row_vals, tags=(tag,))

        self.tree.tag_configure('even_row', background='#ffffff')
        self.tree.tag_configure('odd_row', background='#f8fafc')

    def trigger_sort(self, column_id):
        if self.sort_field == column_id:
            self.sort_direction = not self.sort_direction
        else:
            self.sort_field = column_id
            self.sort_direction = True
        self.load_active_view_data()

    def delete_selected_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please click on a row inside the database table to delete.")
            return

        pk_val = selected[0]
        pk_field = 'id' if self.current_view == 'students' else 'code'
        singular_name = 'student' if self.current_view == 'students' else 'program' if self.current_view == 'programs' else 'college'

        if self.current_view == 'programs':
            students = load_data(DB_FILES['students'])
            assigned_students = [s for s in students if s.get('programCode', '').upper() == pk_val.upper()]
            if assigned_students:
                messagebox.showerror(
                    "Integrity Restriction",
                    f"Cascade Deletion Blocked!\n\nCannot delete program Code \"{pk_val}\" "
                    f"because there are {len(assigned_students)} student(s) currently enrolled in it.\n\n"
                    "Please re-assign or delete those student files first."
                )
                return

        elif self.current_view == 'colleges':
            programs = load_data(DB_FILES['programs'])
            assigned_programs = [p for p in programs if p.get('collegeCode', '').upper() == pk_val.upper()]
            if assigned_programs:
                messagebox.showerror(
                    "Integrity Restriction",
                    f"Cascade Deletion Blocked!\n\nCannot delete college folder \"{pk_val}\" "
                    f"because it has {len(assigned_programs)} academic program(s) attached to it.\n\n"
                    "Please delete or update those courses first to safe keep student files."
                )
                return

        confirm = messagebox.askyesno(
            "Confirm Record Deletion",
            f"Are you absolutely certain you want to permanently delete the {singular_name} entry with key: \"{pk_val}\"?",
            icon='warning'
        )
        if not confirm:
            return

        current_csv = DB_FILES[self.current_view]
        all_records = load_data(current_csv)
        filtered_records = [r for r in all_records if r[pk_field].upper() != pk_val.upper()]

        if self.current_view == 'students':
            cols = ['id', 'firstname', 'lastname', 'programCode', 'year', 'gender']
        elif self.current_view == 'programs':
            cols = ['code', 'name', 'collegeCode']
        else:
            cols = ['code', 'name']

        save_data(current_csv, cols, filtered_records)
        self.filter_data()
        messagebox.showinfo("Delete Complete", f"Success! The database entry with ID \"{pk_val}\" was deleted.")

    def open_add_dialog(self):
        FormDialog(self, title=f"Create New {self.current_view.capitalize()} Record", mode='add')

    def open_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Edit Missing selection", "Please click a row from the dataset table grid to edit details.")
            return
        pk_val = selected[0]
        FormDialog(self, title=f"Edit {self.current_view.capitalize()} Record - ID: {pk_val}", mode='edit', target_pk=pk_val)

    def reset_database_to_csv(self):
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
            if self.current_view == 'colleges':
                save_data(filepath, ['code', 'name'], DEFAULT_COLLEGES)
            elif self.current_view == 'programs':
                save_data(filepath, ['code', 'name', 'collegeCode'], DEFAULT_PROGRAMS)
            else:
                save_data(filepath, ['id', 'firstname', 'lastname', 'programCode', 'year', 'gender'], DEFAULT_STUDENTS)

            self.filter_data()
            messagebox.showinfo("Reset Successful", f"Database successfully overwritten! Loaded defaults catalog for \"{self.current_view}\".")
        except Exception as exc:
            messagebox.showerror("Overwrite Failed", f"Operational issue occurred during rewrite files:\n{exc}")
