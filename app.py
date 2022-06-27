from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_response = ' '
    if request.method == 'POST':
        user_response = request.form['word']
    return render_template('index.html', user_response=user_response)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# @app.route('/greet')
#def greet():
 #   name = 'John Doe'
 #   return render_template('greet.html', name=name) 

if __name__ == '__main__':
    app.run(debug=True)