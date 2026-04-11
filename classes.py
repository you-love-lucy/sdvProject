from datetime import date

'''
To do:
- finish room object and room dictionary w/i reservation object
- finish Checkin() function for reservation object (add editing room status)
- add Checkout() incl. updating room status
- add Confirmation() to reservation
- add Receipt() to reservation
- add Employee object
- add activity reporting (f'{employee} changed {number} to {new_num}) added to a document
- add Employee methods
- add database
'''

class Room:
    def __init__(self, number, price, r_type):
        self.number = number
        self.price = price
        self.type = r_type

class Reservation:
    def __init__(self):
        self.rooms = {
            101: Room()
        }
        self.guest_email = 'Email'
        self.checkin_date = date.today()
        self.checkout_date = date.today()
        self.nights = 0
        self.payment_type = 'Cash'
        self.payments = ['Cash', 'Credit Card', 'Debit Card', 'Bill']
        self.status = 'In Progress'
        self.total = self.nights * self.price
        
    def Create(self, room, price, guest_name, guest_number, guest_email, checkin_date, checkout_date, payment_type):
        self._add_room(room)
        self._add_price(price)
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
        # remove from database

    def Checkin(self):
        self.status = 'In House'
        # edit in database

    def _set_status(self, status):
        self.status = status
        # edit in database

    def _add_room(self, room):
        if room not in self.room_numbers:
            raise ValueError('Not a valid room number.') # if you want me to change this so it's better integrated with the GUI, lmk
        self.room = room
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