from flask import Flask, render_template, redirect, url_for, request, flash
import requests, yaml
from flask_mysqldb import MySQL
import joblib
db = yaml.load(open('db.yaml'))


import json

url = "http://api.airvisual.com/v2/nearest_city?key=2c23aa7d-e9ed-4485-97ff-98207407a347"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)
files = response.json()
aqi=files['data']['current']['pollution']['aqius']


app = Flask(__name__)
app.secret_key = 'hello'
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/cache', methods=['GET','POST'])
def cache():
    if request.method == 'POST':
        details = request.form
        city = details['city']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO aqi(city) VALUES(%s)', [city])
        mysql.connection.commit()
        cur.close()
        flash(message='done')
    return render_template('app.html')
@app.route('/aboutus', methods=["GET","POST"])
def aboutus():
	return render_template('aboutus.html')
@app.route('/stats', methods=["GET", "POST"])
def stats():
    return render_template('stats.html', aqi=aqi)
@app.route('/failed', methods=["GET","POST"])
def failed():
    if request.method == 'POST':
        details = request.form
        city = details['city']
        pm10 = details['pm10']
        pm25 = details['pm25']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO aqi(city,pm1,pm25) VALUES(%s,%s,%s)', (city,pm10,pm25))
        mysql.connection.commit()
        cur.close()
    return render_template('failed.html')
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM aqi")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
@app.route('/data', methods=["GET","POST"])
def data():
    if request.method == 'POST':
        details = request.form
        data = details['data']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO data(data) VALUES(%s)', [data])
        mysql.connection.commit()
        cur.close()
    return render_template('data.html')


if __name__ == '__main__':
    app.run()
