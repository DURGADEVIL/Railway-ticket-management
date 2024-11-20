from sqlite_context import SqliteConnection
from datetime import datetime


class User:
    def __init__(self, name, password, confirm_password,email,Mobile_number):
        self.name = name
        self.password = password
        self.confirm_password=confirm_password
        self.email=email
        self.Mobile_number= Mobile_number

def insert_admin():
    with SqliteConnection('user.db') as connection:
        cursor=connection.cursor()
        cursor.execute('''INSERT OR REPLACE INTO Registration (name, password, confirm_password,email,Mobile_number,type) VALUES (?,?,?,?,?,?)''',('mird','Admin@123','Admin@123','dd@gmail.com','999999999','ADMIN'))

def insert_new_admin(users):
    with SqliteConnection('user.db') as connection:
        cursor=connection.cursor()
        cursor.execute('''INSERT INTO Registration (name, password, confirm_password,email,Mobile_number,type) VALUES (?,?,?,?,?,?)''',(users.name, users.password, users.confirm_password,users.email, users.Mobile_number, 'ADMIN'))

def create_user_table():
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""create table if not exists Registration (
        id integer primary key AUTOINCREMENT, 
        name text not null,
        password real not null,
        confirm_password real not null,
        email text not null,
        Mobile_number integer, 
        type text not null)""")

def add_user(users):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""insert into Registration (name, password, confirm_password,email,Mobile_number,type) values
        (?, ?, ?,? ,? ,?)""", (users.name, users.password, users.confirm_password,users.email, users.Mobile_number, 'USER'))

def login(name,password):
    with SqliteConnection('user.db') as connection:
        cursor=connection.cursor()
        cursor.execute('''SELECT * FROM Registration WHERE email=? AND password=? ''',(name,password))
        login=cursor.fetchone()
        return login

def get_all_user():
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("select * from Registration")
        employees = cursor.fetchall()
        return employees

class Train:
    def __init__(self,trainid,trainname,from1,to1,date,acseat,sleeperseat,arrivaltime,departuretime,fare):
        self.trainid = trainid
        self.trainname = trainname
        self.from1 = from1
        self.to1=to1
        self.date=date
        self.acseat=acseat
        self.sleeperseat=sleeperseat
        self.arrivaltime=arrivaltime
        self.departuretime=departuretime
        self.fare=fare


def create_train_table():
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""create table if not exists train (
        trainid integer primary key , 
        trainname text not null,
        from1 text not null,
        to1 text not null,
        date date not null,
        acseat integer not null,
        sleeperseat integer not null,
        arrivaltime datetime not null,
        departuretime datetime not null,
        fare integer not null)""")

def add_train(train):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""insert into train values 
        (?, ?, ?,?,?,?,?,?,?,?)""", (train.trainid,train.trainname,train.from1,train.to1,train.date,train.acseat,train.sleeperseat,train.arrivaltime,train.departuretime,train.fare))

def get_all_train():
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("select * from train")
        train = cursor.fetchall()
        return train

def getuser(id):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Registration WHERE email=? and type="USER"''', (id,))
        userinfo=cursor.fetchone()
        return userinfo

def getadmin(id):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Registration WHERE email=? and type="ADMIN"''', (id,))
        userinfo=cursor.fetchone()
        return userinfo

def search(train):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("select * from train where from1=? and to1=? and date>=? ORDER BY date,departuretime",train)
        trains = cursor.fetchall()
        return trains

def update_train(trainid, data):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""update train set trainname=?,from1=?,to1=?,date=?,acseat=?,sleeperseat=?,arrivaltime=?,departuretime=?,fare=? 
        where trainid = ?""", (data['trainname'], data['from1'], data['to1'],data['date'],data['acseat'],data['sleeperseat'], data['arrivaltime'],data['departuretime'],data['fare'],trainid))


def get_train(trainid):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""select * from train where trainid = ?""", (trainid,))
        employee = cursor.fetchone()
        return employee

def delete_train(trainid):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""delete from train where trainid = ?""", (trainid,))

def view_user(trainid):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""select Pname from bookings where trainid = ?""", (trainid,))
        employee = cursor.fetchone()
        return employee

class Booking:
    def __init__(self,pname,page,pgender,pemail,pmobile,nseats,sclass):
        self.pname = pname
        self.page = page
        self.pgender = pgender
        self.pemail=pemail
        self.pmobile=pmobile
        self.nseats=nseats
        self.sclass=sclass

def create_booking_table():
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS bookings (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         userid INTEGER NOT NULL,
         trainid INTEGER NOT NULL,
         Pname TEXT NOT NULL,
         page INTEGER NOT NULL,
         pgender TEXT NOT NULL,
         pemail TEXT NOT NULL,
         pmobile INTEGER NOT NULL,
         nseats INTEGER NOT NUll,
         sclass TEXT NOT NULL,
         fare integer not null,
         b_date TEXT NOT NULL,
         status TEXT NOT NULL DEFAULT "Confirmed",
         FOREIGN KEY(userid) REFERENCES Registration(id),
         FOREIGN KEY(trainid) REFERENCES train(trainid))""")

def addpassenger(passengerl):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT id from Registration where email=?""",(passengerl[4],))
        uid=cursor.fetchone()
        cursor.execute("""SELECT fare from train where trainid=?""",(passengerl[0],))
        fare=cursor.fetchone()
        if passengerl[7].lower()=="ac":
            cursor.execute("select acseat from train where trainid=?",(passengerl[0],))
            seats=cursor.fetchone()
            if int(seats[0])>int(passengerl[6]):
                cursor.execute("""UPDATE train set acseat=acseat-? where trainid=?""",(passengerl[6],passengerl[0]))
                cursor.execute("""INSERT INTO bookings(userid,trainid,pname,page,pgender,pemail,pmobile,nseats,sclass,fare,b_date) 
                        VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (
                uid[0], passengerl[0], passengerl[1], passengerl[2], passengerl[3], passengerl[4], passengerl[5],
                passengerl[6], passengerl[7],int(fare[0])*int(passengerl[6])*2,passengerl[8]))
            else:
                return False

        elif passengerl[7].lower()=="sleeper":
            cursor.execute("select sleeperseat from train where trainid=?", (passengerl[0],))
            seats = cursor.fetchone()
            if int(seats[0]) > int(passengerl[6]):
                cursor.execute("""UPDATE train set sleeperseat=sleeperseat-? where trainid=?""",(passengerl[6],passengerl[0]))
                cursor.execute("""INSERT INTO bookings(userid,trainid,pname,page,pgender,pemail,pmobile,nseats,sclass,fare, b_date) 
                        VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (
                uid[0], passengerl[0], passengerl[1], passengerl[2], passengerl[3], passengerl[4], passengerl[5],
                passengerl[6], passengerl[7],int(fare[0])*int(passengerl[6]),passengerl[8]))
            else:
                return False

        cursor.execute("""SELECT bookings.pname, train.trainid, train.trainname, train.date, train.from1, train.to1, bookings.nseats,
        bookings.sclass, bookings.fare from train join bookings on train.trainid=bookings.trainid where bookings.trainid=?""", (passengerl[0],))
        bdetails=cursor.fetchall()
        return [bdetails[-1]]

def bookdisplay(t_id):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("select trainid,trainname,from1,to1,date from train where trainid=?",(t_id,))
        trains = cursor.fetchall()
        return trains
def get_all_bookings():
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT bookings.id, bookings.pname,bookings.pgender, train.trainid, train.trainname, train.from1, 
        train.to1, train.date, bookings.sclass, bookings.nseats,bookings.fare,bookings.status
         FROM train JOIN bookings ON train.trainid=bookings.trainid """)
        bdetails=cursor.fetchall()
        return bdetails

def get_train_bookings(tid):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT bookings.id, bookings.pname,bookings.pgender
         FROM bookings where trainid =? and status=='Confirmed'  """,(tid,))
        tdetails=cursor.fetchall()
        return tdetails

def delete_booking(bid):
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""select sclass,nseats,status,trainid,b_date from bookings where id=?""",(bid,))
        c_data=cursor.fetchone()
        c_data_f = c_data[4]
        booking_time = datetime.strptime(c_data_f, '%Y-%m-%d %H:%M')
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d %H:%M")
        cancel_time = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        cursor.execute("""select date,departuretime from train where trainid=?""", (c_data[3],))
        d_data = cursor.fetchone()
        d_data_f = d_data[0] + " " + d_data[1]
        departure_time = datetime.strptime(d_data_f, '%Y-%m-%d %H:%M')
        time_difference_booking_departure = departure_time - booking_time
        time_difference_cancel_booking = cancel_time - booking_time
        time_difference_booking_departure_hours = time_difference_booking_departure.total_seconds() / 3600
        time_difference_cancel_booking_hours = time_difference_cancel_booking.total_seconds() / 3600
        if time_difference_cancel_booking_hours < 48:
            rp = 100
        elif 48 <= time_difference_booking_departure_hours < 24 * 7:  # 24 hours * 7 days = 168 hours
            if time_difference_booking_departure_hours < 24:
                rp = 70
            else:
                rp = 40
        else:
            rp = 40

        if c_data[0].lower()=="ac" and c_data[2]=="Confirmed":
            cursor.execute("""UPDATE train set acseat=acseat+? where trainid=?""",(c_data[1],c_data[3]))
            cursor.execute("UPDATE bookings SET status=?,fare=fare-(?/100*fare) where id=?",("Cancelled",rp,bid))
        elif c_data[0].lower()=="sleeper" and c_data[2]=="Confirmed":
            cursor.execute("""UPDATE train set sleeperseat=sleeperseat+? where trainid=?""",(c_data[1],c_data[3]))
            cursor.execute("UPDATE bookings SET status=?,fare=fare-(?/100*fare) where id=?",("Cancelled",rp,bid))


def delte_table():
    with SqliteConnection('user.db') as connection:
        cursor = connection.cursor()
        cursor.execute("drop table bookings")


#delte_table()
create_user_table()
create_train_table()
insert_admin()
create_booking_table()