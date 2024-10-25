import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import pandas as pd

def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_SQL_PASSWORD",
            database="StudentDB"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
        return None

def add_student(first_name, last_name, dob, gender, email, phone):
    if not first_name or not last_name or not dob or not gender or not email or not phone:
        messagebox.showerror("Input Error", "All fields are required!")
        return
    
    if not validate_email(email):
        messagebox.showerror("Input Error", "Invalid email format!")
        return

    if not validate_phone(phone):
        messagebox.showerror("Input Error", "Invalid phone number format!")
        return

    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (first_name, last_name, date_of_birth, gender, email, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, dob, gender, email, phone))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def validate_email(email):
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return phone.isdigit() and len(phone) in [10, 11]

def update_student(student_id, first_name, last_name, dob, gender, email, phone):
    if not first_name or not last_name or not dob or not gender or not email or not phone:
        messagebox.showerror("Input Error", "All fields are required!")
        return
    
    if not validate_email(email):
        messagebox.showerror("Input Error", "Invalid email format!")
        return

    if not validate_phone(phone):
        messagebox.showerror("Input Error", "Invalid phone number format!")
        return

    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE students
            SET first_name = %s, last_name = %s, date_of_birth = %s, gender = %s, email = %s, phone_number = %s
            WHERE student_id = %s
        """, (first_name, last_name, dob, gender, email, phone, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def delete_student(student_id):
    if student_id is None:
        messagebox.showerror("Input Error", "No student selected!")
        return

    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def view_students():
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    view_window = Toplevel()
    view_window.title("View Students")
    view_window.geometry("1800x800")

    tree = ttk.Treeview(view_window, columns=("ID", "First Name", "Last Name", "DOB", "Gender", "Email", "Phone"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("DOB", text="Date of Birth")
    tree.heading("Gender", text="Gender")
    tree.heading("Email", text="Email")
    tree.heading("Phone", text="Phone")

    for record in records:
        tree.insert("", "end", values=record)

    tree.pack(expand=True, fill="both")

    def on_student_select(event):
        selected_item = tree.selection()
        if selected_item:
            student_id = tree.item(selected_item)["values"][0]
            student_details = tree.item(selected_item)["values"][1:]

            update_window = Toplevel()
            update_window.title("Update Student")
            update_window.geometry("400x400")

            entry_style = {'width': 35, 'font': ('Arial', 12)}

            Label(update_window, text="First Name").grid(row=0, column=0, padx=10, pady=10)
            first_name = Entry(update_window, **entry_style)
            first_name.grid(row=0, column=1)
            first_name.insert(0, student_details[0])

            Label(update_window, text="Last Name").grid(row=1, column=0, padx=10, pady=10)
            last_name = Entry(update_window, **entry_style)
            last_name.grid(row=1, column=1)
            last_name.insert(0, student_details[1])

            Label(update_window, text="Date of Birth (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=10)
            dob = Entry(update_window, **entry_style)
            dob.grid(row=2, column=1)
            dob.insert(0, student_details[2])

            Label(update_window, text="Gender").grid(row=3, column=0, padx=10, pady=10)
            gender = ttk.Combobox(update_window, values=["Male", "Female", "Other"], state="readonly", width=32)
            gender.grid(row=3, column=1)
            gender.set(student_details[3])

            Label(update_window, text="Email").grid(row=4, column=0, padx=10, pady=10)
            email = Entry(update_window, **entry_style)
            email.grid(row=4, column=1)
            email.insert(0, student_details[4])

            Label(update_window, text="Phone Number").grid(row=5, column=0, padx=10, pady=10)
            phone = Entry(update_window, **entry_style)
            phone.grid(row=5, column=1)
            phone.insert(0, student_details[5])

            update_btn = Button(update_window, text="Update", command=lambda: update_student(student_id, first_name.get(), last_name.get(), dob.get(), gender.get(), email.get(), phone.get()))
            update_btn.grid(row=6, column=1, pady=20)

            delete_btn = Button(update_window, text="Delete", command=lambda: delete_student(student_id,))
            delete_btn.grid(row=7, column=1, pady=5)

    tree.bind("<<TreeviewSelect>>", on_student_select)

def export_to_excel():
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    if not records:
        messagebox.showinfo("Export Error", "No records to export!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df = pd.DataFrame(records, columns=["ID", "First Name", "Last Name", "DOB", "Gender", "Email", "Phone"])
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Data exported to Excel successfully!")

def add_student_gui():
    root = Tk()
    root.title("Add Student")
    root.geometry("600x450")
    root.resizable(False, False)

    background_image = Image.open("Background_Image_Location")
    background_image = background_image.resize((600, 450), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(background_image)

    bg_label = Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    entry_style = {'width': 35, 'font': ('Arial', 12)}

    Label(root, text="First Name").grid(row=0, column=0, padx=10, pady=10)
    first_name = Entry(root, **entry_style)
    first_name.grid(row=0, column=1)

    Label(root, text="Last Name").grid(row=1, column=0, padx=10, pady=10)
    last_name = Entry(root, **entry_style)
    last_name.grid(row=1, column=1)

    Label(root, text="Date of Birth (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=10)
    dob = Entry(root, **entry_style)
    dob.grid(row=2, column=1)

    Label(root, text="Gender").grid(row=3, column=0, padx=10, pady=10)
    gender = ttk.Combobox(root, values=["Male", "Female", "Other"], state="readonly", width=32)
    gender.grid(row=3, column=1)

    Label(root, text="Email").grid(row=4, column=0, padx=10, pady=10)
    email = Entry(root, **entry_style)
    email.grid(row=4, column=1)

    Label(root, text="Phone Number").grid(row=5, column=0, padx=10, pady=10)
    phone = Entry(root, **entry_style)
    phone.grid(row=5, column=1)

    add_btn = Button(root, text="Add Student", command=lambda: add_student(first_name.get(), last_name.get(), dob.get(), gender.get(), email.get(), phone.get()), bg="lightgreen", width=20)
    add_btn.grid(row=6, column=1, pady=20)

    view_btn = Button(root, text="View Students", command=view_students, bg="lightyellow", width=20)
    view_btn.grid(row=7, column=1, pady=5)

    export_btn = Button(root, text="Export to Excel", command=export_to_excel, bg="lightblue", width=20)
    export_btn.grid(row=8, column=1, pady=5)

    root.mainloop()

add_student_gui()
