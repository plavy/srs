import sys
import os
import json
from usermgmt import file, validate_password, request_password, passwd, force_pass


def login(user):
    with open(file, "r") as f:
        logins = json.load(f)
    force = ""
    while True:
        password = request_password()
        if user not in logins:
            print("Username or password incorrect.")
            continue
        hash_string = logins[user]['hash']
        salt = logins[user]['salt']
        force = logins[user]['force']
        if not validate_password(password, salt, hash_string):
            print("Username or password incorrect.")
            continue
        break
    if force:
        print("Administrator demanded password change.")
        passwd(user)
        force_pass(user, False)
    print("Login successful.")


def main(argv):
    if not os.path.exists(file):
        print("No logins file found!")
        exit(1)
    if len(argv) != 1:
        print("login USER")
        exit(1)
    user = argv[0]
    login(user)


if __name__ == "__main__":
    main(sys.argv[1:])
