import tkinter as tk
from tkinter import messagebox, filedialog
from faker import Faker
from openpyxl import Workbook

# Initialize Faker generator
fake = Faker()

def generate_data():
    try:
        # Get the selected data type and number of rows
        data_type = var.get()
        num_rows = int(entry.get())

        if num_rows <= 0:
            raise ValueError("Number of rows must be greater than zero.")

        # Update status
        status_label.config(text="Generating data...")
        root.update_idletasks()

        # Generate fake data
        data = []
        if data_type == "name":
            data = [[fake.name()] for _ in range(num_rows)]
        elif data_type == "address":
            data = [[fake.address().replace("\n", ", ")] for _ in range(num_rows)]
        elif data_type == "email":
            data = [[fake.email()] for _ in range(num_rows)]
        elif data_type == "phone":
            data = [[fake.phone_number()] for _ in range(num_rows)]
        else:
            raise ValueError("Invalid data type selected.")

        # Save dialog for Excel file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"fake_{data_type}_data.xlsx"
        )

        if not file_path:
            status_label.config(text="Save canceled.")
            return

        # Create workbook and write data
        wb = Workbook()
        ws = wb.active
        ws.title = "Fake Data"
        ws.append([data_type.capitalize()])  # Header
        for row in data:
            ws.append(row)

        wb.save(file_path)

        print(f"Data saved successfully to {file_path}")
        messagebox.showinfo("Success", f"Data saved to {file_path}")
        status_label.config(text="Data saved successfully.")

    except ValueError as ve:
        print(f"ValueError: {ve}")
        messagebox.showerror("Error", str(ve))
        status_label.config(text="Error occurred.")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        status_label.config(text="Unexpected error.")

# Create the main window
root = tk.Tk()
root.title("Fake Data Generator")
root.geometry("400x350")

# Label and Entry for number of rows
tk.Label(root, text="Enter the number of rows:").pack(pady=10)
entry = tk.Entry(root)
entry.pack()

# Radio buttons for data type selection
var = tk.StringVar(value="name")
tk.Label(root, text="Select data type:").pack(pady=10)

tk.Radiobutton(root, text="Names", variable=var, value="name").pack(anchor=tk.W)
tk.Radiobutton(root, text="Addresses", variable=var, value="address").pack(anchor=tk.W)
tk.Radiobutton(root, text="Emails", variable=var, value="email").pack(anchor=tk.W)
tk.Radiobutton(root, text="Phone Numbers", variable=var, value="phone").pack(anchor=tk.W)

# Button to generate data
tk.Button(root, text="Generate Data", command=generate_data).pack(pady=20)

# Status label
status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

# Run the app
root.mainloop()
