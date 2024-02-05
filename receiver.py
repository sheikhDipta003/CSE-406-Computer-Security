from AES_CBC import schedule_key, decrypt
from diffie_hellman import double_and_add_algo, gen_num_with_bits
from mysocket import *

G = []
A = []

# # receive a, b, G, A from sender and send B
a = receive()   # a
b = receive()   # b
p = receive()   # p
temp = receive()   # G[0]
G.append(int(temp))
temp = receive()   # G[1]
G.append(int(temp))
temp = receive()   # A[0]
A.append(int(temp))
temp = receive()    # A[1]
A.append(int(temp))

assert ( 4*pow(a,3) + 27*pow(b,2) ) % p != 0

# Choose a secret and random number key Kb, and performs a scalar multiplication with the generated points (Kb * G mod P = B)
kb = gen_num_with_bits(256, False)
B = double_and_add_algo(G, kb, p, a, b)
send(B[0])
send(B[1])

## compute the shared secret key, store it and inform receiver that sender is ready for transmission
Rb = double_and_add_algo(A, kb, p, a, b)
Rb_in_hex = hex(Rb[0])[2:]

# construct a list of strings where each character is composed of two hex digits
if len(Rb_in_hex) % 2 != 0:
     Rb_in_hex = '0' + Rb_in_hex

key = [Rb_in_hex[i:i+2] for i in range(0, len(Rb_in_hex), 2)]
w = schedule_key(key[0:16])

## reciever should be able to decrypt it using the shared secret key
temp = receive_text()

iv_in_hex = temp[0:16]

decrypted_text = decrypt(temp[16:], iv_in_hex, w)
print("\nDeciphered text:")
print("In HEX: ", end='')
for c in decrypted_text:
    print(c, end=" ")

print("\nIn ASCII: ", end='')
for c in decrypted_text:
    print(bytes.fromhex(c).decode('ascii'), end='')
print()