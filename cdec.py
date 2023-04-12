from helpers import *
import sys

def decrypt(esentence, s):
    encoded = blockConverter(esentence)
    enlength = len(encoded)
    A = int(encoded[0], 2)
    B = int(encoded[1], 2)
    C = int(encoded[2], 2)
    D = int(encoded[3], 2)
    cipher = [A, B, C, D]
    r = 12
    w = 32
    modulo = 2**32
    lgw = 5
    C = (C - s[2*r+3]) % modulo
    A = (A - s[2*r+2]) % modulo
    for j in range(1, r+1):
        i = r+1-j
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D*(2*D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        t_temp = (B*(2*B + 1)) % modulo 
        t = ROL(t_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        C = (ROR((C-s[2*i+1]) % modulo, tmod, 32) ^ u)  
        A = (ROR((A-s[2*i]) % modulo, umod, 32) ^ t) 
    D = (D - s[1]) % modulo 
    B = (B - s[0]) % modulo
    orgi = [A, B, C, D]
    return cipher, orgi

def main():
    if len(sys.argv) < 2:
        print("Usage: python cenc.py <key> optional(filename)")
        sys.exit(0)

    key = sys.argv[1]
    if len(key) < 16:
        key = key + " "*(16-len(key))
    key = key[:16]
                          
    s = generateKey(key)
    loc = "encrypted.txt"
    if len(sys.argv) >= 3:
        loc = sys.argv[2]
    with open(loc, "r") as f:
        esentence = f.readline().strip()
    cipher, orgi = decrypt(esentence, s)
    sentence = deBlocker(orgi)
    print("\nDecrypted String list: ", orgi)
    print("Decrypted String: " + sentence)

if __name__ == "__main__":
    main()