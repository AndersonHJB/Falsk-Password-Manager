你好，我是悦创。

为了解决问题，你可以设置一个会话或 cookie 来验证管理员是否已经登录。如果没有登录，就应该重定向到登录页面或显示错误信息。下面是修改后的代码，我添加了Flask的`session`功能来跟踪管理员的登录状态，并进行了一些必要的调整：

1. 在`app`配置中添加一个秘钥，以便安全地使用会话。
2. 在管理员成功登录后，设置一个会话变量。
3. 在访问管理密码页面之前，检查会话变量来确认登录状态。

这是修改后的代码示例：

```python
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
from datetime import datetime, timedelta
from models import Admin, Password
from apscheduler.schedulers.background import BackgroundScheduler
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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # 登出时清除会话
    return redirect(url_for('index'))

scheduler = BackgroundScheduler(timezone=pytz.utc)
scheduler.add_job(func=delete_expired_passwords, trigger="interval", seconds=3600)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
```

这段代码设置了一个简单的会话管理，当管理员通过验证后，`session['logged_in']`被设置为`True`，并在用户登出时被删除。这确保了只有成功登录的管理员才能访问管理密码页面。