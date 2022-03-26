import json
import sys
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256


file = "tajnik.encrypted"


def generate_keys(master_key):  # IMPROVE FUNCTION
    master_key = str.encode(master_key)
    aes_key = SHA256.new(data=master_key)
    hmac_key = SHA256.new(data=master_key)
    return aes_key.digest(), hmac_key.digest()


def generate_aes(key, data):
    data = str.encode(json.dumps(data))
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return iv, ct


def decrypt_aes(key, iv, ct):
    try:
        iv = b64decode(iv)
        ct = b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
    except (ValueError, KeyError):
        raise Exception("Incorrect AES decryption")


def generate_hmac(key, data):
    data = str.encode(data)
    h = HMAC.new(key, digestmod=SHA256)
    h.update(data)
    return h.hexdigest()


def validate_hmac(key, hmac, data):
    data = str.encode(data)
    h = HMAC.new(key, digestmod=SHA256)
    h.update(data)
    try:
        h.hexverify(hmac)
        return True
    except ValueError:
        return False


def init(master_pass):
    aes_key, hmac_key = generate_keys(master_pass)
    data = {}
    init_vector, cipher = generate_aes(aes_key, data)
    hmac = generate_hmac(hmac_key, cipher)
    result = json.dumps({'init_vector': init_vector, 'hmac': hmac, 'encrypted_data': cipher})
    with open(file, "w") as f:
        json.dump(result, f)
    print("Password manager initialized.")


def get(master_pass, site):
    aes_key, hmac_key = generate_keys(master_pass)
    with open(file, "r") as f:
        result = json.loads(json.load(f))
    if validate_hmac(hmac_key, result['hmac'], result['encrypted_data']):
        data = json.loads(decrypt_aes(aes_key, result['init_vector'], result['encrypted_data']))
        if site in data:
            print(f"Password for {site} is: {data[site]}.")
        else:
            print(f"No password found for {site}.")
            exit(1)
    else:
        print("Master password incorrect or integrity check failed.")


def put(master_pass, site, password):
    aes_key, hmac_key = generate_keys(master_pass)
    with open(file, "r") as f:
        result = json.loads(json.load(f))
    if validate_hmac(hmac_key, result['hmac'], result['encrypted_data']):
        data = json.loads(decrypt_aes(aes_key, result['init_vector'], result['encrypted_data']))
        data[site] = password
        init_vector, cipher = generate_aes(aes_key, data)
        hmac = generate_hmac(hmac_key, cipher)
        result = json.dumps({'init_vector': init_vector, 'hmac': hmac, 'encrypted_data': cipher})
        with open(file, "w") as f:
            json.dump(result, f)
        print(f"Stored password for {site}.")
    else:
        print("Master password incorrect or integrity check failed.")


def main(argv):
    command = argv[0]
    if command == "init":
        init(argv[1])
    elif command == "get":
        get(argv[1], argv[2])
    elif command == "put":
        put(argv[1], argv[2], argv[3])
    else:
        print("tajnik: Available commands are: init | put | get")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
