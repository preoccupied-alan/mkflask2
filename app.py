from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random
import string
from threading import Timer

app = Flask(__name__)

# The password that allows access to the name submission form
password = ''.join(random.choice(string.ascii_lowercase) for i in range(6))

def update_password():
    global password
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    Timer(60, update_password).start()

update_password()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'password' in request.form:
            return jsonify({'password_correct': request.form['password'] == password})
        elif 'name' in request.form and request.form['name']:
            with open('list.json', 'r+') as f:
                data = json.load(f)
                new_member = {
                    'name': request.form['name'],
                    'spot': int(request.form['spot'])
                }
                data.append(new_member)
                data.sort(key=lambda x: (x['spot'], data.index(x)))  # Sort by spot and original order
                f.seek(0)
                json.dump(data, f)
            return redirect(url_for('member'))
    return render_template('index.html')


@app.route('/securepasspage', methods=['GET'])
def securepasspage():
    return render_template('securepasspage.html', password=password)

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
