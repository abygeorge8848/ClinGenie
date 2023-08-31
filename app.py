from flask import Flask, render_template
from gpt import gpt
from sql import sql
from save import save, data, delete, update
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/profile')
def home():
    return render_template('index.html')

gpt(app)
sql(app)
save(app)
data(app)
delete(app)
update(app)
