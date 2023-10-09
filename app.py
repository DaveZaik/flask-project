from flask import *
import pymysql
# create the app
app=Flask(__name__)
# define the connection 
connection = pymysql.connect(host ="localhost",user ="root",database="bookings_db",password="")
# create the main 
@app.route("/")
def home():
 return"Welcome to our application. Type the route name in the address bar"

# create the room-upload route
@app.route("/")
def uploadRoom():
 return