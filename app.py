from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    
        if username == 'admin' and password == 'admin123':
            session['username'] = username
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))

        elif username == 'user' and password == 'user123':
            session['username'] = username
            session['role'] = 'user'
            return redirect(url_for('user_dashboard'))

        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/user/dashboard')
def user_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'user':
        return redirect(url_for('login'))

    return render_template('user/dashboard.html', username=session.get('username'))


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    return render_template('admin/dashboard.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)