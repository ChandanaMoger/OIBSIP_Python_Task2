import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
import sqlite3
from datetime import datetime
import re

class BMICalculator:
    def __init__(self):
        self.data_file = "bmi_data.json"
        self.db_file = "bmi_database.db"
        self.init_database()
    
    def calculate_bmi(self, weight, height):
        """Calculate BMI given weight in kg and height in meters"""
        try:
            bmi = float(weight) / (float(height) ** 2)
            return round(bmi, 2)
        except (ValueError, ZeroDivisionError):
            return None
    
    def classify_bmi(self, bmi):
        """Classify BMI into categories"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def validate_input(self, weight, height):
        """Validate user input for weight and height"""
        try:
            weight_float = float(weight)
            height_float = float(height)
            
            if weight_float <= 0 or height_float <= 0:
                return False, "Weight and height must be positive numbers"
            
            if weight_float > 300:  # Reasonable upper limit for weight in kg
                return False, "Weight seems too high. Please check your input."
            
            if height_float > 2.5:  # Reasonable upper limit for height in meters
                return False, "Height seems too high. Please check your input."
            
            return True, "Valid input"
            
        except ValueError:
            return False, "Please enter valid numbers for weight and height"
    
    def init_database(self):
        """Initialize SQLite database for storing BMI records"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
    def save_to_database(self, username, weight, height, bmi, category):
        """Save BMI record to SQLite database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO bmi_records (username, weight, height, bmi, category, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, weight, height, bmi, category, timestamp))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_user_history(self, username):
        """Retrieve BMI history for a specific user"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, weight, height, bmi, category 
                FROM bmi_records 
                WHERE username = ? 
                ORDER BY timestamp DESC
            ''', (username,))
            
            records = cursor.fetchall()
            conn.close()
            return records
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_all_users(self):
        """Get list of all unique users"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT DISTINCT username FROM bmi_records')
            users = [row[0] for row in cursor.fetchall()]
            conn.close()
            return users
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

class BMICalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.calculator = BMICalculator()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.calc_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.calc_tab, text='BMI Calculator')
        self.notebook.add(self.history_tab, text='History')
        self.notebook.add(self.stats_tab, text='Statistics')
        
        self.setup_calculator_tab()
        self.setup_history_tab()
        self.setup_stats_tab()
    
    def setup_calculator_tab(self):
        """Setup the BMI calculator tab"""
        # Main frame
        main_frame = ttk.Frame(self.calc_tab)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="BMI Calculator", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill='x', pady=20)
        
        # Username
        ttk.Label(input_frame, text="Username:").grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(input_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        # Weight
        ttk.Label(input_frame, text="Weight (kg):").grid(row=1, column=0, sticky='w', pady=5)
        self.weight_entry = ttk.Entry(input_frame, width=30)
        self.weight_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        # Height
        ttk.Label(input_frame, text="Height (m):").grid(row=2, column=0, sticky='w', pady=5)
        self.height_entry = ttk.Entry(input_frame, width=30)
        self.height_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        input_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Calculate BMI", 
                  command=self.calculate_bmi_gui).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_entries).pack(side='left', padx=5)
        
        # Result frame
        self.result_frame = ttk.LabelFrame(main_frame, text="Result")
        self.result_frame.pack(fill='x', pady=20)
        
        self.result_text = tk.Text(self.result_frame, height=6, width=60, 
                                  font=('Arial', 10), state='disabled')
        self.result_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        # BMI Chart Reference
        chart_frame = ttk.LabelFrame(main_frame, text="BMI Categories")
        chart_frame.pack(fill='x', pady=10)
        
        chart_text = """Underweight: BMI < 18.5
Normal weight: 18.5 ≤ BMI < 25
Overweight: 25 ≤ BMI < 30
Obese: BMI ≥ 30"""
        
        chart_label = tk.Text(chart_frame, height=4, width=60, 
                             font=('Arial', 9), state='disabled')
        chart_label.pack(padx=10, pady=5, fill='both')
        chart_label.config(state='normal')
        chart_label.insert('1.0', chart_text)
        chart_label.config(state='disabled')
    
    def setup_history_tab(self):
        """Setup the history tab"""
        # Main frame
        main_frame = ttk.Frame(self.history_tab)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # User selection
        user_frame = ttk.Frame(main_frame)
        user_frame.pack(fill='x', pady=10)
        
        ttk.Label(user_frame, text="Select User:").pack(side='left', padx=5)
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(user_frame, textvariable=self.user_var, 
                                      state='readonly', width=20)
        self.user_combo.pack(side='left', padx=5)
        
        ttk.Button(user_frame, text="Load History", 
                  command=self.load_user_history).pack(side='left', padx=10)
        ttk.Button(user_frame, text="Refresh Users", 
                  command=self.refresh_users).pack(side='left', padx=5)
        
        # History display
        history_frame = ttk.LabelFrame(main_frame, text="BMI History")
        history_frame.pack(fill='both', expand=True, pady=10)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, 
                                                     width=80, height=20,
                                                     font=('Arial', 9))
        self.history_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.history_text.config(state='disabled')
        
        # Load users initially
        self.refresh_users()
    
    def setup_stats_tab(self):
        """Setup the statistics tab"""
        # Main frame
        main_frame = ttk.Frame(self.stats_tab)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # User selection for stats
        stats_user_frame = ttk.Frame(main_frame)
        stats_user_frame.pack(fill='x', pady=10)
        
        ttk.Label(stats_user_frame, text="Select User for Statistics:").pack(side='left', padx=5)
        self.stats_user_var = tk.StringVar()
        self.stats_user_combo = ttk.Combobox(stats_user_frame, 
                                           textvariable=self.stats_user_var,
                                           state='readonly', width=20)
        self.stats_user_combo.pack(side='left', padx=5)
        
        ttk.Button(stats_user_frame, text="Generate Chart", 
                  command=self.generate_stats).pack(side='left', padx=10)
        
        # Chart frame
        self.chart_frame = ttk.Frame(main_frame)
        self.chart_frame.pack(fill='both', expand=True, pady=10)
        
        # Load users for stats
        self.refresh_stats_users()
    
    def calculate_bmi_gui(self):
        """Calculate BMI from GUI inputs"""
        username = self.username_entry.get().strip()
        weight = self.weight_entry.get().strip()
        height = self.height_entry.get().strip()
        
        if not username:
            messagebox.showerror("Input Error", "Please enter a username")
            return
        
        # Validate input
        is_valid, message = self.calculator.validate_input(weight, height)
        if not is_valid:
            messagebox.showerror("Input Error", message)
            return
        
        # Calculate BMI
        bmi = self.calculator.calculate_bmi(weight, height)
        if bmi is None:
            messagebox.showerror("Calculation Error", "Error calculating BMI. Please check your inputs.")
            return
        
        category = self.calculator.classify_bmi(bmi)
        
        # Save to database
        success = self.calculator.save_to_database(username, weight, height, bmi, category)
        
        # Display result
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        
        result = f"Username: {username}\n"
        result += f"Weight: {weight} kg\n"
        result += f"Height: {height} m\n"
        result += f"BMI: {bmi}\n"
        result += f"Category: {category}\n"
        result += f"Data saved: {'Yes' if success else 'No'}"
        
        self.result_text.insert('1.0', result)
        self.result_text.config(state='disabled')
        
        # Refresh user lists
        self.refresh_users()
        self.refresh_stats_users()
    
    def clear_entries(self):
        """Clear all input fields"""
        self.username_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.config(state='disabled')
    
    def refresh_users(self):
        """Refresh the list of users in the history tab"""
        users = self.calculator.get_all_users()
        self.user_combo['values'] = users
        if users:
            self.user_var.set(users[0])
    
    def refresh_stats_users(self):
        """Refresh the list of users in the stats tab"""
        users = self.calculator.get_all_users()
        self.stats_user_combo['values'] = users
        if users:
            self.stats_user_var.set(users[0])
    
    def load_user_history(self):
        """Load and display user history"""
        username = self.user_var.get()
        if not username:
            messagebox.showerror("Selection Error", "Please select a user")
            return
        
        records = self.calculator.get_user_history(username)
        
        self.history_text.config(state='normal')
        self.history_text.delete('1.0', tk.END)
        
        if not records:
            self.history_text.insert('1.0', f"No records found for user: {username}")
        else:
            header = f"BMI History for: {username}\n"
            header += "-" * 80 + "\n"
            header += f"{'Date/Time':<20} {'Weight (kg)':<12} {'Height (m)':<12} {'BMI':<8} {'Category':<15}\n"
            header += "-" * 80 + "\n"
            self.history_text.insert('1.0', header)
            
            for i, record in enumerate(records):
                timestamp, weight, height, bmi, category = record
                # Format timestamp for better readability
                formatted_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
                line = f"{formatted_time:<20} {weight:<12} {height:<12} {bmi:<8} {category:<15}\n"
                self.history_text.insert(tk.END, line)
        
        self.history_text.config(state='disabled')
    
    def generate_stats(self):
        """Generate BMI trend chart for selected user"""
        username = self.stats_user_var.get()
        if not username:
            messagebox.showerror("Selection Error", "Please select a user")
            return
        
        records = self.calculator.get_user_history(username)
        if not records:
            messagebox.showinfo("No Data", f"No records found for user: {username}")
            return
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Prepare data for chart
        dates = []
        bmis = []
        weights = []
        
        for record in reversed(records):  # Reverse to show chronological order
            timestamp, weight, height, bmi, category = record
            dates.append(timestamp)
            bmis.append(bmi)
            weights.append(float(weight))
        
        # Create matplotlib figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        
        # Plot BMI trend
        ax1.plot(dates, bmis, 'b-o', linewidth=2, markersize=4)
        ax1.set_title(f'BMI Trend for {username}')
        ax1.set_ylabel('BMI')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Add BMI category lines
        ax1.axhline(y=18.5, color='green', linestyle='--', alpha=0.5, label='Underweight/Normal')
        ax1.axhline(y=25, color='orange', linestyle='--', alpha=0.5, label='Normal/Overweight')
        ax1.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='Overweight/Obese')
        ax1.legend()
        
        # Rotate x-axis labels for better readability
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Plot weight trend
        ax2.plot(dates, weights, 'g-o', linewidth=2, markersize=4)
        ax2.set_title(f'Weight Trend for {username}')
        ax2.set_ylabel('Weight (kg)')
        ax2.grid(True, linestyle='--', alpha=0.7)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

def command_line_bmi():
    """Simple command-line BMI calculator for beginners"""
    print("=== BMI Calculator (Command Line) ===")
    print("Enter your details to calculate BMI")
    
    while True:
        try:
            weight = float(input("Enter your weight in kg: "))
            height = float(input("Enter your height in meters: "))
            
            if weight <= 0 or height <= 0:
                print("Error: Weight and height must be positive numbers.\n")
                continue
            
            calculator = BMICalculator()
            bmi = calculator.calculate_bmi(weight, height)
            category = calculator.classify_bmi(bmi)
            
            print(f"\n--- Results ---")
            print(f"Weight: {weight} kg")
            print(f"Height: {height} m")
            print(f"BMI: {bmi}")
            print(f"Category: {category}")
            print("----------------\n")
            
        except ValueError:
            print("Error: Please enter valid numbers.\n")
        
        again = input("Calculate another BMI? (y/n): ").lower()
        if again != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        command_line_bmi()
    else:
        root = tk.Tk()
        app = BMICalculatorGUI(root)
        root.mainloop()