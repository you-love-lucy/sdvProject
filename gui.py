import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# -------------------- DATABASE SETUP -------------------- #
# This section creates/connects to the SQLite database file
# and creates the reservations table if it does not already exist.
conn = sqlite3.connect("hotel_bookings.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_name TEXT,
    phone TEXT,
    email TEXT,
    room_number INTEGER,
    checkin_date TEXT,
    checkout_date TEXT,
    payment_type TEXT,
    total REAL,
    status TEXT
)
""")
conn.commit()


# -------------------- ROOM CLASS -------------------- #
# This class is used to create room objects and store
# room number, room price, room type, and booking status.
class Room:
    def __init__(self, number, price, room_type):
        self.number = number
        self.price = price
        self.type = room_type
        self.assigned = False


# This dictionary stores all available hotel rooms
# with their room number, price, and room type.
rooms = {
    101: Room(101, 80.00, "QQ"),
    102: Room(102, 80.00, "QQ"),
    201: Room(201, 90.00, "K"),
    202: Room(202, 90.00, "K")
}

# This list contains all payment methods available
# for the customer to choose from.
payments = ["Cash", "Credit Card", "Debit Card", "Bill"]


# -------------------- FUNCTIONS -------------------- #
# These functions handle reservation actions like saving,
# cancelling, and displaying stored reservations.

# This function shows a message when a reservation is cancelled.
# It can later be expanded to remove data from the database.
def cancel_reservation():
    messagebox.showinfo("Cancelled", "Reservation Cancelled Successfully")


# This function collects user input, validates the form,
# calculates total cost, and saves the reservation into SQL.
def save_reservation():
    try:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        room = int(room_var.get())
        payment = payment_var.get()

        checkin = datetime.strptime(checkin_entry.get(), "%Y-%m-%d")
        checkout = datetime.strptime(checkout_entry.get(), "%Y-%m-%d")

        if not name or not phone or not email:
            messagebox.showerror("Error", "Please fill in all guest details.")
            return

        nights = (checkout - checkin).days
        if nights <= 0:
            messagebox.showerror("Error", "Checkout must be after check-in.")
            return

        total = nights * rooms[room].price

        cursor.execute("""
            INSERT INTO reservations (
                guest_name, phone, email, room_number,
                checkin_date, checkout_date,
                payment_type, total, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            email,
            room,
            checkin_entry.get(),
            checkout_entry.get(),
            payment,
            total,
            "Confirmed"
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Reservation Saved!\n\nGuest: {name}\nRoom: {room}\nTotal: ${total}"
        )

        show_reservations_window()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------- SECOND WINDOW -------------------- #
# This section opens a second window that displays all
# saved reservations from the SQL database in a table.
# This function opens a new window and displays all saved
# reservations using a Treeview table from the database.
def show_reservations_window():
    top = tk.Toplevel(root)
    top.title("Stored Reservations")
    top.geometry("900x400")
    top.configure(bg="black")

    tk.Label(
        top,
        text="Stored Reservations",
        font=("Helvetica", 16, "bold"),
        bg="black",
        fg="white"
    ).pack(pady=10)

    columns = (
        "ID", "Guest", "Phone", "Email", "Room",
        "Check-in", "Check-out", "Payment", "Total", "Status"
    )

    tree = ttk.Treeview(top, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True, padx=10, pady=10)


# -------------------- GUI -------------------- #
# This section builds the main hotel booking interface,
# including labels, input boxes, dropdowns, and buttons.
root = tk.Tk()
root.title("Hotel Booking System")
root.geometry("500x550")
root.configure(bg="black")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("default")

style.configure(
    "TCombobox",
    fieldbackground="black",
    background="black",
    foreground="white"
)


tk.Label(
    root,
    text="Hotel Booking System",
    font=("Helvetica", 18, "bold"),
    bg="black",
    fg="white"
).pack(pady=10)

frame = tk.Frame(root, bg="black")
frame.pack(padx=20, pady=10)

labels = [
    "Guest Name",
    "Phone Number",
    "Email",
    "Room Number",
    "Check-in (YYYY-MM-DD)",
    "Check-out (YYYY-MM-DD)",
    "Payment Type"
]

for i, text in enumerate(labels):
    tk.Label(
        frame,
        text=text,
        bg="black",
        fg="white"
    ).grid(row=i, column=0, sticky="w", pady=5)

name_entry = tk.Entry(frame, bg="black", fg="white", insertbackground="white")
phone_entry = tk.Entry(frame, bg="black", fg="white", insertbackground="white")
email_entry = tk.Entry(frame, bg="black", fg="white", insertbackground="white")
checkin_entry = tk.Entry(frame, bg="black", fg="white", insertbackground="white")
checkout_entry = tk.Entry(frame, bg="black", fg="white", insertbackground="white")

room_var = tk.StringVar()
room_combo = ttk.Combobox(
    frame,
    textvariable=room_var,
    values=list(rooms.keys()),
    state="readonly"
)

payment_var = tk.StringVar(value="Cash")
payment_combo = ttk.Combobox(
    frame,
    textvariable=payment_var,
    values=payments,
    state="readonly"
)

widgets = [
    name_entry,
    phone_entry,
    email_entry,
    room_combo,
    checkin_entry,
    checkout_entry,
    payment_combo
]

for i, widget in enumerate(widgets):
    widget.grid(row=i, column=1, pady=5)


tk.Button(
    root,
    text="Create Reservation",
    command=save_reservation,
    width=25,
    bg="white",
    fg="black"
).pack(pady=20)


tk.Button(
    root,
    text="Cancel Reservation",
    command=cancel_reservation,
    width=25,
    bg="white",
    fg="black"
).pack(pady=5)


tk.Button(
    root,
    text="View Stored Reservations",
    command=show_reservations_window,
    width=25,
    bg="white",
    fg="black"
).pack()

root.mainloop()

conn.close()
