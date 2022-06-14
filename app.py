from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def about():
    return render_template('dashboard.html')

# @app.route('/greet')
#def greet():
 #   name = 'John Doe'
 #   return render_template('greet.html', name=name) 

if __name__ == '__main__':
    app.run(debug=True)