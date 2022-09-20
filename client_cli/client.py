import argparse
import sys, os
import fetch
from utils import input_user_password, password2_feedback_function

prog_name = 'FamilyBudget Client'

class ClientCli:
    """
    Commandline tool used in communication with backend.
    """
    def __init__(self):
        dirname, filename = os.path.split(__file__)
        print('''
    |----------------------------------------------------------|
    |                   FamilyBudget Client                    |
    |----------------------------------------------------------|''')
        parser = argparse.ArgumentParser(
            prog=prog_name,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=filename + ' [command] {args}',
            description='''
    |----------------------------------------------------------|
    |            Client used to interact with web app.         |
    |----------------------------------------------------------|''',
        epilog='''
    |----------------------------------------------------------| 
    |           First try to 'register' or 'login'.            |
    |     Then type -h or --help for further instruction.      |       
    | All commands despite 'register' require to be logged in. |
    |----------------------------------------------------------|''')

        self.choices = ['register', 'login', 'status', 'info', 'email', 'test']
        parser.add_argument('command', help='Type command to be used', choices=self.choices)

        def _retrieve_cmd_or_exit():
            cmd = None
            if len(sys.argv) > 1:
                cmd = parser.parse_args(sys.argv[1:2])  # if incorrent parser will exit
            if not cmd or not hasattr(self, cmd.command):
                parser.print_help()
                exit(1)
            return cmd.command, sys.argv[2:]

        cmd, args = _retrieve_cmd_or_exit()
        print(getattr(self, cmd)(*args))



    def status(self, *args, **kwargs):
        """
        Test if backend server works. No authentication required.
        """
        status_parser = argparse.ArgumentParser()
        status_parser.add_argument('-v', '--verbose', action='store_true')
        status_args = status_parser.parse_args(args)
        return fetch.fetch_status(status_args.verbose)

    def register(self, *args, **kwargs):
        """
        Register user with password. No authentication required.
        """
        user, password = input_user_password(password2_feedback_function)
        result = fetch.fetch_register(user, password)
        return result[2]

    def email(self, *args, **kwargs):
        email_parser = argparse.ArgumentParser()
        email_parser.add_argument('email')
        email_parser.add_argument('-v', '--verbose', action='store_true')
        email_args = email_parser.parse_args(args)

        # user, password = input_user_password()
        user, password = 'Tomek', 'zwierz1234'
        return fetch.fetch_set_email(user, password, email_args.email, email_args.verbose)

if __name__ == "__main__":
    ClientCli()