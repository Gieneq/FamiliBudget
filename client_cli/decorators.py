import fetch
import utils
from utils import CredentialsException, get_username_apikey_from_dotenv, save_username_apikey_dotenv
from fetch import fetch_api_key
import getpass

def with_apikey(user_name_ext=None, api_key_ext=None):
    def decorator(fun):
        def wrapper(*args, user_name=None, api_key=None, **kwargs):
            print('>>with_apikey')
            if user_name_ext is not None and api_key_ext is not None:
                # passed api key, dont save
                print('>>> checking')
                if fetch.check_user_apikey(user_name_ext, api_key_ext):
                    return fun(*args, user_name=user_name_ext, api_key=api_key_ext, **kwargs)
            return fun(*args, user_name=None, api_key=None, **kwargs)
        return wrapper
    return decorator


def with_apikey_restored(fun):
    def wrapper(*args, user_name=None, api_key=None, **kwargs):
        print('>>with_apikey_restored')
        if user_name is not None and api_key is not None:
            # passed api key, dont check
            return fun(*args, user_name=user_name, api_key=api_key, **kwargs)
        # nope, retrive from file
        credentials = get_username_apikey_from_dotenv()
        if credentials is not None:
            user_name, api_key = credentials
        # print(user_name, api_key)
        if fetch.check_user_apikey(user_name, api_key):
            save_username_apikey_dotenv(user_name, api_key)
            return fun(*args, user_name=user_name, api_key=api_key, **kwargs)
        return fun(*args, user_name=None, api_key=None, **kwargs)
    return wrapper


def with_user_password(user_name_ext=None, password_ext=None):
    def decorator(fun):
        def wrapper(*args, user_name=None, api_key=None, **kwargs):
            if user_name_ext is not None and password_ext is not None:
                token = fetch.fetch_api_key(user_name_ext, password_ext)
                if token is not None:
                    save_username_apikey_dotenv(user_name_ext, token)
                    return fun(*args, user_name=user_name_ext, api_key=token, **kwargs)

            if user_name is not None and api_key is not None:
                # passed api key, dont check
                return fun(*args, user_name=user_name, api_key=api_key, **kwargs)
            token, user = utils.input_user_password_fetch_token()  # if fail shut program
            save_username_apikey_dotenv(user, token)
            return fun(*args, user_name=user, api_key=token, **kwargs)
        return wrapper
    return decorator



