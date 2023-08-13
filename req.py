import requests


def make_post_request(url, data=None, headers=None):
    response = requests.post(url, data=data, headers=headers)
    if response.status_code < 202:
        try:
            print(response.json())
        except:
            print(response.text)
    else:
        print(response.status_code, response.reason)


def make_get_request(url, data=None):
    response = requests.get(url, params=data)
    if response.status_code < 202:
        try:
            print(response.json())
        except:
            print(response.text)
    else:
        print(response.status_code, response.reason)


def register_user(email, password, first_name, last_name):
    reg_url = 'http://127.0.0.1:8000/api/v1/auth/users/'
    data = {
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name
    }
    make_post_request(reg_url, data=data)


def login_user(email, password):
    login_url = 'http://127.0.0.1:8000/auth/token/login/'
    data = {
        'email': email,
        'password': password
    }
    make_post_request(login_url, data=data)


def logout_user(token):
    logout_url = 'http://127.0.0.1:8000/auth/token/logout/'
    headers = {
        'Authorization': f'Token {token}'
    }
    make_post_request(logout_url, headers=headers)


def get_friends(user_id=1):
    url = f'http://127.0.0.1:8000/api/v1/profile/friends/{user_id}'
    make_get_request(url)


if __name__ == '__main__':
    user1_token = '9d4834658c0828c66643600ad607fd4670137a73'
    # register_user('user1@mail.ru', 'pass', 'name1', 'surname1')
    # login_user('user1@mail.ru', 'pass')
    # logout_user(user1_token)
    get_friends()

