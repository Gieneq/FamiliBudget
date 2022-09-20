import getpass


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
