from flask import url_for, flash, jsonify, Flask, render_template, request, redirect, session
import json
import requests
from functools import wraps
from urllib2 import Request, urlopen, URLError
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Registration

app = Flask(__name__)

#engine = create_engine('sqlite:///registration.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#sess = DBSession()
url = 'https://cluzzchef-intern.herokuapp.com:443/register'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged-in' in session:
            return f(*args, **kwargs)

        else:
            flash('You need to be logged in first.')
            return redirect(url_for('login'))

    return wrap

@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        url = 'https://cluzzchef-intern.herokuapp.com/register'
        daata=request.form
        requests.post(url, data = daata)
        flash('Your details have been successfully submitted, Please login to view your profile.')

        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
            phone = request.form['phone_number']
            password = request.form['password']

            if (len(phone)>0) and (len(password)>0) :
                    try:
                        if phone == 'admin' and password=='admin':
                            url1 = 'https://cluzzchef-intern.herokuapp.com/register'
                            req1 = Request(url1)
                            response = urlopen(req1)
                            if response!= None:
                                j_response = json.loads(response.read())
                                users = j_response["users"]
                                m = len(users)
                                session['logged-in'] = True
                                return render_template('users.html', users = users, m = m)

                        else :
                            url = 'https://cluzzchef-intern.herokuapp.com/login/'+phone+'/'+password
                            req = Request(url)
                            response = urlopen(req)
                            if response!=None:
                                json_response = json.loads(response.read())
                                status = json_response["status"]
                                email= json_response["user"]["email"]
                                fname= json_response["user"]["fname"]
                                lname= json_response["user"]["lname"]
                                phone_number= json_response["user"]["phone_number"]

                                print status
                                if status==True:
                                        session['logged-in'] = True
                                        return render_template('logged.html', fname = fname, lname = lname, email = email, phone_number = phone_number)
                                else :
                                        return render_template('index.html', error = error)

                    except URLError as e:
                        if hasattr(e, 'reason'):
                            print 'We failed to reach a server.'
                            print 'Reason: ', e.reason
                        elif hasattr(e, 'code'):
                            print 'The server couldn\'t fulfill the request.'
                            print 'Error code: ', e.code
                        else:
                            return render_template(url_for('home'))
            else:
                    return render_template('index.html', error = error, id = id)

    else:
        return render_template('index.html', error = error)



@app.route('/logout')
@login_required
def logout():
    session.pop('logged-in', None)
    flash('You were just logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
