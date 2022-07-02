from flask import Flask, render_template, url_for, request
from flaskext.mysql import MySQL
import pymysql.cursors
import json

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'dictionary'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '@OPEyemi2001'

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_response = ' '
    if request.method == 'POST':
        user_input = request.form['word']
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('select meaning from word where word=%s', (user_input))
        rv = cur.fetchall()
        if (len(rv) > 0):
            user_response = rv[0]['meaning']
        else:
            user_response = "The word cannot be found in this dictionary, please try again with another word."
        
    return render_template('index.html', user_response=user_response)

@app.route('/dashboard')
def dashboard():
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('select * from word')
    rv = cur.fetchall()
    for item in rv:
        print(item)
    return render_template('dashboard.html', words=rv)

@app.route('/word', methods=['POST'])
def add_word():
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('insert into word(word, meaning) VALUES (%s, %s)', (word, meaning))
    conn.commit()
    cur.close()

    return json.dumps('success')

if __name__ == '__main__':
    app.run(debug=True)