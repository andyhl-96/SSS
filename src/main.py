from SSlib import *
from cryptography.fernet import Fernet
import getpass
import base64

def main():
    # prompt user for option
    opt = input("(E)ncrypt or (D)ecrypt >> ")

    # encryption procedure
    if opt.upper() == "E":
        # the order of the field must be greater than the secret and number of shares
        # the file to keep secret

        # prompt for a file to encrypt and read contents
        path = input("Enter file (absolute) >> ")
        file = open(path, "r")
        contents = ""
        for line in file.readlines():
            contents += line

        # initialize encryption library
        key = Fernet.generate_key()
        # obtain the integer value of the key byte array
        key_int = int.from_bytes(base64.urlsafe_b64decode(key), "little")
        fernet1 = Fernet(key)
        # encrypt the file contents and write ciphertext to file
        C = fernet1.encrypt(contents.encode())
        outfile = open("../out/secret.susss", "w")
        outfile.write(C.decode() + "\n")

        # prompt for number of shares to generate
        n = input("Enter number of shares >> ")
        n = int(n)
        # prompt for number of shares needed, determines polynomial degree
        k = input("Enter shares needed >> ")
        k = int(k)
        # write required share number for later
        outfile.write(str(k))
        # currently using the integer for arithmetic, change later
        field = Ffield(0, 0)
        poly = Polynomial(key_int, k - 1, field)
        poly.generate_shares(n)

        # write the generated shares to a file, change later for security
        sh = open("shares", "w")
        for share in poly.shares:
            sh.write(str(share) + "\n")

    # decryption procedure
    elif opt.upper() == "D":
        # prompt for file to decrypt, read ciphertext and required shares
        path = input("Enter file >> ")
        file = open(path, "r")
        C = file.readline()
        k = file.readline()
        k = int(k)
        file.close()

        # using integers, later need to use the proper finite field
        field = Ffield(0, 0)
        # initialize polynomial of degree k - 1 for computation
        poly = Polynomial(0, k - 1, field)
        shares = []
        # read the shares from file
        for i in range(k):
            temp = input("Enter share >> ")
            temp = temp[1:-1].split(",")
            share = (int(temp[0]), int(temp[1]))
            shares.append(tuple(share))
        
        # compute the secret key and convert it to a byte array
        secret = poly.compute_secret(shares)
        key = secret.to_bytes(32, "little")
        fernet = Fernet(base64.urlsafe_b64encode(key))

        # convert ciphertext to bytes
        C = bytes(C, "utf-8")
        P = fernet.decrypt(C).decode()
        file = open("plain_text", "w")
        file.write(P)
        file.close()
        pass
        


if __name__ == "__main__":
    main()