from datetime import date
from database import connect_db, create_tables, insert_rooms, get_rooms

log = open('hotelLog.txt', 'a')

'''
To do:
- add proper documentation (i hate doing this)
- add readme
'''

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

class Reservation:
    def __init__(self, rooms):
        self.id = None
        self.rooms = get_rooms(Room)
        self.room = None
        self.checkin_date = date.today()
        self.checkout_date = date.today()
        self.nights = 0
        self.payment_type = 'Cash'
        self.payments = ['Cash', 'Credit Card', 'Debit Card', 'Bill']
        self.status = 'In Progress'
        self.price = 0.0
        self.total = self.nights * self.price
        
    def Create(self, room_num, guest_name, guest_number, guest_email, checkin_date, checkout_date, payment_type):
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

        con = connect_db()
        cur = con.cursor()
        cur.execute('''INSERT INTO reservations (
                        room_num,
                        guest_name,
                        guest_number,
                        guest_email,
                        checkin_date,
                        checkout_date,
                        nights,
                        payment_type,
                        status,
                        price
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        self.room.number,
                        self.guest_name,
                        self.guest_number, 
                        self.guest_email, 
                        str(self.checkin_date),
                        str(self.checkout_date),
                        self.nights,
                        self.payment_type,
                        self.status,
                        self.price
                    ))
        
        self.id = cur.lastrowid

        con.commit()
        con.close()

    def Cancel(self):
        self.status = 'Cancelled'
        if self.room:
            self.room.assigned = False
        self.Save()

    def Checkin(self):
        if self.room == None:
            raise ValueError('No room assigned.')

        if self.room.clean == False:
            raise ValueError('Assigned room not clean.')
        self.status = 'In House'
        self.room.occupied = True
        self.Save()

    def Checkout(self):
        self.status = 'Out'
        self.room.assigned = False
        self.room.clean = False
        self.room.occupied = False
        self.Save()

    def Confirm(self):
        if self.id is None:
            return
        conf = open(f'confirmation_{self.id}.txt', 'w')
        conf.write(f'Confirmation {self.id}\n{self.status}\n\n{self.guest_name}\n{self.guest_number}\n{self.guest_email}\n\n\n{self.room.number}\n{self.checkin_date} to {self.checkout_date} ({self.nights} nights)\nPayment type: {self.payment_type}\nTotal: {self.total}')
        conf.close()

    def Receipt(self):
        if self.id is None:
            return
        receipt = open(f'receipt_{self.id}.txt', 'w')
        receipt.write(f'Receipt {self.id}\n\n{self.guest_name}\n{self.guest_number}\n{self.guest_email}\n\n\n{self.room.number}\n{self.checkin_date} to {self.checkout_date} ({self.nights} nights)\nPayment type: {self.payment_type}\nTotal: {self.total}')
        receipt.close()

    def Save(self):
        con = connect_db()
        cur = con.cursor()

        if self.id is None:
            return

        cur.execute('''UPDATE reservations SET
                        room_num = ?,
                        guest_name = ?,
                        guest_number = ?,
                        guest_email = ?,
                        checkin_date = ?,
                        checkout_date = ?,
                        nights = ?,
                        payment_type = ?,
                        status = ?, 
                        price = ?
                    WHERE id = ?''', (
                        self.room.number,
                        self.guest_name,
                        self.guest_number, 
                        self.guest_email, 
                        str(self.checkin_date),
                        str(self.checkout_date),
                        self.nights,
                        self.payment_type,
                        self.status,
                        self.price,
                        self.id
                    ))
        
        self.rooms = get_rooms(Room)

        con.commit()
        con.close()

    def _set_status(self, status):
        self.status = status

    def _add_room(self, room_number):
        if room_number not in self.rooms:
            raise ValueError('Not a valid room.')
        if self.rooms[room_number].assigned:
            raise ValueError('Room already assigned.')
        self.room = self.rooms[room_number]
        self.room.assigned = True

    def _add_price(self, price):
        if type(price) != float:
            raise ValueError('Not a valid price.')
        self.price = price

    def _add_name(self, name):
        if type(name) != str:
            raise ValueError('Not a valid name.')
        self.guest_name = name

    def _add_number(self, number):
        if type(number) != str:
            raise ValueError('Not a valid phone number.')
        self.guest_number = number

    def _add_email(self, email):
        if type(email) != str:
            raise ValueError('Not a valid email address.')
        
        if '@' not in email:
            raise ValueError('Not a valid email address.')
        
        self.guest_email = email
    
    def _set_checkin(self, checkin):
        if type(checkin) != date:
            raise ValueError('Not a valid date.')
        self.checkin_date = checkin
    
    def _set_checkout(self, checkout):
        if type(checkout) != date:
            raise ValueError('Not a valid date.')
        self.checkout_date = checkout

    def _get_nights(self):
        end = self.checkout_date
        start = self.checkin_date
        nights = (end - start).days
        if nights <= 0:
            raise ValueError('Number of nights is not valid. Check dates.')
        self.nights = nights

    def _set_payment(self, payment):
        if type(payment) != str or payment not in self.payments:
            raise ValueError('Payment type not valid.')
        self.payment_type = payment

class Employee:
    def __init__(self, id: int, name: str, is_admin: bool):
        self.id = id
        self.name = name
        self.is_admin = is_admin
    
    def log(self, action: str):
        log.write(f'{date.today()} - {action} - {self.name} - {self.id} \n')

create_tables()
insert_rooms()
log.close()