from flask import Flask, render_template, request, redirect,session
from model import User,Train ,bookdisplay,add_user,insert_new_admin, getadmin,get_train_bookings,get_train,add_train,getuser, get_all_train,login,delete_train,update_train,search,view_user,addpassenger,get_all_bookings,delete_booking
from datetime import datetime
app = Flask(__name__)


app.secret_key="sprint"


#Home Page
@app.route('/', methods=['GET','POST'])
def Login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        session['name']=name
        loginl=login(name,password)
        if loginl:
            if loginl[6] == "ADMIN":
                return redirect("/a")
            elif loginl[6] == "USER":
                return redirect('/userhome')
        else:
            return redirect('/')
    return render_template('Login.html')

#Add User
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email=request.form['email']
        Mobile_number=request.form['Mobile_number']
        if password == confirm_password:
            if getuser(email) == None:
                obj = User(name, password, confirm_password, email, Mobile_number)
                add_user(obj)
                return redirect("/")
            else:
                data = "Email already exist"
                return render_template('Registration.html', data=data)
        else:
            data1 = "Password must match with above passsword"
            return render_template('Registration.html', data1=data1)

        obj= User(name, password, confirm_password,email, Mobile_number)
        add_user(obj)
        return redirect('/')

    return render_template('Registration.html')

@app.route('/a')
def adminhome():
    if 'name' in session:
        return render_template('ahome.html')
    else:
        return redirect('/a')

#adding admin
@app.route('/addadmin',methods=["GET",'POST'])
def add_admin():
    if 'name' in session:
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            email = request.form['email']
            Mobile_number = request.form['Mobile_number']

            if password == confirm_password:
                if getadmin(email) == None:
                    trains1 = User(name, password, confirm_password, email, Mobile_number)
                    insert_new_admin(trains1)
                    return redirect('/a')
                else:
                    data = "Email already exist"
                    return render_template('addadmin.html', data=data)
            else:
                data1 = "Password must match with above passsword"
                return render_template('addadmin.html', data1=data1)
        return render_template('addadmin.html')



    else:
        return redirect('/a')

@app.route('/addtrain', methods=['GET', 'POST'])
def add__train():
    if 'name' in session:
        if request.method == 'POST':
            trainid = request.form['trainid']
            trainname = request.form['trainname'].capitalize()
            from1 = request.form['from1'].capitalize()
            to1 = request.form['to1'].capitalize()
            date = request.form['date']
            acseat = request.form['acseat']
            sleeperseat = request.form['sleeperseat']
            arrivaltime = request.form['arrivaltime']
            departuretime = request.form['departuretime']
            fare = request.form['fare']

            if from1!=to1:
                trains = Train(trainid,trainname,from1,to1,date,acseat,sleeperseat,arrivaltime,departuretime,fare)
                add_train(trains)
                return redirect('/trainlist')
            else:
                data="Origin and destination cannot be the same"
                return render_template("train register.html", data=data)
            #else:
           # return render_template("confirmation.html", passengers=passengers)

        return render_template('train register.html')
    else:
        return redirect('/')


#get all trains
@app.route('/trainlist')
def list_train():
    if 'name' in session:
        trains = get_all_train()
        return render_template('trainlist.html', trains=trains)
    else:
        return redirect('/')

@app.route('/edit/<int:trainid>', methods=['GET', 'POST'])
def edit(trainid):
    if 'name' in session:
        trains = get_train(trainid)
        if request.method == 'POST':
            employee_data = {
            'trainname' : request.form['trainname'].capitalize(),
            'from1' : request.form['from1'].capitalize(),
            'to1' : request.form['to1'].capitalize(),
            'date' : request.form['date'],
            'acseat' : request.form['acseat'],
            'sleeperseat' : request.form['sleeperseat'],
            'arrivaltime': request.form['arrivaltime'],
            'departuretime': request.form['departuretime'],
            'fare': request.form['fare']
            }

            update_train(trainid, employee_data)
            return redirect('/trainlist')
        return render_template('edit.html', trains=trains)
    else:
        return redirect('/')

@app.route('/delete/<int:trainid>', methods=['POST'])
def delete(trainid):
    if 'name' in session:
        delete_train(trainid)
        trains = get_all_train()
        return render_template('trainlist.html', trains=trains)
    else:
        return redirect('/')

@app.route('/view/<int:trainid>', methods=["GET",'POST'])
def view(trainid):
    if 'name' in session:
        trains = view_user(trainid)
        return render_template('view.html', trains=trains)
    else:
        return redirect('/a')





# Search Train-user home
@app.route('/userhome', methods=['GET', 'POST'])
def searchtrain():
    if 'name' in session:
        trains = get_all_train()
        if request.method == 'POST':
            fromstation=request.form['fromstation'].capitalize()
            tostation = request.form['tostation'].capitalize()
            date = request.form['date']
            train=(fromstation, tostation, date)
            trains=search(train)
            return render_template('userhome.html',trains=trains)
        return render_template('userhome.html',trains=trains)
    else:
        return redirect('/')

#add booking
@app.route('/booking/<int:tid>', methods=['GET','POST'])
def booking(tid):
    if 'name' in session:
        if request.method=='POST':
            pname = request.form['pname']
            page = request.form['page']
            pgender = request.form['pgender']
            pemail = request.form['pemail']
            pmobile = request.form['pmobile']
            nseats = request.form['nseats']
            sclass = request.form['sclass']
            now = datetime.now()
            b_date = now.strftime("%Y-%m-%d %H:%M")
            passengerl=(tid,pname,page,pgender,pemail,pmobile,nseats,sclass,b_date)
            if int(nseats) >0:
                passengers=addpassenger(passengerl)
                if not passengers:
                    data = "Maxium seats reached"
                    display = bookdisplay(tid)
                    return render_template("booking.html", data=data, display=display)
                else:
                    return render_template("confirmation.html", passengers=passengers)

            else:
                data1 = "Seats cannot be zero"
                display = bookdisplay(tid)
                return render_template("booking.html", display=display,data1=data1)

        display = bookdisplay(tid)
        return render_template("booking.html", display=display)
    else:
        return redirect('/')

#booking history
@app.route('/listofbooking')
def listofbooking():
    if 'name' in session:
        bookings = get_all_bookings()
        return render_template('listofbooking.html', bookings=bookings)
    else:
        return redirect('/')

@app.route('/viewadmin/<int:tid>')
def viewbooking(tid):
    if 'name' in session:
        bookings = get_train_bookings(tid)
        return render_template('view.html', bookings=bookings)
    else:
        return redirect('/')

#booking History
@app.route('/deletebooking/<int:bid>', methods=['GET', 'POST'])
def deletebooking(bid):
    if 'name' in session:
        if request.method == 'POST':
            delete_booking(bid)
            bookings = get_all_bookings()
            return render_template('listofbooking.html', bookings=bookings)
        bookings=get_all_bookings()
        return render_template('listofbooking.html',bookings=bookings)
    else:
        return redirect('/')




@app.route('/logout')
def logout():
    if 'name' in session:
        session.pop("name",None)
        return render_template('logout.html')
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)