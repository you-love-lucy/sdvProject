from datetime import date, datetime
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3




def connect_db():
    con = sqlite3.connect("hotel.db")
    con.execute("PRAGMA foreign_keys = ON")
    return con




def create_tables():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_num INTEGER PRIMARY KEY,
            price REAL,
            type TEXT,
            assigned INTEGER,
            occupied INTEGER,
            clean INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_num INTEGER,
            guest_name TEXT,
            guest_number TEXT,
            guest_email TEXT,
            checkin_date TEXT,
            checkout_date TEXT,
            nights INTEGER,
            payment_type TEXT,
            status TEXT,
            price REAL,
            FOREIGN KEY(room_num) REFERENCES rooms(room_num)
        )
    """)

    con.commit()
    con.close()


def insert_rooms():
    con = connect_db()
    cur = con.cursor()

    rooms = [
        (101, 80.00, 'QQ', 0, 0, 1),
        (102, 80.00, 'QQ', 0, 0, 1),
        (103, 80.00, 'QQ', 0, 0, 1),
        (104, 80.00, 'QQ', 0, 0, 1),
        (105, 80.00, 'QQ', 0, 0, 1),
        (106, 80.00, 'QQ', 0, 0, 1),
        (201, 90.00, 'K', 0, 0, 1),
        (202, 90.00, 'K', 0, 0, 1),
        (203, 90.00, 'K', 0, 0, 1),
        (204, 90.00, 'K', 0, 0, 1),
        (205, 90.00, 'K', 0, 0, 1),
        (206, 90.00, 'K', 0, 0, 1)
    ]

    existing = cur.execute("SELECT room_num FROM rooms").fetchall()
    existing = [r[0] for r in existing]

    for r in rooms:
        if r[0] not in existing:
            cur.execute("INSERT INTO rooms VALUES (?, ?, ?, ?, ?, ?)", r)

    con.commit()
    con.close()


def get_rooms(Room):
    con = connect_db()
    cur = con.cursor()

    rooms = {}

    for r in cur.execute("SELECT * FROM rooms"):
        rooms[r[0]] = Room(r[0], r[1], r[2])
        rooms[r[0]].assigned = bool(r[3])

    con.close()
    return rooms




class Room:
    def __init__(self, number, price, room_type):
        self.number = number
        self.price = price
        self.type = room_type
        self.assigned = False




class Reservation:
    def __init__(self):
        self.rooms = get_rooms(Room)
        self.room = None
        self.nights = 0
        self.price = 0
        self.total = 0

    def Create(self, room_num, name, phone, email, checkin, checkout, payment):

        if room_num not in self.rooms:
            raise ValueError("Invalid room")

        self.room = self.rooms[room_num]

        if self.room.assigned:
            raise ValueError("Room already booked")

        self.price = self.room.price

        self.nights = (checkout - checkin).days
        if self.nights <= 0:
            raise ValueError("Invalid dates")

        self.total = self.nights * self.price

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO reservations (
                room_num, guest_name, guest_number, guest_email,
                checkin_date, checkout_date, nights,
                payment_type, status, price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            room_num, name, phone, email,
            str(checkin), str(checkout),
            self.nights, payment,
            "Confirmed", self.total
        ))

        cur.execute(
            "UPDATE rooms SET assigned=1 WHERE room_num=?",
            (room_num,)
        )

        con.commit()
        con.close()




create_tables()
insert_rooms()


# =====================================================
# GUI FUNCTIONS
# =====================================================

def save_reservation():
    try:
        res = Reservation()

        res.Create(
            int(room_var.get()),
            name_entry.get(),
            phone_entry.get(),
            email_entry.get(),
            datetime.strptime(checkin_entry.get(), "%Y-%m-%d").date(),
            datetime.strptime(checkout_entry.get(), "%Y-%m-%d").date(),
            payment_var.get()
        )

        messagebox.showinfo("Success", "Reservation Created")

        clear_fields()
        show_reservations()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    checkin_entry.delete(0, tk.END)
    checkout_entry.delete(0, tk.END)


def cancel_reservation():
    rid = cancel_entry.get()

    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT room_num FROM reservations WHERE id=?", (rid,))
    row = cur.fetchone()

    if not row:
        messagebox.showerror("Error", "Not found")
        return

    cur.execute(
        "UPDATE reservations SET status='Cancelled' WHERE id=?",
        (rid,)
    )

    cur.execute(
        "UPDATE rooms SET assigned=0 WHERE room_num=?",
        (row[0],)
    )

    con.commit()
    con.close()

    messagebox.showinfo("Cancelled", "Reservation Cancelled")


def show_reservations():
    top = tk.Toplevel(root)
    top.title("Reservations")
    top.geometry("900x400")

    tree = ttk.Treeview(
        top,
        columns=("ID","Room","Name","Phone","Email","In","Out","N","Pay","Status","Total"),
        show="headings"
    )

    for c in tree["columns"]:
        tree.heading(c, text=c)
        tree.column(c, width=80)

    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM reservations")
    for r in cur.fetchall():
        tree.insert("", tk.END, values=r)

    con.close()

    tree.pack(fill="both", expand=True)

# Create main application window
root = tk.Tk()

# Set window title
root.title("Hotel Booking System")

# Set window size
root.geometry("550x650")

# Set background color
root.configure(bg="black")

# Prevent resizing window
root.resizable(False, False)


# ---------------- TITLE LABEL ----------------
# Displays main system title at top of window
tk.Label(
    root,
    text="Hotel Booking System",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="black"
).pack(pady=10)


# ---------------- INPUT FRAME ----------------
# Holds all user input fields in a structured layout
frame = tk.Frame(root, bg="black")
frame.pack()


# Labels for input fields
labels = [
    "Name",
    "Phone",
    "Email",
    "Room",
    "Check-in (YYYY-MM-DD)",
    "Check-out (YYYY-MM-DD)",
    "Payment"
]


# Create labels in GUI
for i, text in enumerate(labels):
    tk.Label(frame, text=text, fg="white", bg="black").grid(row=i, column=0, sticky="w")


# ---------------- ENTRY FIELDS ----------------
# User input fields for guest information

name_entry = tk.Entry(frame)
phone_entry = tk.Entry(frame)
email_entry = tk.Entry(frame)
checkin_entry = tk.Entry(frame)
checkout_entry = tk.Entry(frame)


# Room dropdown selection
room_var = tk.StringVar()
room_combo = ttk.Combobox(
    frame,
    textvariable=room_var,
    values=list(get_rooms(Room).keys()),
    state="readonly"
)


# Payment dropdown selection
payment_var = tk.StringVar(value="Cash")
payment_combo = ttk.Combobox(
    frame,
    textvariable=payment_var,
    values=["Cash", "Credit Card", "Debit Card", "Bill"],
    state="readonly"
)


# Place input widgets in grid layout
widgets = [
    name_entry,
    phone_entry,
    email_entry,
    room_combo,
    checkin_entry,
    checkout_entry,
    payment_combo
]

for i, w in enumerate(widgets):
    w.grid(row=i, column=1)


# ---------------- BUTTONS ----------------

# Creates reservation using input data
tk.Button(
    root,
    text="Create Reservation",
    command=save_reservation
).pack(pady=10)


# Opens reservation table window
tk.Button(
    root,
    text="View Reservations",
    command=show_reservations
).pack()


# ---------------- CANCEL SECTION ----------------
# Input field to cancel reservation by ID

cancel_entry = tk.Entry(root)
cancel_entry.pack(pady=10)


# Cancel reservation button
tk.Button(
    root,
    text="Cancel Reservation",
    command=cancel_reservation
).pack()


# ---------------- START APP ----------------
root.mainloop()
