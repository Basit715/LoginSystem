from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import certifi
import bcrypt

client = MongoClient("mongodb+srv://basitabass27411:iamahacker313@baiq.o4c0pn6.mongodb.net/?retryWrites=true&w=majority", tlsCAFile = certifi.where())
db = client['login']
coll = db['user']

# coll.insert_one({'user1': 'password'}) 

app = Flask(__name__) 


@app.route('/')
def index():
     if 'username' in session:
          return render_template('index.html')
     return render_template("index.html")
@app.route('/register', methods = ['GET', 'POST'])
def register():
     
     if request.method == 'POST':
         user = coll.find_one({'name': request.form['username']})
         
         if user is None:
              hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
              coll.insert_one({'name':request.form['username'], 'password': hashpass})
              session['username'] = request.form['username']
              return redirect(url_for('index'))
         
         
         return 'The username already exists'
     
     return render_template('register.html')     

@app.route('/login', methods = ['POST'])
def login():
     user = coll.find_one({'name':request.form['username']})
     if user:
          if bcrypt.hashpw(request.form['password'].encode('utf-8'), user['password']) == user['password']:
               return render_template('home.html')
     return 'incorrect username/password' 
               
     
     
     
if __name__ == "__main__":
     app.secret_key = 'mysecret'
     app.run(debug=True)