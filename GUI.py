# This is the code I have so far this is using the information provided in the classes.py 
# This code all creates just one window so far and it allows you to create a reservation, store it, check in, and check out.
# Later on I plan to make it to where you can have multiple windows and integrate SQL to store all this information in a database. 



import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

# -------------------- ROOM CLASS -------------------- #
class Room:
    def __init__(self, number: int, price: float, r_type: str):
        self.number = number
        self.price = price
        self.type = r_type
        self.assigned = False
        self.occupied = False
        self.clean = True

    def _set_clean(self):
        self.clean = True


# -------------------- RESERVATION CLASS -------------------- #
class Reservation:
    def __init__(self, rooms):
        self.rooms = rooms
        self.room = None
        self.guest_name = ""
        self.guest_number = ""
        self.guest_email = ""
        self.checkin_date = date.today()
        self.checkout_date = date.today()
        self.nights = 0
        self.payment_type = 'Cash'
        self.payments = ['Cash', 'Credit Card', 'Debit Card', 'Bill']
        self.status = 'In Progress'
        self.price = 0.0
        self.total = 0.0
        
    # ----------- Public Methods ----------- #
    def Create(self, room_num, guest_name, guest_number,
               guest_email, checkin_date, checkout_date, payment_type):
        self._add_room(room_num)
        self.price = self.room.price
        self._add_name(guest_name)
        self._add_number(guest_number)
        self._add_email(guest_email)
        self._set_checkin(checkin_date)
        self._set_checkout(checkout_date)
        self._get_nights()
        self._set_payment(payment_type)
        self.status = 'Confirmed'
        self.total = self.nights * self.price

    def Cancel(self):
        self.status = 'Cancelled'
        if self.room:
            self.room.assigned = False

    def Checkin(self):
        if self.room is None:
            raise ValueError('No room assigned.')
        if not self.room.clean:
            raise ValueError('Assigned room not clean.')
        self.status = 'In House'
        self.room.occupied = True

    def Checkout(self):
        self.status = 'Out'
        if self.room:
            self.room.assigned = False
            self.room.clean = False
            self.room.occupied = False

    def Confirm(self):
        """Generate a confirmation text file."""
        if self.status != 'Confirmed':
            raise ValueError("Reservation must be confirmed first.")

        filename = f"Confirmation_Room{self.room.number}_{self.guest_name}.txt"
        with open(filename, "w") as f:
            f.write("HOTEL RESERVATION CONFIRMATION\n")
            f.write("-" * 40 + "\n")
            f.write(f"Guest Name: {self.guest_name}\n")
            f.write(f"Phone: {self.guest_number}\n")
            f.write(f"Email: {self.guest_email}\n")
            f.write(f"Room Number: {self.room.number}\n")
            f.write(f"Room Type: {self.room.type}\n")
            f.write(f"Check-in: {self.checkin_date}\n")
            f.write(f"Check-out: {self.checkout_date}\n")
            f.write(f"Nights: {self.nights}\n")
            f.write(f"Price per Night: ${self.price:.2f}\n")
            f.write(f"Total Cost: ${self.total:.2f}\n")
            f.write(f"Payment Type: {self.payment_type}\n")
            f.write("-" * 40 + "\n")
            f.write("Thank you for choosing our hotel!\n")
        return filename

    def Receipt(self):
        """Generate a receipt text file."""
        if self.status not in ['In House', 'Out']:
            raise ValueError("Guest must be checked in or out to generate a receipt.")

        filename = f"Receipt_Room{self.room.number}_{self.guest_name}.txt"
        with open(filename, "w") as f:
            f.write("HOTEL PAYMENT RECEIPT\n")
            f.write("-" * 40 + "\n")
            f.write(f"Guest Name: {self.guest_name}\n")
            f.write(f"Room Number: {self.room.number}\n")
            f.write(f"Stay: {self.checkin_date} to {self.checkout_date}\n")
            f.write(f"Nights: {self.nights}\n")
            f.write(f"Total Paid: ${self.total:.2f}\n")
            f.write(f"Payment Method: {self.payment_type}\n")
            f.write(f"Status: {self.status}\n")
            f.write("-" * 40 + "\n")
            f.write("We appreciate your stay with us!\n")
        return filename

    # ----------- Helper Methods ----------- #
    def _add_room(self, room_number):
        if room_number not in self.rooms:
            raise ValueError('Not a valid room number.')
        room = self.rooms[room_number]
        if room.assigned:
            raise ValueError('Room already assigned.')
        self.room = room
        room.assigned = True

    def _add_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError('Not a valid name.')
        self.guest_name = name.strip()

    def _add_number(self, number):
        if not isinstance(number, str) or not number.strip():
            raise ValueError('Not a valid phone number.')
        self.guest_number = number.strip()

    def _add_email(self, email):
        if not isinstance(email, str) or '@' not in email:
            raise ValueError('Not a valid email address.')
        self.guest_email = email.strip()

    def _set_checkin(self, checkin):
        if not isinstance(checkin, date):
            raise ValueError('Not a valid check-in date.')
        self.checkin_date = checkin

    def _set_checkout(self, checkout):
        if not isinstance(checkout, date):
            raise ValueError('Not a valid check-out date.')
        self.checkout_date = checkout

    def _get_nights(self):
        nights = (self.checkout_date - self.checkin_date).days
        if nights <= 0:
            raise ValueError('Checkout must be after check-in.')
        self.nights = nights

    def _set_payment(self, payment):
        if payment not in self.payments:
            raise ValueError('Payment type not valid.')
        self.payment_type = payment


# -------------------- ROOMS DATA -------------------- #
rooms = {
    101: Room(101, 80.00, 'QQ'),
    102: Room(102, 80.00, 'QQ'),
    103: Room(103, 80.00, 'QQ'),
    104: Room(104, 80.00, 'QQ'),
    105: Room(105, 80.00, 'QQ'),
    106: Room(106, 80.00, 'QQ'),
    201: Room(201, 90.00, 'K'),
    202: Room(202, 90.00, 'K'),
    203: Room(203, 90.00, 'K'),
    204: Room(204, 90.00, 'K'),
    205: Room(205, 90.00, 'K'),
    206: Room(206, 90.00, 'K')
}

# Create a reservation instance
current_reservation = Reservation(rooms)

# -------------------- GUI FUNCTIONS -------------------- #
def update_room_list():
    available = [num for num, room in rooms.items() if not room.assigned]
    room_combo['values'] = available
    if available:
        room_var.set(available[0])
    else:
        room_var.set("")

def create_reservation():
    try:
        room_num = int(room_var.get())
        checkin = datetime.strptime(checkin_entry.get(), "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout_entry.get(), "%Y-%m-%d").date()

        current_reservation.Create(
            room_num,
            name_entry.get(),
            phone_entry.get(),
            email_entry.get(),
            checkin,
            checkout,
            payment_var.get()
        )

        messagebox.showinfo(
            "Success",
            f"Reservation confirmed!\nTotal: ${current_reservation.total:.2f}"
        )
        update_room_list()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def cancel_reservation():
    try:
        current_reservation.Cancel()
        messagebox.showinfo("Cancelled", "Reservation cancelled.")
        update_room_list()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def checkin_guest():
    try:
        current_reservation.Checkin()
        messagebox.showinfo("Check-in", "Guest checked in.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def checkout_guest():
    try:
        current_reservation.Checkout()
        messagebox.showinfo("Check-out", "Guest checked out.")
        update_room_list()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_confirmation():
    try:
        filename = current_reservation.Confirm()
        messagebox.showinfo("Confirmation", f"Created: {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_receipt():
    try:
        filename = current_reservation.Receipt()
        messagebox.showinfo("Receipt", f"Created: {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------- GUI LAYOUT -------------------- #
root = tk.Tk()
root.title("Hotel Booking System")
root.geometry("500x550")
root.resizable(False, False)

title = tk.Label(root, text="Hotel Booking System",
                 font=("Helvetica", 18, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(padx=20, pady=10)

labels = [
    "Guest Name", "Phone Number", "Email",
    "Room Number", "Check-in (YYYY-MM-DD)",
    "Check-out (YYYY-MM-DD)", "Payment Type"
]

for i, text in enumerate(labels):
    tk.Label(frame, text=text).grid(row=i, column=0, sticky="w", pady=5)

name_entry = tk.Entry(frame)
phone_entry = tk.Entry(frame)
email_entry = tk.Entry(frame)

room_var = tk.StringVar()
room_combo = ttk.Combobox(frame, textvariable=room_var, state="readonly")

checkin_entry = tk.Entry(frame)
checkin_entry.insert(0, date.today().strftime("%Y-%m-%d"))

checkout_entry = tk.Entry(frame)
checkout_entry.insert(0, date.today().strftime("%Y-%m-%d"))

payment_var = tk.StringVar(value="Cash")
payment_combo = ttk.Combobox(
    frame,
    textvariable=payment_var,
    values=current_reservation.payments,
    state="readonly"
)

widgets = [
    name_entry, phone_entry, email_entry,
    room_combo, checkin_entry, checkout_entry,
    payment_combo
]

for i, widget in enumerate(widgets):
    widget.grid(row=i, column=1, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

buttons = [
    ("Create Reservation", create_reservation, "#4CAF50"),
    ("Cancel Reservation", cancel_reservation, "#F44336"),
    ("Check In", checkin_guest, "#2196F3"),
    ("Check Out", checkout_guest, "#9C27B0"),
    ("Generate Confirmation", generate_confirmation, None),
    ("Generate Receipt", generate_receipt, None)
]

for i, (text, cmd, color) in enumerate(buttons):
    tk.Button(
        button_frame,
        text=text,
        command=cmd,
        width=25,
        bg=color if color else None,
        fg="white" if color else None
    ).grid(row=i, column=0, pady=5)

update_room_list()
root.mainloop()
