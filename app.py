from models import Admin, Password
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import pytz

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 你可以生成一个更安全的密钥


def save_data(admins, passwords):
    with open('admins.pickle', 'wb') as f:
        pickle.dump(admins, f)
    with open('passwords.pickle', 'wb') as f:
        pickle.dump(passwords, f)


def load_data():
    try:
        with open('admins.pickle', 'rb') as f:
            admins = pickle.load(f)
    except FileNotFoundError:
        admins = []
    try:
        with open('passwords.pickle', 'rb') as f:
            passwords = pickle.load(f)
    except FileNotFoundError:
        passwords = []
    return admins, passwords


# 创建一个管理员账号
hashed_password = generate_password_hash("admin", method='pbkdf2:sha256')
admin = Admin("admin", hashed_password)
admins, passwords = load_data()
admins.append(admin)
save_data(admins, passwords)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    # admins, passwords = load_data()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admins, passwords = load_data()
        for admin in admins:
            if admin.username == username and check_password_hash(admin.password, password):
                session['logged_in'] = True  # 设置会话标志为已登录
                return redirect(url_for('manage_passwords'))
        return 'Invalid credentials'
    else:
        return render_template('admin.html')


@app.route('/manage-passwords', methods=['GET', 'POST'])
def manage_passwords():
    if not session.get('logged_in'):  # 检查是否已经登录
        return redirect(url_for('admin_page'))  # 未登录则重定向到登录页面
    admins, passwords = load_data()
    if request.method == 'POST':
        password = request.form['password']
        valid_days = int(request.form['valid_days'])
        new_password = Password(password, datetime.utcnow(), valid_days)
        passwords.append(new_password)
        save_data(admins, passwords)
        return 'Password added'
    else:
        return render_template('manage_passwords.html', passwords=passwords)


@app.route('/content', methods=['GET', 'POST'])
def content():
    admins, passwords = load_data()
    if request.method == 'POST':
        password = request.form['password']
        for password_entry in passwords:
            if password_entry.password == password:
                if password_entry.valid_days == -1 or \
                        datetime.utcnow() - password_entry.created_at < timedelta(days=password_entry.valid_days):
                    # return 'Here is the content...'
                    return str(open("link.html", "r").read())
                else:
                    return 'Password expired'
        return 'Invalid password'
    else:
        return render_template('content.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # 登出时清除会话
    return redirect(url_for('index'))


def delete_expired_passwords():
    with open('passwords.pickle', 'rb') as f:
        passwords = pickle.load(f)

    for password in passwords:
        if password.valid_days != -1 and datetime.now() > password.created_at + timedelta(days=password.valid_days):
            passwords.remove(password)

    with open('passwords.pickle', 'wb') as f:
        pickle.dump(passwords, f)


@app.route('/delete-password', methods=['GET', 'POST'])
def delete_password():
    if not session.get('logged_in'):  # 检查是否已经登录
        return redirect(url_for('admin_page'))  # 未登录则重定向到登录页面
    admins, passwords = load_data()
    if request.method == 'POST':
        password_to_delete = request.form['password_to_delete']
        passwords = [password for password in passwords if password.password != password_to_delete]
        save_data(admins, passwords)
        flash('Password deleted successfully.')
        return redirect(url_for('delete_password'))
    else:
        return render_template('delete_password.html', passwords=passwords)


# scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Tokyo'))
scheduler = BackgroundScheduler(timezone=pytz.utc)
scheduler.add_job(func=delete_expired_passwords, trigger="interval", seconds=3600)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
