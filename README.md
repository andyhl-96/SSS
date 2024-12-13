# SSS -- Simple Shared Secret

An implementation of Shamir's secret sharing for some simple practical purposes.

Shamir's is a cryptographic technique that allows for sharing a secret among several parties without revealing the secret to the parties. Mathematically, it relies on the concept of Lagrange interpolation polynomials and reconstruction of a polynomial using basis polynomials, as well as finite field arithmetic for improved secrecy.

This implementation generates a random encryption key and encrypt a file inputted by a user under that key. The value of the key is then encoded into the constant term of a polynomial and the polynomial is used to generate a user-specified number of shares.

When the user wishes to decrypt a file, they are prompted to input the shares corresponding to the key used to encrypt the file. If a sufficient number of the correct shares are inputted, the file will be decrypted.

Issues:
- Need a better way to input shares for decryption
- Need a more secret way to distribute the shares
- Need to implement finite field arithmetic
