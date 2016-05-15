import string
import random
import json

def create_encoding_key():
    crypt_key = {}
    valid_chars = list(string.printable)
    exchangeable_chars = list(string.printable)
    while len(valid_chars) > 0:
        crypt_key[valid_chars.pop(0)] = exchangeable_chars.pop(random.randrange(0,
            len(exchangeable_chars), 1))

    return crypt_key

def create_decoding_key(encodeed_dict):
    decode_key = {}
    #swap the keys and values to create the decode_key
    for key, val in encodeed_dict.items():
        decode_key[val] = key

    return decode_key

def encode(encoding_key, estring):
    encodeed_string = ''
    for c in estring:
        encodeed_string += encoding_key[c]

    return encodeed_string

def decode(decode_key, encodeed_string):
    decodeed_string = ''
    for c in encodeed_string:
        decodeed_string += decode_key[c]

    return decodeed_string


def export_encoding_key(e1):
    e_key = open('encoding_key.json', 'w')
    json.dump(e1, e_key)
    e_key.close()

def export_decoding_key(d1):
    d_key = open('decoding_key.json', 'w')
    json.dump(d1, d_key)
    d_key.close()

# add error handling if there is no encoding key files
# add .close for files
# might be worth removing the hardcode of file names
def import_encoding_key():
    e1 = json.load(open('encoding_key.json')) # how does one close this?
    return e1

def import_decoding_key():
    d1 = json.load(open('decoding_key.json')) # how does one close this?
    return d1

# currently only tested Text I/O
def encode_file(use_keys):
    file_path = input("Please give a path to a file to encode: ")
    f = open(file_path, 'r+')
    if not f.writable():
        print('Error: File is not writable! Terminating Program.')
        exit()
    data  = f.read()

    if use_keys:
        e1 = import_encoding_key()
    else:
        e1 = create_encoding_key()
        export_encoding_key(e1)
        export_decoding_key(create_decoding_key(e1))

    data = encode(e1, data)
    f.seek(0)
    f.write(data)
    f.truncate()
    f.close()
    print("File encodeed!")
    # currently need the encoding keys to returned for debuggging
    return e1

def decode_file():
    file_path = input("Please give a path to the file to decode: ")
    f = open(file_path, 'r+')
    if not f.writable():
        print('Error: File is not writable! Terminating Program.')
        exit()
    data = f.read()
    # this will be removed when the read from decrypion file function is done
    d1 = import_decoding_key()
    data = decode(d1, data)
    f.seek(0)
    f.write(data)
    f.truncate()
    f.close()
    return

def main():
    alive = True
    while(alive):
        print("Please Select:")
        print("1.encode a message")
        print("2.decode a message")
        print("4.Exit")
        option = str(input(""))
        if option == '1':
            print("encode mode selected\n")
            print("1. Use my own encoding keys")
            print("2. Generate an encoding/decoding key set")
            encode_or_decode = str(input(""))
            if encode_or_decode == '1':
                encode_file(True)
            elif encode_or_decode == '2':
                encode_file(False)
            else:
                print("Invalid selection. Redirecting to root menu.")
        elif option == '2':
            print("decoding mode selected")
            decode_file()
        elif option == '4':
            print("Terminating Program")
            alive = False
        else:
            print("Select a valid menu option")


if __name__ == '__main__': main()
