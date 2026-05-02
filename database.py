import sqlite3

def connect_db():
    con = sqlite3.connect('hotel.db')
    con.execute('PRAGMA foreign_keys = ON')
    return con

def create_tables():
    con = connect_db()
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_num INTEGER PRIMARY KEY,
            price REAL,
            type TEXT,
            assigned INTEGER,
            occupied INTEGER,
            clean INTEGER
        )
        ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY,
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
        ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            is_admin INTEGER
        )
        ''')
    
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

    query = cur.execute('SELECT room_num FROM rooms')
    room_list = [r[0] for r in query.fetchall()]
        
    for room in rooms:
        if room[0] not in room_list:
            cur.execute('INSERT INTO rooms VALUES(?, ?, ?, ?, ?, ?)', room)

    con.commit()
    con.close()

def get_rooms(Room):
    con = connect_db()
    cur = con.cursor()

    rooms = {}
    for room in cur.execute('SELECT * from rooms').fetchall():
        room_num = room[0]
        price = room[1]
        r_type = room[2]

        rooms[room_num] = Room(room_num, price, r_type)
        rooms[room_num].assigned = bool(room[3])
        rooms[room_num].occupied = bool(room[4])
        rooms[room_num].clean = bool(room[5])
    return rooms