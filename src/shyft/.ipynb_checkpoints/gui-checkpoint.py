import datetime
import json
import os
import tkinter as tk
from datetime import datetime, timedelta
from pathlib import Path as p
from tkinter import ttk, messagebox, simpledialog, Text, Button


HOME = p.home()
WORKSPACES_DIR = HOME / 'workspaces'
VYPYR_DIR = WORKSPACES_DIR / 'vypyr'
SRC_DIR = VYPYR_DIR / 'src'
shyft_DIR = SRC_DIR.resolve() / 'shyft'
DATA_PATH = shyft_DIR.resolve() / "data.json"
LOGS_DIR = shyft_DIR.resolve() / "logs"


class TimerWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Timer")
        self.elapsed_time = timedelta(0)
        self.running = False
        self.last_time = None

        # Timer display label
        self.timer_label = tk.Label(self.master, text="00:00:00", font=("Helvetica", 16))
        self.timer_label.pack(padx=10, pady=10)

        # Control buttons
        controls_frame = tk.Frame(self.master)
        controls_frame.pack(pady=5)

        self.start_button = tk.Button(controls_frame, text="Start", command=self.start)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(controls_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(controls_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side="left", padx=5)

        # Update the timer every 100ms
        self.update_timer()

    def start(self):
        if not self.running:
            self.running = True
            self.last_time = datetime.now()

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time += datetime.now() - self.last_time

    def reset(self):
        self.stop()
        self.elapsed_time = timedelta(0)
        self.timer_label.config(text="00:00:00")

    def update_timer(self):
        if self.running:
            current_time = datetime.now()
            delta = current_time - self.last_time
            elapsed = self.elapsed_time + delta
            self.timer_label.config(text=str(elapsed).split('.')[0])
        self.master.after(100, self.update_timer)


class shyftGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("shyft Timekeeper GUI")
        self.configure_styles()
        self.load_data()
        self.create_widgets()
        self.refresh_view()
        self.timer_window = None

    def configure_styles(self):
        self.style = ttk.Style(self.master)
        self.style.configure(
            "TButton",
            foreground="black",
            background="light gray",
            font=("Helvetica", 12),
        )
        self.style.configure(
            "TLabel",
            foreground="green",
            background="light gray",
            font=("Helvetica", 12, "bold"),
        )
        self.style.configure(
            "TEntry", foreground="black", background="white", font=("Helvetica", 12)
        )
        self.style.configure(
            "Treeview", background="white", fieldbackground="white", foreground="black"
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Helvetica", 10, "bold"),
            foreground="black",
            background="gray",
        )

    def load_data(self):
        wd = os.getcwd()
        if wd != shyft_DIR:
            os.chdir(shyft_DIR)
        else:
            pass
        try:
            with open(DATA_PATH, "r") as f:
                self.data = json.load(f).get("data", {})
        except FileNotFoundError:
            messagebox.showerror("Error", "data.json not found.")
            self.data = {}

    def save_data(self):
        try:
            with open(DATA_PATH, "w") as f:
                json.dump({"data": self.data}, f, indent=4)
            messagebox.showinfo("Success", "Data updated successfully.")
        except Exception as e:
            messagebox.showerror("Save Failed", str(e))

    def create_widgets(self):
        self.tree = ttk.Treeview(
            self.master,
            columns=(
                "ID",
                "Date",
                "Project ID",
                "Model ID",
                "In (hh:mm)",
                "Out (hh:mm)",
                "Duration (hrs)",
                "Hourly rate",
                "Gross pay",
            ),
            show="headings",
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=100)
        self.tree.pack(expand=True, fill="both")

        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill="x", expand=True)

        ttk.Button(
            button_frame,
            text="Manual Entry",
            command=self.manual_entry,
            style="TButton",
        ).pack(side="left", expand=True)
        ttk.Button(
            button_frame, text="Edit Shift", command=self.edit_shift, style="TButton"
        ).pack(side="left", expand=True)
        ttk.Button(
            button_frame,
            text="Delete Shift",
            command=self.delete_shift,
            style="TButton",
        ).pack(side="left", expand=True)
        ttk.Button(
            button_frame,
            text="Refresh View",
            command=self.refresh_view,
            style="TButton",
        ).pack(side="left", expand=True)
        ttk.Button(
            button_frame, text="View Logs", command=self.view_logs, style="TButton"
        ).pack(side="left", expand=True)
        ttk.Button(
            button_frame, text="Autologger", command=self.autologger, style="TButton"
        ).pack(side="left", expand=True)
        ttk.Button(button_frame, text="Totals", command=self.calculate_totals).pack(
            side="left", expand=True
        )

    def refresh_view(self):
        self.load_data()
        self.populate_tree()

    def populate_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for id, shift in self.data.items():
            self.tree.insert(
                "",
                "end",
                iid=id,
                values=(
                    id,
                    shift.get("Date", "N/A"),
                    shift.get("Project ID", "N/A"),
                    shift.get("Model ID", "N/A"),
                    shift.get("In (hh:mm)", "N/A"),
                    shift.get("Out (hh:mm)", "N/A"),
                    shift.get("Duration (hrs)", "N/A"),
                    shift.get("Hourly rate", "N/A"),
                    shift.get("Gross pay", "N/A"),
                ),
            )

    def calculate_totals(self):
        number_of_shifts = len(self.data.values())
        total_hours_worked = sum(
            float(shift["Duration (hrs)"]) for shift in self.data.values()
        )
        total_gross_pay = sum(float(shift["Gross pay"]) for shift in self.data.values())
        tax_liability = total_gross_pay * 0.27
        net_income = total_gross_pay - tax_liability

        # Display these totals in a pop-up window or directly on the GUI
        totals_window = tk.Toplevel(self.master)
        totals_window.title("shyft Totals")

        ttk.Label(totals_window, text="Shifts Worked:                   ").grid(
            row=0, column=0, sticky=tk.W, pady=2, padx=10
        )
        ttk.Label(totals_window, text=f"{number_of_shifts}").grid(
            row=0, column=1, sticky=tk.E, pady=2, padx=10
        )

        ttk.Label(totals_window, text="Total Hours Worked:              ").grid(
            row=1, column=0, sticky=tk.W, pady=2, padx=10
        )
        ttk.Label(totals_window, text=f"{total_hours_worked:.2f}").grid(
            row=1, column=1, sticky=tk.E, pady=2, padx=10
        )

        ttk.Label(totals_window, text="Total Gross Pay:                 ").grid(
            row=2, column=0, sticky=tk.W, pady=2, padx=10
        )
        ttk.Label(totals_window, text=f"${total_gross_pay:.2f}").grid(
            row=2, column=1, sticky=tk.E, pady=2, padx=10
        )

        ttk.Label(totals_window, text="Estimated Tax Liability (27%):   ").grid(
            row=3, column=0, sticky=tk.W, pady=2, padx=10
        )
        ttk.Label(totals_window, text=f"${tax_liability:.2f}").grid(
            row=3, column=1, sticky=tk.E, pady=2, padx=10
        )

        ttk.Label(totals_window, text="Estimated Net Income:            ").grid(
            row=4, column=0, sticky=tk.W, pady=2, padx=10
        )
        ttk.Label(totals_window, text=f"${net_income:.2f}").grid(
            row=4, column=1, sticky=tk.E, pady=2, padx=10
        )

    def view_logs(self):
        os.chdir(LOGS_DIR)
        log_window = tk.Toplevel(self.master)
        log_window.title("View Logs")

        # Create a frame for the TreeView
        tree_frame = ttk.Frame(log_window)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Set up the TreeView
        log_tree = ttk.Treeview(tree_frame, columns=["Log Files"], show="headings")
        log_tree.heading("Log Files", text="Log Files")
        log_tree.column("Log Files", anchor="w", width=100)
        log_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=log_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_tree.configure(yscrollcommand=scrollbar.set)

        # Populate the TreeView with log files
        log_files = sorted(
            [f for f in LOGS_DIR.iterdir() if f.is_file()], key=lambda x: x.name
        )
        for log_file in log_files:
            log_tree.insert("", "end", iid=log_file.name, values=[log_file.name])

        # Create a frame for the Text widget to display the log content
        text_frame = ttk.Frame(log_window)
        text_frame.pack(fill=tk.BOTH, expand=True)
        text_widget = Text(text_frame, wrap="word")
        text_widget.pack(fill=tk.BOTH, expand=True)

        def on_log_selection(event):
            selected_item = log_tree.selection()
            if selected_item:
                log_file_path = LOGS_DIR / selected_item[0]
                with open(log_file_path, "r") as file:
                    content = file.read()
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", content)

        log_tree.bind("<<TreeviewSelect>>", on_log_selection)

    def manual_entry(self):
        window = tk.Toplevel(self.master)
        window.title("Manual Shift Entry")
        entries = {}
        fields = [
            "Date",
            "Project ID",
            "Model ID",
            "In (hh:mm)",
            "Out (hh:mm)",
            "Hourly rate",
        ]
        uppercase_fields = ["Project ID", "Model ID"]  # Fields to convert to uppercase

        for field in fields:
            row = ttk.Frame(window)
            label = ttk.Label(row, width=15, text=field, anchor="w")
            entry_var = tk.StringVar()
            entry = ttk.Entry(row, textvariable=entry_var)
            if field in uppercase_fields:
                entry_var.trace_add(
                    "write", lambda *args, var=entry_var: var.set(var.get().upper())
                )
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries[field] = entry

        # Button Frame
        button_frame = ttk.Frame(window)
        button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        submit_button = ttk.Button(
            button_frame, text="Submit", command=lambda: submit_action()
        )
        submit_button.pack(side=tk.RIGHT, padx=5)

        def submit_action():
            try:
                # Validate time format for StartTime and EndTime
                validate_time_format(entries["In (hh:mm)"].get())
                validate_time_format(entries["Out (hh:mm)"].get())

                new_data = {field: entries[field].get() for field in fields}
                if any(v == "" for v in new_data.values()):
                    messagebox.showerror("Error", "All fields must be filled out.")
                    return

                # Generate a new ID and format it
                new_id = max([int(x) for x in self.data.keys()], default=0) + 1
                formatted_id = self.format_id(new_id)  # Format the new ID

                # Calculate duration based on 'StartTime' and 'EndTime'
                duration_hrs = calculate_duration(
                    new_data["In (hh:mm)"], new_data["Out (hh:mm)"]
                )
                new_data["Duration (hrs)"] = "{:.2f}".format(duration_hrs)
                gross_pay = float(new_data["Hourly rate"]) * duration_hrs
                new_data["Gross pay"] = "{:.2f}".format(gross_pay)

                self.data[formatted_id] = new_data
                self.save_data()
                self.populate_tree()
                window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def calculate_duration(start, end):
            """Calculate the duration in hours between two HH:MM formatted times."""
            try:
                start_dt = datetime.strptime(start, "%H:%M")
                end_dt = datetime.strptime(end, "%H:%M")
                # Handle scenario where end time is past midnight
                if end_dt < start_dt:
                    end_dt += timedelta(days=1)
                duration = (end_dt - start_dt).total_seconds() / 3600.0
                return duration
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM format.")

        def validate_time_format(time_str):
            """Check if the time string is in HH:MM format."""
            try:
                datetime.strptime(time_str, "%H:%M")
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM format.")

    def edit_shift(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a shift to edit.")
            return
        selected_id = selected_item[0]
        shift = self.data.get(selected_id)

        window = tk.Toplevel(self.master)
        window.title("Edit Shift")
        entries = {}
        fields = [
            "Date",
            "Project ID",
            "Model ID",
            "In (hh:mm)",
            "Out (hh:mm)",
            "Duration (hrs)",
            "Hourly rate",
            "Gross pay",
        ]
        uppercase_fields = ["Project ID", "Model ID"]  # Fields to convert to uppercase

        # First, create all entries without the uppercase transformation
        for field in fields:
            row = ttk.Frame(window)
            label = ttk.Label(row, width=15, text=field, anchor="w")
            entry_var = tk.StringVar(value=shift.get(field, ""))
            entry = ttk.Entry(row, textvariable=entry_var)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries[field] = entry_var  # Store the StringVar, not the Entry widget

        # Apply uppercase transformation where necessary
        for field in uppercase_fields:
            entry_var = entries[field]
            entry_var.trace_add(
                "write", lambda *args, var=entry_var: var.set(var.get().upper())
            )

        # Button Frame
        button_frame = ttk.Frame(window)
        button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        submit_button = ttk.Button(
            button_frame, text="Submit", command=lambda: submit_action()
        )
        submit_button.pack(side=tk.RIGHT, padx=5)

        def submit_action():
            try:
                updated_data = {field: entries[field].get() for field in fields}
                if any(v == "" for v in updated_data.values()):
                    messagebox.showerror("Error", "All fields must be filled out.")
                    return

                self.data[selected_id] = updated_data
                self.save_data()
                self.populate_tree()
                window.destroy()
            except Exception as e:
                messagebox.showerror(
                    "Error", "Failed to update shift. Error: " + str(e)
                )

    def delete_shift(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a shift to delete.")
            return
        selected_id = selected_item[0]
        response = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this shift?"
        )
        if response:
            del self.data[selected_id]
            self.save_data()
            self.populate_tree()

    
    def autologger(self):
        model_id_response = simpledialog.askstring(
            "Model ID", "Enter Model ID:", parent=self.master
        )
        if not model_id_response:
            return
        model_id = model_id_response.upper()
    
        project_id_response = simpledialog.askstring(
            "Project ID", "Enter Project ID:", parent=self.master
        )
        if not project_id_response:
            return
        project_id = project_id_response.upper()
    
        hourly_rate = simpledialog.askstring(
            "Hourly rate", "Enter hourly rate:", parent=self.master
        )
        try:
            hourly_rate = float(hourly_rate)
        except (TypeError, ValueError):
            messagebox.showerror(
                "Error", "Invalid hourly rate; please enter a numeric value."
            )
            return
    
        notes_window = tk.Toplevel(self.master)
        notes_window.title("Notes - Autologger")
    
        text = Text(notes_window, wrap=tk.WORD, width=64)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        def insert_divider():
            divider = "═" * 64 + "\n"
            text.insert(tk.INSERT, divider)
    
        if self.timer_window is None or not tk.Toplevel.winfo_exists(self.timer_window.master):
            timer_window = tk.Toplevel(self.master)
            self.timer_window = TimerWindow(timer_window)
            self.timer_window.start()
    
        def submit_notes():
            if self.timer_window:
                self.timer_window.stop()
                elapsed_time = self.timer_window.elapsed_time
    
                seconds_in_a_minute = 60
                whole_minutes = elapsed_time.total_seconds() // seconds_in_a_minute
                duration_minutes = whole_minutes
                duration_hrs = duration_minutes / 60
            else:
                messagebox.showerror("Error", "Timer is not running.")
                return
    
            gross_pay = duration_hrs * hourly_rate
    
            new_id = max([int(x) for x in self.data.keys()], default=0) + 1
            formatted_id = self.format_id(new_id)
    
            self.data[formatted_id] = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Project ID": project_id,
                "Model ID": model_id,
                "In (hh:mm)": (datetime.now() - elapsed_time).strftime("%H:%M"),
                "Out (hh:mm)": datetime.now().strftime("%H:%M"),
                "Duration (hrs)": f"{duration_hrs:.2f}",
                "Hourly rate": f"{hourly_rate:.2f}",
                "Gross pay": f"{gross_pay:.2f}",
            }
    
            if not LOGS_DIR.exists():
                LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
            log_file_path = LOGS_DIR / f"{formatted_id}.log"
            with open(log_file_path, "w") as file:
                file.write(text.get("1.0", tk.END))
    
            self.save_data()
            self.populate_tree()
            notes_window.destroy()
    
            if self.timer_window:
                self.timer_window.reset()
                self.timer_window.master.destroy()
                self.timer_window = None
    
        Button(notes_window, text="Submit", command=submit_notes).pack(
            side=tk.RIGHT, padx=5, pady=5
        )
        Button(notes_window, text="Cancel", command=notes_window.destroy).pack(
            side=tk.LEFT, padx=5, pady=5
        )
        Button(notes_window, text="Insert Divider", command=insert_divider).pack(
            side=tk.TOP, pady=5
        )


    def format_id(self, id):
        """Format the given ID to have at least 3 digits with leading zeros."""
        return f"{id:03d}"


def main():
    root = tk.Tk()
    app = shyftGUI(root)
    app.refresh_view()
    root.mainloop()


if __name__ == "__main__":
    main()