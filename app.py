import os
from flask import Flask, render_template, request, redirect, url_for, flash, current_app
import datetime, json, psycopg2

app = Flask(__name__)

app.secret_key = 'secret'
def get_db_connection():
  conn = psycopg2.connect("postgres://kgqrxzyrtsuoag:a84393990d6bbad0365b98b7389f64b88fb4f2d5308b31e0bda1d522faa482b8@ec2-44-205-64-253.compute-1.amazonaws.com:5432/d84mkmj7qcnmon")
  return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    user_response = ' '
    if request.method == 'POST':
        user_input = request.form['word']
        if user_input == ' ':
            flash("You did not enter a valid word, please try again.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('select meaning from firstdict where UPPER(word) = %s', (user_input.upper(), ))
            rv = cur.fetchall()
            if (len(rv) > 0):
                user_response = rv[0][0]
            else:
                flash("The word cannot be found in this dictionary, please try again with another word.")
        
    return render_template('index.html', user_response=user_response)

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from firstdict')
    rv = cur.fetchall()
    for item in rv:
        print(item)
    return render_template('dashboard.html', words=rv)

@app.route('/insert', methods=['POST'])
def insert():
   # req = request.get_json()
   if request.method == "POST":
       id = request.form['id']
       word = request.form['word']
       meaning = request.form['meaning']
       if  word == ' ' or meaning == ' ':
           flash('Please fill in all fields to add a new word')
       else:
           conn = get_db_connection()
           cur = conn.cursor()
           cur.execute('insert into firstdict(id, word, meaning) VALUES (%s, %s, %s)', (id, word, meaning))
           conn.commit()
           cur.close()
           flash('word successfully added!')

           return redirect(url_for('dashboard'))
       return redirect(url_for('dashboard'))

@app.route('/delete/<string:id_data>')
def delete(id_data):
    #word_id = id
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(' delete from firstdict where id=%s ', (id_data))
    conn.commit()
    cur.close()
    flash('word successfully deleted!')

    return redirect(url_for('dashboard'))

@app.route('/edit/<string:id_data>', methods=['GET', 'POST'])
def edit(id_data):
    #word_id = id
    if request.method == "POST":
        #id = request.form['id']
        word = request.form['word']
        meaning = request.form['meaning']
        if  word == ' ' or meaning == ' ':
            flash('Please fill in all fields to update a word')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(' update firstdict set word=%s, meaning=%s where id=%s ', (word, meaning, id_data))
            conn.commit()
            cur.close()
            flash('word successfully updated')
    
        return redirect(url_for('dashboard'))
    
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