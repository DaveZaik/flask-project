from flask import *
import pymysql
# create the app
app=Flask(__name__)
# define the secret key
app.secret_key = 'mySecretKey'
# define the connection 
connection=pymysql.connect(host="localhost",user="root",database="bookings_db",password="")
# create the main route
@app.route("/")
def Main():
    return "welcome to our application. type the route name in the address bar"

# create the room-upload route
@app.route("/upload_room",methods=['GET','POST'])
def upload_room():
    # check if user has posted anything
    if request.method == 'POST':
        # TODO
            # GET THE RECORDS FROM the user/form
        room_name=request.form['room_name'] 
        room_desc=request.form['room_desc']  
        cost=request.form['cost']  
        avilability=request.form['availability'] 
        square_ft=request.form['square_feet'] 
        image=request.files['image_url']  
        # check if the user if has filled in all the records 
        if not room_name or not room_desc or not cost or not avilability or not square_ft or not image:
            return render_template("upload_room.html",error="please fill all the records") 
        
        # save the image inside the static folder
        image.save('static/images/'+image.filename)
        # pick the name of the image
        image_url=image.filename
        # create cursor to execute the sql query
        cursor=connection.cursor()
        # define the sql query
        sql='insert into rooms(room_name,room_desc,cost,avilability,square_ft,image_url) values(%s,%s,%s,%s,%s,%s)'
        values =(room_name,room_desc,cost,avilability,square_ft,image_url)
        # execute the query
        cursor.execute(sql,values)
        connection.commit()
        return render_template("upload_room.html",message="room uploaded sucessfully")
    else: 
        return render_template("upload_room.html")       

    
    # CRUD operation
    # C-create
    # R-read
    # U-update
    # D-delete-remove-DELETE

@app.route("/getrooms",methods=['get','post'])
def Get_rooms():
    # define the connection
    sql='select * from rooms'
    #cursor function -to execute the sql
    cursor=connection.cursor()
    # execute the sql query
    cursor.execute(sql)
    # fetch the records
    records=cursor.fetchall()
    # check if theres records saved in the database
    if cursor.rowcount==0:
        return render_template("rooms.html",error="No rooms avilable")
    else:
        print(records)
        return render_template("rooms.html",rooms=records)
        # return jsonify(records)


# signup route
@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method =='POST':
        # TODO
        # get data from the form
        username=request.form['username']
        email=request.form['email']
        phone=request.form['phone']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        # connection already defined
        # input validation

        if not username or not email or not phone or not password or not confirm_password:
            return render_template("signup.html",error="please fill all the records") 
        if password !=confirm_password:
            return render_template("signup.html",error="password dont match confirm passsword")
        elif " "in username:
            return render_template("signup",error="username must be one word")


        elif '@' not in email:
            return render_template ("signup.html",error="email must have @")

        elif len(password) <4:
            return render_template("signup.html",error="password must have 4 digits") 
        else:
            # check if the user exists
            sql_check_user='select * from users where username=%s'
            cursor_check_user=connection.cursor()
            cursor_check_user.execute(sql_check_user, username)
            if cursor_check_user.rowcount==1:
              return render_template("signup.html",error="Username already exists")

            sql_save='insert into users (username,email,phone,password) values(%s,%s,%s,%s)'
            values=(username,email,phone,password) 
            # cursor function
            cursor_save=connection.cursor()
            # execute the sql query  
            cursor_save.execute(sql_save,values)
            # commit
            connection.commit()
            return render_template("signup.html",message="signup successful") 
    else:
        return render_template("signup.html") 

#sign in 
@app.route("/login",methods=['GET','POST'])
def Signin():
    #check the method
    if request.method=='POST':
        # TODO
        username=request.form['username']
        password=request.form['password']
        # define the sql query
        sql='select * from users where username=%s and password=%s'
        # create cursor function 
        cursor=connection.cursor()
        # exeucte the qury
        cursor.execute(sql,(username,password))
        # check if user esxits
        if cursor.rowcount==0:
            return render_template("signup.html",error="Incorrect login credentials.Try again")
        # create user sessions
        session['key']=username
        # fetch the other columns
        user=cursor.fetchone()
        session['email']=user[1]
        session['phone']=user[2]
        return redirect("/getrooms")
    # If the request method is GET, render the login page
    else:
     return render_template("login.html")
# clear the session
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

    # run the app
app.run(debug=True,port=80000)

