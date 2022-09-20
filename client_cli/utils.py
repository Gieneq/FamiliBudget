import getpass
import fetch
import dotenv, os, pathlib

USER_KEY = 'USER_NAME'
API_KEY = 'API_KEY'

def input_user_password(feedback_function):
    try:
        while True:
            print('Pass username/password or Ctrl-C to abort.')
            username = input('Username:')
            password = getpass.getpass(f'Password for {username}:')
            if feedback := feedback_function(username, password):
                return feedback, username  # return or shut program
            print('Attempt failed.\n')
    except KeyboardInterrupt:
        print('Aborted.')
        exit(1)

class CredentialsException(Exception):
    def __init__(self, user_name, message=None):
        if message is None:
            message = f"Password doesn't match user: {user_name}."
        super().__init__(message)


def input_user_password_fetch_token():
    return input_user_password(fetch.fetch_api_key)

def password2_feedback_function(username, password):
    password2 = getpass.getpass(f'Password again {username}:')
    if password2 == password:
        return username, password
    return username, None

def default_feedback_function(username, password):
    return username, password

def input_user_password(feedback_function=default_feedback_function):
    try:
        while True:
            print('Pass username/password or Ctrl-C to abort.')
            username = input('Username:')
            password = getpass.getpass(f'Password for {username}:')
            if feedback := feedback_function(username, password):
                return username, feedback[1]
            print('Attempt failed.\n')
    except KeyboardInterrupt:
        print('Aborted.')
        exit(1)

def get_dotenv_path():
    env_path = dotenv.find_dotenv()
    if not env_path:
        print('No user data stored.')
        pathlib.Path('.env').touch()
        env_path = dotenv.find_dotenv()
    return env_path

def _retrieve_env_vars():
    env_keys = list(os.environ.keys())
    if USER_KEY not in env_keys:
        return None
    if API_KEY not in env_keys:
        return None
    return os.environ.get(USER_KEY), os.environ.get(API_KEY)

def get_username_apikey_from_dotenv():
    """
    Retrieve username and apikey from dotenv if exists. If dotenv doesn't exist create one.
    :return: None if data was not stored or (<USER_KEY>, <API_KEY>)
    """
    env_path = get_dotenv_path()
    dotenv.load_dotenv(dotenv_path=env_path)
    return _retrieve_env_vars()

def save_username_apikey_dotenv(username, apikey):
    env_path = get_dotenv_path()
    dotenv.load_dotenv(dotenv_path=env_path)
    dotenv.set_key(env_path, USER_KEY, username)
    dotenv.set_key(env_path, API_KEY, apikey)






# def login(silent = False):
#
#
#
#
#     if not silent:
#         print('Attempting to login...')
#     env_path = dotenv.find_dotenv()
#     if not env_path:
#         if not silent:
#             print('No user data stored.')
#         pathlib.Path('.env').touch()
#         env_path = dotenv.find_dotenv()
#
#     dotenv.load_dotenv(dotenv_path=env_path)
#
#     env_vars = _retrieve_env_vars()
#     """
#     env_vars == None -> login with new user/pass
#     env_vars != None -> use apikey
#     """
#     if env_vars:
#         user = env_vars[USER_KEY]
#         api_key = env_vars[API_KEY]
#         if not silent:
#             print(f'Logging in to {user} with previously stored data.')
#         success = fetch.fetch_status(user, api_key)
#         if not success:
#             print(f"Couldn't login to {user} with stored credentials.")
#             env_vars = None  # seems to be not up to date or incorrect
#
#     if not env_vars:
#         env_vars = input_user_password_retrieve_token()
#
#     if not env_vars:
#         print("Couldn't logine. Try again or register new account using 'register' command.")
#         return None
#
#     # user/key finally retived and can be stored
#     if not silent:
#         print(f"User {env_vars.get(USER_KEY)} successfully logged in.")
#     if os.environ.get(USER_KEY) != env_vars[USER_KEY] or os.environ.get(API_KEY) != env_vars[API_KEY]:
#         dotenv.set_key(env_path, USER_KEY, env_vars[USER_KEY])
#         dotenv.set_key(env_path, API_KEY, env_vars[API_KEY])
#         print('Credentials stored for future use.')
#     return env_vars





# def register():
#     print('Attempting to register new accout...')
