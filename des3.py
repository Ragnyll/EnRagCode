import string
import random
import json

def create_encryption_key():
    crypt_key = {}
    valid_chars = list(string.printable)
    exchangeable_chars = list(string.printable)
    while len(valid_chars) > 0:
        crypt_key[valid_chars.pop(0)] = exchangeable_chars.pop(random.randrange(0,
            len(exchangeable_chars), 1))
    return crypt_key

def create_decryption_key(encrypted_dict):
    decrypt_key = {}
    #swap the keys and values to create the decrypt_key
    for key, val in encrypted_dict.items():
        decrypt_key[val] = key
    return decrypt_key

def encrypt(encryption_key, estring):
    encrypted_string = ''
    for c in estring:
        encrypted_string += encryption_key[c]
    return encrypted_string

def decrypt(decrypt_key, encrypted_string):
    decrypted_string = ''
    for c in encrypted_string:
        decrypted_string += decrypt_key[c]
    return decrypted_string

def des3_encrypt(e1, e2, e3, estring):
    estring = encrypt(e1, estring)
    estring = encrypt(e2, estring)
    estring = encrypt(e3, estring)
    return estring

def des3_decrypt(d1, d2, d3, estring):
    estring = decrypt(d3, estring)
    estring = decrypt(d2, estring)
    estring = decrypt(d1, estring)
    return estring

# give it the encrypted dictionaries
def export_des3_encryption_keys(e1, e2, e3):
    des_e_1 = open('des_e_1.json', 'w')
    json.dump(e1, des_e_1)
    des_e_1.close()
    des_e_2 = open('des_e_2.json', 'w')
    json.dump(e1, des_e_2)
    des_e_2.close()
    des_e_3 = open('des_e_3.json', 'w')
    json.dump(e3, des_e_3)
    des_e_3.close()

# give it the decrypt dictionaries
def export_des3_decryption_keys(d1, d2, d3):
    des_d_1 = open('des_d_1.json', 'w')
    json.dump(d1, des_d_1)
    des_d_1.close()
    des_d_2 = open('des_d_2.json', 'w')
    json.dump(d2, des_d_2)
    des_d_2.close()
    des_d_3 = open('des_d_3.json', 'w')
    json.dump(d3, des_d_3)
    des_d_3.close()

# add error handling if there is no encryption key files
# add .close for files
# might be worth removing the hardcode of file names
def import_encryption_keys():
    e1 = json.load(open('des_e_1.json')) # how does one close this?
    e2 = json.load(open('des_e_2.json'))
    e3 = json.load(open('des_e_3.json'))
    return e1, e2, e3

def import_decryption_keys():
    d1 = json.load(open('des_d_1.json')) # how does one close this?
    d2 = json.load(open('des_d_2.json'))
    d3 = json.load(open('des_d_3.json'))
    return d1, d2, d3
# currently only tested Text I/O
def encrypt_file(use_keys):
    file_path = input("Please give a path to a file to encrypt: ")
    f = open(file_path, 'r+')
    if not f.writable():
        print('Error: File is not writable! Terminating Program.')
        exit()
    data  = f.read()

    if use_keys:
        e1, e2, e3 = import_encryption_keys()
    else:
        e1 = create_encryption_key()
        e2 = create_encryption_key()
        e3 = create_encryption_key()
        export_des3_encryption_keys(e1, e2, e3)
        export_des3_decryption_keys(create_decryption_key(e1), create_decryption_key(e2),
            create_decryption_key(e3))

    data = des3_encrypt(e1, e2, e3, data)
    f.seek(0)
    f.write(data)
    f.truncate()
    f.close()
    print("File Encrypted!")
    # currently need the encryption keys to returned for debuggging
    return e1, e2, e3

def decrypt_file():
    file_path = input("Please give a path to the file to decrypt: ")
    f = open(file_path, 'r+')
    if not f.writable():
        print('Error: File is not writable! Terminating Program.')
        exit()
    data = f.read()
    # this will be removed when the read from decrypion file function is done
    d1, d2, d3 = import_decryption_keys()
    data = des3_decrypt(d1, d2, d3, data)
    f.seek(0)
    f.write(data)
    f.truncate()
    f.close()
    return

def main():
    alive = True
    while(alive):
        print("Please Select:")
        print("1.Encrypt a message")
        print("2.Decrypt a message")
        print("4.Exit")
        option = str(input(""))
        if option == '1':
            print("Encrypt mode selected\n")
            print("1. Use my own encryption keys")
            print("2. Generate an Encryption/Decryption key set")
            encrypt_or_decrypt = str(input(""))
            if encrypt_or_decrypt == '1':
                encrypt_file(True)
            elif encrypt_or_decrypt == '2':
                encrypt_file(False)
            else:
                print("Invalid selection. Redirecting to root menu.")
        elif option == '2':
            print("Decryption mode selected")
            decrypt_file()
        elif option == '4':
            print("Terminating Program")
            alive = False
        else:
            print("Select a valid menu option")


if __name__ == '__main__': main()
