import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
from PIL import Image, ImageTk

class JSONEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Base Sample_App Creator & Editor")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        # Initialize variables
        self.json_data = {}
        self.file_path = ""
        self.base_path = r"D:\project\poc\jason_data"  # Hardcoded base path

        # Load and display logo
        self.logo = self.load_logo()
        self.create_main_menu()

    def load_logo(self):
        """Load and return the logo image."""
        try:
            image_path = r"D:\project\poc\logo.png"  # Adjust path as needed
            img = Image.open(image_path)
            if img.mode in ("RGBA", "LA"):
                img = img.convert("RGBA")
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading logo: {e}")
            return None

    def display_logo(self, parent):
        """Display the logo on the given parent widget."""
        if self.logo:
            logo_label = tk.Label(parent, image=self.logo, bg="#f0f0f0")
            logo_label.pack(pady=10)

    def create_main_menu(self):
        """Main menu with Create and Edit options."""
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True)

        self.display_logo(main_frame)

        tk.Label(
            main_frame,
            text="Welcome to JSON Base Sample_App Creator & Editor",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)

        tk.Button(
            main_frame,
            text="Create New JSON File",
            font=("Arial", 14),
            width=30,
            command=self.create_new_file,
            bg="#007bff",
            fg="white",
            relief="flat"
        ).pack(pady=10)

        tk.Button(
            main_frame,
            text="Edit Existing JSON File",
            font=("Arial", 14),
            width=30,
            command=self.edit_existing_file,
            bg="#28a745",
            fg="white",
            relief="flat"
        ).pack(pady=10)


    def create_new_file(self):
        """Interface to create a new JSON file."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.json_data = {}  # Initialize empty JSON data

        tk.Label(self.root, text=f"Base Path: {self.base_path}", fg="blue", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

        tk.Label(self.root, text="Enter File Name:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.file_name_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.file_name_entry.pack(pady=5)

        # Key-value entry section
        self.create_fields_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.create_fields_frame.pack(pady=10)

        tk.Label(self.create_fields_frame, text="Key:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.new_key_entry = tk.Entry(self.create_fields_frame, width=20, font=("Arial", 12))
        self.new_key_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.create_fields_frame, text="Value:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.new_value_entry = tk.Entry(self.create_fields_frame, width=20, font=("Arial", 12))
        self.new_value_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(self.create_fields_frame, text="Add Key-Value", font=("Arial", 12), command=self.add_key_value_to_new_file, bg="#ffc107", fg="white", relief="flat", bd=0).grid(row=0, column=4, padx=5, pady=5)

        # Frame to display added key-value pairs
        self.key_value_display_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.key_value_display_frame.pack(pady=10)

        # Save and Back buttons
        tk.Button(self.root, text="Save JSON File", font=("Arial", 12), command=self.save_new_file, bg="#007bff", fg="white", relief="flat", bd=0).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 12), command=self.create_main_menu, bg="#6c757d", fg="white", relief="flat", bd=0).pack(pady=10)

    def add_key_value_to_new_file(self):
        """Add a new key-value pair to the JSON data."""
        new_key = self.new_key_entry.get().strip()
        new_value = self.new_value_entry.get().strip()

        if not new_key:
            messagebox.showerror("Error", "Key cannot be empty.")
            return

        if new_key in self.json_data:
            messagebox.showerror("Error", f"Key '{new_key}' already exists.")
            return

        # Infer data type for the value
        if new_value.isdigit():
            new_value = int(new_value)
        elif new_value.lower() in {"true", "false"}:
            new_value = new_value.lower() == "true"

        # Add to JSON data
        self.json_data[new_key] = new_value

        # Update display
        self.update_key_value_display()

        # Clear input fields
        self.new_key_entry.delete(0, tk.END)
        self.new_value_entry.delete(0, tk.END)

    def update_key_value_display(self):
        """Update the displayed key-value pairs."""
        for widget in self.key_value_display_frame.winfo_children():
            widget.destroy()

        tk.Label(self.key_value_display_frame, text="Added Key-Value Pairs:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)

        for idx, (key, value) in enumerate(self.json_data.items()):
            tk.Label(self.key_value_display_frame, text=f"{key}: {value}", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=10)

    def save_new_file(self):
        """Save the new JSON file to the hardcoded base path."""
        file_name = self.file_name_entry.get().strip()

        if not file_name:
            messagebox.showerror("Error", "File name cannot be empty.")
            return

        file_path = os.path.join(self.base_path, file_name)
        if not file_path.endswith(".json"):
            file_path += ".json"

        try:
            # Save JSON data to the file
            with open(file_path, 'w') as json_file:
                json.dump(self.json_data, json_file, indent=4)

            messagebox.showinfo("Success", f"File saved successfully at {file_path}")

            # Display the JSON content after saving
            self.display_json_file(file_path)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def display_json_file(self, file_path):
        """Display the saved JSON file content."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"File Saved Successfully: {file_path}", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        try:
            with open(file_path, 'r') as json_file:
                json_content = json_file.read()

            # Display the JSON content in a text area
            text_area = tk.Text(self.root, width=80, height=20, font=("Courier New", 10))
            text_area.pack(pady=10)
            text_area.insert(tk.END, json_content)
            text_area.config(state=tk.DISABLED)  # Make it read-only

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open saved JSON file: {e}")

        # Back to Main Menu button
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 12), command=self.create_main_menu, bg="#6c757d", fg="white", relief="flat", bd=0).pack(pady=10)

    def edit_existing_file(self):
        """Interface to edit an existing JSON file."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Base Path: {self.base_path}", fg="blue", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

        # File browsing and loading options
        file_name_frame = tk.Frame(self.root, bg="#f0f0f0")
        file_name_frame.pack(pady=10)

        tk.Label(file_name_frame, text="Enter File Name:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.file_name_entry = tk.Entry(file_name_frame, width=40, font=("Arial", 12))
        self.file_name_entry.grid(row=0, column=1, padx=5)

        tk.Button(file_name_frame, text="Load File", font=("Arial", 12), command=self.load_from_file_name, bg="#ffc107", fg="white", relief="flat", bd=0).grid(row=0, column=2, padx=5)
        tk.Button(file_name_frame, text="Browse File", font=("Arial", 12), command=self.browse_json_file, bg="#007bff", fg="white", relief="flat", bd=0).grid(row=0, column=3, padx=5)

        # JSON editing area
        self.edit_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.edit_frame.pack(pady=10)

        # Save and Back buttons
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 12), command=self.create_main_menu, bg="#6c757d", fg="white", relief="flat", bd=0).pack(pady=10)

    def browse_json_file(self):
        """Browse and load a JSON file."""
        self.file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if self.file_path:
            self.load_json_file()

    def load_from_file_name(self):
        """Load a JSON file using the hardcoded base path and provided file name."""
        file_name = self.file_name_entry.get().strip()

        if not file_name:
            messagebox.showerror("Error", "File name cannot be empty.")
            return

        self.file_path = os.path.join(self.base_path, file_name)

        if not os.path.isfile(self.file_path):
            messagebox.showerror("Error", f"The file '{self.file_path}' does not exist.")
            return

        self.load_json_file()

    def load_json_file(self):
        """Load JSON content and display editing interface."""
        try:
            with open(self.file_path, 'r') as json_file:
                self.json_data = json.load(json_file)

            self.display_json_editor()
            messagebox.showinfo("Success", f"Loaded file: {self.file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open JSON file: {e}")

    def display_json_editor(self):
        """Display JSON keys and values as editable fields."""
        for widget in self.edit_frame.winfo_children():
            widget.destroy()

        self.entries = {}
        for idx, (key, value) in enumerate(self.json_data.items()):
            tk.Label(self.edit_frame, text=key, font=("Arial", 12), bg="#f0f0f0").grid(row=idx, column=0, padx=10, pady=5, sticky="e")

            entry = tk.Entry(self.edit_frame, width=50, font=("Arial", 12))
            entry.insert(0, str(value))
            entry.grid(row=idx, column=1, padx=10, pady=5)

            self.entries[key] = entry

        # Save Changes button
        tk.Button(self.edit_frame, text="Save Changes", font=("Arial", 12), command=self.save_json, bg="#28a745", fg="white", relief="flat", bd=0).grid(row=len(self.json_data) + 1, column=1, pady=10)

    def save_json(self):
        """Save changes to the JSON file."""
        try:
            for key, entry in self.entries.items():
                value = entry.get()
                if value.isdigit():
                    self.json_data[key] = int(value)
                elif value.lower() in {"true", "false"}:
                    self.json_data[key] = value.lower() == "true"
                else:
                    self.json_data[key] = value

            with open(self.file_path, 'w') as json_file:
                json.dump(self.json_data, json_file, indent=4)

            messagebox.showinfo("Success", "JSON file saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON file: {e}")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditorApp(root)
    root.mainloop()
