import sys
import os
import json
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256


file = "logins.encrypted"


def request_password(repeat=False):
    import getpass
    if repeat:
        prompt = "New password: "
    else:
        prompt = "Password: "
    password = getpass.getpass(prompt)
    if repeat:
        repeat_password = getpass.getpass("Repeat password: ")
        if password != repeat_password:
            print("Password mismatch. Try again.")
            exit(1)
    return password


def generate_hash(password, salt):
    password = str.encode(password)
    salt = bytes.fromhex(salt)
    hash_object = SHA256.new(data=password)
    hash_object.update(salt)
    return hash_object.hexdigest()


def validate_password(password, salt, hash_string):
    password = str.encode(password)
    salt = bytes.fromhex(salt)
    hash_object = SHA256.new(data=password)
    hash_object.update(salt)
    if hash_string == hash_object.hexdigest():
        return True
    return False


def init():
    logins = {}
    with open(file, "w") as f:
        json.dump(logins, f)


def passwd(user, create=False):
    with open(file, "r") as f:
        logins = json.load(f)
    if not create and user not in logins:
        print("Add user first.")
        exit(1)
    password = request_password(True)
    salt = get_random_bytes(32).hex()
    hash_string = generate_hash(password, salt)
    if create:
        logins[user] = {}
    logins[user]['hash'] = hash_string
    logins[user]['salt'] = salt
    with open(file, "w") as f:
        json.dump(logins, f)
    if create:
        print("User successfully added.")
    else:
        print("Password change successful.")


def force_pass(user, force=True):
    with open(file, "r") as f:
        logins = json.load(f)
    if force:
        logins[user]['force'] = "yes"
        print("User will be requested to change password on next login.")
    else:
        logins[user]['force'] = ""
    with open(file, "w") as f:
        json.dump(logins, f)


def add(user):
    with open(file, "r") as f:
        logins = json.load(f)
    if user not in logins:
        passwd(user, True)
        force_pass(user, False)
    else:
        print("User already exists. Use passwd instead.")
        exit(1)


def delete(user):
    with open(file, "r") as f:
        logins = json.load(f)
    if user not in logins:
        print("User doesn't exist.")
    else:
        del logins[user]
        print("User successfully removed.")
    with open(file, "w") as f:
        json.dump(logins, f)


def main(argv):
    if not os.path.exists(file):
        init()
    if len(argv) != 2:
        print("usermgmt (add|passwd|forcepass|del) USER")
        exit(1)
    command = argv[0]
    user = argv[1]
    if command == "add":
        add(user)
    elif command == "passwd":
        passwd(user)
    elif command == "forcepass":
        force_pass(user)
    elif command == "del":
        delete(user)
    else:
        print("usermgmt (add|passwd|forcepass|del) USER")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
