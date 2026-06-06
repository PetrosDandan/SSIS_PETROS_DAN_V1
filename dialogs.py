import re
import tkinter as tk
from tkinter import ttk, messagebox

from config import DB_FILES
from database import load_data, save_data


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
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 150, parent.winfo_rooty() + 80))
        self.transient(parent)
        self.grab_set()

        self.build_modal_inputs()

    def build_modal_inputs(self):
        """Creates a stacked form layout based on the current view."""
        form_frame = tk.Frame(self, bg="#ffffff", padx=24, pady=24)
        form_frame.pack(fill=tk.BOTH, expand=True)

        self.inputs = {}

        if self.current_view == 'students':
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

            if not program_options:
                messagebox.showerror(
                    "Referential Constraint Warning",
                    "There are no active Program Codes inside the directory database!\n\n"
                    "By guidelines, a Student must belong to a valid program. Please close this "
                    "window and create a Program first."
                )
                self.destroy()
                return

        elif self.current_view == 'programs':
            colleges_db = load_data(DB_FILES['colleges'])
            college_options = [c['code'] for c in colleges_db if c.get('code')]

            fields = [
                {"name": "code", "label": "Program Code (ex. BSCS, BSIT):", "type": "entry"},
                {"name": "name", "label": "Complete Program Degree Name:", "type": "entry"},
                {"name": "collegeCode", "label": "Associated Academic College Code:", "type": "combo", "opts": college_options}
            ]

            if not college_options:
                messagebox.showerror(
                    "Referential Constraint Warning",
                    "There are no colleges registered in the Colleges directory!\n\n"
                    "By guidelines, a program must belong to a college. Please close this "
                    "window and create a College entry first."
                )
                self.destroy()
                return

        else:
            fields = [
                {"name": "code", "label": "College division Code (ex. CCS, COE):", "type": "entry"},
                {"name": "name", "label": "Division / College Academic Department Title:", "type": "entry"}
            ]

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

            else:
                var = tk.StringVar()
                widget = ttk.Combobox(form_frame, textvariable=var, state="readonly", font=("Segoe UI", 10))
                widget['values'] = f['opts']
                widget.grid(row=current_idx, column=0, sticky=tk.EW, pady=(0, 10))
                self.inputs[f['name']] = var

            current_idx += 1

        if self.mode == 'edit':
            self.load_editable_data_values()

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
        all_records = load_data(DB_FILES[self.current_view])
        pk_field = 'id' if self.current_view == 'students' else 'code'

        target = next((r for r in all_records if r.get(pk_field, '').upper() == self.target_pk.upper()), None)
        if target:
            for field, var in self.inputs.items():
                var.set(target.get(field, ''))

    def submit_form_details(self):
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

        if self.current_view == 'students':
            if not re.match(r'^\d{4}-\d{4}$', data_packet['id']):
                messagebox.showerror(
                    "Format Validation Error",
                    "Invalid Student ID!\n\nStandard ID must be structured in YYYY-NNNN (e.g., 2021-0001)."
                )
                return

        if self.mode == 'add':
            pk_val = data_packet[pk_field]
            if any(r.get(pk_field, '').upper() == pk_val.upper() for r in all_records):
                messagebox.showerror(
                    "Conflict Discovered",
                    f"Action aborted!\n\nA record inside the \"{self.current_view}\" tables already contains the Primary Key code: \"{pk_val}\"."
                )
                return

            all_records.append(data_packet)
        else:
            idx_to_replace = next((i for i, r in enumerate(all_records) if r.get(pk_field, '').upper() == self.target_pk.upper()), -1)
            if idx_to_replace == -1:
                messagebox.showerror("Error", "The target data packet could not be resolved inside database records.")
                return

            old_pk = self.target_pk
            new_pk = data_packet.get(pk_field, '')

            if new_pk.upper() != old_pk.upper() and any(r.get(pk_field, '').upper() == new_pk.upper() for r in all_records):
                messagebox.showerror(
                    "Conflict Discovered",
                    f"Action aborted!\n\nA record inside the \"{self.current_view}\" tables already contains the Primary Key code: \"{new_pk}\"."
                )
                return

            if self.current_view == 'students':
                programs = load_data(DB_FILES['programs'])
                if not any(p.get('code', '').upper() == data_packet.get('programCode', '').upper() for p in programs):
                    messagebox.showerror(
                        "Referential Integrity",
                        f"Invalid Program Code \"{data_packet.get('programCode')}\". Please choose an existing program."
                    )
                    return

            if self.current_view == 'programs':
                colleges = load_data(DB_FILES['colleges'])
                if not any(c.get('code', '').upper() == data_packet.get('collegeCode', '').upper() for c in colleges):
                    messagebox.showerror(
                        "Referential Integrity",
                        f"Invalid College Code \"{data_packet.get('collegeCode')}\". Please choose an existing college."
                    )
                    return

                if new_pk.upper() != old_pk.upper():
                    students = load_data(DB_FILES['students'])
                    for student in students:
                        if student.get('programCode', '').upper() == old_pk.upper():
                            student['programCode'] = new_pk
                    save_data(DB_FILES['students'], ['id', 'firstname', 'lastname', 'programCode', 'year', 'gender'], students)

            if self.current_view == 'colleges' and new_pk.upper() != old_pk.upper():
                programs = load_data(DB_FILES['programs'])
                for program in programs:
                    if program.get('collegeCode', '').upper() == old_pk.upper():
                        program['collegeCode'] = new_pk
                save_data(DB_FILES['programs'], ['code', 'name', 'collegeCode'], programs)

            all_records[idx_to_replace] = data_packet

        if self.current_view == 'students':
            cols = ['id', 'firstname', 'lastname', 'programCode', 'year', 'gender']
        elif self.current_view == 'programs':
            cols = ['code', 'name', 'collegeCode']
        else:
            cols = ['code', 'name']

        save_data(filename, cols, all_records)
        self.parent.filter_data()
        self.destroy()
