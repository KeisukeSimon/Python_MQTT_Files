from flask import Flask, request, render_template
import time
import datetime
import sys
import sqlite3

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
	return "Hello world!"

@app.route("/platzi")
def platzi():
	return render_template("platzi.html")

@app.route("/lab_temp")
def lab_temp():
	return "This is an example route"

@app.route("/mqtt_env_db",methods=['GET'])
def mqtt_env_db():
	temperatures, humidities, from_date_str, to_date_str = get_records()
	return render_template("mqtt_env.html",temp=temperatures,hum=humidities)

def get_records():

	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
	range_h_form	= request.args.get('range_h',''); #This will return a string, if field range_h exist in the request

	range_h_int	= "nan" #initialise this variable with not a number

	try:
		range_h_int	= int(range_h_form)
	except:
		print("range_h_form not a number")

	if not validate_date(from_date_str):			# Validate date before sending it to the DB
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M")		# Validate date before sending it to the DB

	if isinstance(range_h_int,int):
		time_now	= datetime.datetime.now()
		time_from	= time_now - datetime.datetimedelta(hours = range_h_imt)
		time_to		= time_now
		from_date_str	= time_from.strftime("%Y=%m-%d %H:%M")
		to_date_str	= time_to.strftime("%Y-%m-%d %H:%M")

	conn=sqlite3.connect('/var/www/mqtt_app/mqtt_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures")
	temperatures = curs.fetchall()
	curs.execute("SELECT * FROM humidities")
	humidities = curs.fetchall()
	conn.close()
	return[temperatures, humidities, from_date_str, to_date_str]

def validate_date(d):
	try:
		datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
