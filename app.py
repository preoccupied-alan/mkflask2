from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random
import string
from threading import Timer

app = Flask(__name__)

# The password that allows access to the name submission form
password = ''.join(random.choice(string.ascii_lowercase) for i in range(6))

# Shared password variable accessed by both securepasspage and index.html
shared_password = password

def update_password():
    global password, shared_password
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    shared_password = password  # Update the shared password
    Timer(60, update_password).start()

update_password()

@app.route('/', methods=['GET', 'POST'])
def index():
    global shared_password  # Use the shared password variable
    if request.method == 'POST':
        if 'password' in request.form:
            return jsonify({'password_correct': request.form['password'] == shared_password})
        elif 'name' in request.form and request.form['name']:
            with open('list.json', 'r+') as f:
                data = json.load(f)
                data.append({'name': request.form['name'], 'ideal_spot': request.form['ideal_spot']})
                data.sort(key=lambda x: (x['ideal_spot'], data.index(x)))  # Sort by ideal_spot and insertion order
                f.seek(0)
                json.dump(data, f)
            return redirect(url_for('member'))
    return render_template('index.html')

@app.route('/securepasspage')
def securepasspage():
    global shared_password  # Use the shared password variable
    return render_template('securepasspage.html', password=shared_password)

@app.route('/member')
def member():
    with open('list.json', 'r') as f:
        data = json.load(f)
    return render_template('member.html', data=data)

@app.route('/secureadmin', methods=['GET', 'POST'])
def secureadmin():
    with open('list.json', 'r') as f:
        data = json.load(f)
    return render_template('secureadmin.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
