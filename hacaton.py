import json
FILE_PATH = 'user.json'

def get_users():
    """
    возвращяет сипсок с userами
    """
    with open(FILE_PATH) as file:
        users = json.load(file)
    return users

def get_name():
    user = get_users()
    user_names = [i['name'] for i in user]
    return user, user_names

def get_password():
    user = get_users()
    user_password = [i['password'] for i in user]
    return user_password 

def validate_password(password: str) -> None:
    if len(password) < 8:
        raise Exception('Пароль слишком короткий!')
    if password.isalpha() or password.isdigit():
        raise Exception('Пароль должен состоять из букв и цифр!')


class RegisterMixin:       
    def register(name, password):
        user, user_names = get_name()
        for i in user_names:
            if i == name:
                raise Exception('Такой пользователь уже существует!')
            
        max_id = max([i['id'] for i in user])
        user.append({
        'id': max_id + 1,
        'name': name,
        'password': password
        })
        validate_password(password)
        with open(FILE_PATH, 'w') as file:
            json.dump(user, file)
            print('Successfully registered')


class LoginMixin:
    def login(name, password):
        user, user_names = get_name()
        password_data = get_password()        
        if not name in user_names:
            raise Exception('Нет такого юзера в БД!')                               
        if not password in password_data:
            raise Exception('Неверный пароль!') 
        print('Вы успешно залогинились!')


class ChangePasswordMixin:
    def change_password(name, old_password, new_password):
        validate_password(new_password)
        user, user_names = get_name()
        for i in range(len(user)):
            if user[i]['name'] == name:
                if user[i]['password'] != old_password:
                    raise Exception('Старый пароль указан не верно!')
                else:
                    user[i]['password'] = new_password
        with open(FILE_PATH, 'w') as file:
            json.dump(user, file)
            print('Password changed successfully!')
 

class ChangeUserNameMixin:
    def change_name(old_name, new_name):
        user, user_names = get_name()
        if not old_name in user_names:
            raise Exception('Нет такого зарегистрированного юзера в БД!') 
        while new_name in user_names:    
            print('Пользователь с таким именем уже существует!')
            new_name = input('Введите новое имя: ')
            continue
        with open(FILE_PATH) as f:
            data = json.load(f)
        for dct in data:
            if dct['name'] == old_name:
                dct['name'] = new_name
        with open(FILE_PATH, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('Username changed successfully!')


class CheckOwnerMixin:
    def check(self, name):
        user, user_names = get_name()
        if not name in user_names:
            raise Exception('Нет такого юзера в БД!')
        print('Owner найден')


class User(LoginMixin, RegisterMixin, ChangeUserNameMixin, ChangePasswordMixin):
    pass


class Post(CheckOwnerMixin):
    def __init__(self, title, description, price, quantity, owner) -> None:
        self.check(owner)
        self.title = title
        self.description = description
        self.price = price
        self.quantity = quantity
        self.owner = owner;