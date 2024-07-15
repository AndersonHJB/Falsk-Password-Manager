import pickle
from datetime import datetime, timedelta


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Password:
    def __init__(self, password, created_at, valid_days):
        self.password = password
        self.created_at = created_at
        self.valid_days = valid_days


def read_passwords(file_path):
    with open(file_path, 'rb') as file:
        passwords = pickle.load(file)
    return passwords


def get_password_info(password_obj):
    password = password_obj.password
    created_at = datetime.strptime(password_obj.created_at, '%Y-%m-%d %H:%M:%S')
    valid_until = created_at + timedelta(days=password_obj.valid_days)
    return {
        'password': password,
        'created_at': created_at,
        'valid_until': valid_until
    }


passwords_file_path = 'data/passwords.pickle'
passwords_list = read_passwords(passwords_file_path)

for password_obj in passwords_list:
    password_info = get_password_info(password_obj)
    print(
        f"Password: {password_info['password']}, Created At: {password_info['created_at']}, Valid Until: {password_info['valid_until']}")
