from datetime import date

'''
To do:
- finish Confirmation() to reservation
- finish Receipt() to reservation
- add Employee object
- add activity reporting (f'{employee} changed {number} to {new_num}) added to a document
- add Employee methods
- add database
- add proper documentation (i hate doing this)
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
        self.rooms = rooms
        self.room = None
        self.guest_email = 'Email'
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
        # add to database

    def Cancel(self):
        self.status = 'Cancelled'
        if self.room:
            self.room.assigned = False
        # remove from database

    def Checkin(self):
        if self.room == None:
            raise ValueError('No room assigned.')

        if self.room.clean == False:
            raise ValueError('Assigned room not clean.')
        self.status = 'In House'
        self.room.occupied = True
        # edit in database

    def Checkout(self):
        self.status = 'Out'
        self.room.assigned = False
        self.room.clean = False
        self.room.occupied = False

    def Confirm(self):
        # create confirmation document for guest
        pass

    def Receipt(self):
        # create receipt for guest
        pass

    def _set_status(self, status):
        self.status = status
        # edit in database

    def _add_room(self, room_number):
        if room_number not in self.rooms:
            raise ValueError('Not a valid room.') # if you want me to change this so it's better integrated with the GUI, lmk
        
        if self.rooms[room_number]:
            raise ValueError('Room already assigned.')
        self.room = self.rooms[room_number]
        self.room.assigned = True
        # edit in database

    def _add_price(self, price):
        if type(price) != float:
            raise ValueError('Not a valid price.')
        self.price = price
        # edit in database

    def _add_name(self, name):
        if type(name) != str:
            raise ValueError('Not a valid name.')
        self.guest_name = name
        # edit in database

    def _add_number(self, number):
        if type(number) != str:
            raise ValueError('Not a valid phone number.')
        self.guest_number = number
        # edit in database

    def _add_email(self, email):
        if type(email) != str:
            raise ValueError('Not a valid email address.')
        
        if '@' not in email:
            raise ValueError('Not a valid email address.')
        
        self.guest_email = email
        # edit in database
    
    def _set_checkin(self, checkin):
        if type(checkin) != date:
            raise ValueError('Not a valid date.')
        self.checkin_date = checkin
        # edit in database
    
    def _set_checkout(self, checkout):
        if type(checkout) != date:
            raise ValueError('Not a valid date.')
        self.checkout_date = checkout
        # edit in database

    def _get_nights(self):
        end = self.checkout_date
        start = self.checkin_date
        nights = (end - start).days
        if nights <= 0:
            raise ValueError('Number of nights is not valid. Check dates.')
        self.nights = nights
        # edit in database

    def _set_payment(self, payment):
        if type(payment) != str or payment not in self.payments:
            raise ValueError('Payment type not valid.')
        self.payment_type = payment
    # edit in database

rooms = {
    # feel free to change this, i just needed some placeholder values
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