from finite_field import *

def main():
    # the order of the field must be greater than the secret and number of shares
    # the file to keep secret
    secret = input("enter secret file: ")
    # number of shares to generate
    n = input("enter number of shares: ")
    # number of shares needed, determines polynomial degree
    k = input("enter k: ")


if __name__ == "__main__":
    main()