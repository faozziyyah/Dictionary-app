import os
from flask import Flask, render_template, request, flash, current_app
from flaskext.mysql import MySQL
import pymysql.cursors
import json

app = Flask(__name__)

app.secret_key = 'secret'
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
        if user_input == ' ':
            flash("You did not enter a valid word, please try again.")
        else:
            conn = mysql.get_db()
            cur = conn.cursor()
            cur.execute('select meaning from word where word=%s', (user_input))
            rv = cur.fetchall()
            if (len(rv) > 0):
                user_response = rv[0]['meaning']
            else:
                flash("The word cannot be found in this dictionary, please try again with another word.")
        
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
    if  word == ' ' or meaning == ' ':
        flash('Please fill in all fields to add a new word')
    else:
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('insert into word(word, meaning) VALUES (%s, %s)', (word, meaning))
        conn.commit()
        cur.close()
        flash('word successfully added!')

    return json.dumps('success')

@app.route('/word/<id>/delete', methods=['POST'])
def delete_word(id):
    word_id = id
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute(' delete from word where id=%s ', (word_id))
    conn.commit()
    cur.close()
    flash('word successfully deleted!')

    return json.dumps('success')

@app.route('/word/<id>/edit', methods=['POST'])
def edit_word(id):
    word_id = id
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    if  word == ' ' or meaning == ' ':
        flash('Please fill in all fields to update a word')
    else:
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute(' update word set word=%s, meaning=%s where id=%s ', (word, meaning, word_id))
        conn.commit()
        cur.close()
        flash('word successfully updated')

    return json.dumps('success')

@app.route('/add_logo', methods=['POST'])
def add_logo():
    image = request.files['file']

    if image:
        filepath = os.path.join(current_app.root_path, 'static/images/logo.png')
        image.save(filepath)
        flash('image successfully added!')
    else:
        flash('error adding image!')

    return 'success'

if __name__ == '__main__':
    app.run(debug=True)