import pickle
from datetime import datetime, timedelta


# 定义 Admin 和 Password 类
class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Password:
    def __init__(self, password, created_at, valid_days):
        self.password = password
        self.created_at = created_at
        self.valid_days = valid_days


# 自定义 Unpickler 类
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "models" and name == "Admin":
            return Admin
        elif module == "models" and name == "Password":
            return Password
        return super().find_class(module, name)


# 读取密码的函数
def read_passwords(file_path):
    with open(file_path, 'rb') as file:
        passwords = CustomUnpickler(file).load()
    return passwords


# 获取密码信息的函数
def get_password_info(password_obj):
    password = password_obj.password
    created_at = password_obj.created_at
    valid_until = created_at + timedelta(days=password_obj.valid_days)
    return {
        'password': password,
        'created_at': created_at,
        'valid_until': valid_until
    }


# 路径到pickle文件
passwords_file_path = 'data/passwords.pickle'
# 从文件中读取密码
passwords_list = read_passwords(passwords_file_path)

# 收集每个密码的信息
passwords_info = [get_password_info(password_obj) for password_obj in passwords_list]

import pandas as pd

# 显示密码信息为DataFrame
passwords_df = pd.DataFrame(passwords_info)
print(passwords_df)
