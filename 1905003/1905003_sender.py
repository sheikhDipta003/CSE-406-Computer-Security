import importlib
import secrets

AES_CBC = importlib.import_module("1905003_AES_CBC")
ECDH = importlib.import_module("1905003_diffie_hellman")
MySocket = importlib.import_module("1905003_mysocket")

a = 0
b = 7
G = [55066263022277343669578718895168534326250603453777594175500187360389116729240, 
     32670510020758816978083085130507043184471273380659243275938904335757337482424]
p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)
B = []

assert ( 4*pow(a,3) + 27*pow(b,2) ) % p != 0

# send IV to receiver for decryption
iv = list(secrets.token_bytes(16))
iv_in_hex = [hex(i)[2:].zfill(2) for i in iv]

# # generate the shared parameters G, a, b, p
# Choose a secret and random number key Ka, and performs a scalar multiplication with the generated points (Ka * G mod P = A)
ka = ECDH.gen_num_with_bits(256, False)
A = ECDH.double_and_add_algo(G, ka, p, a, b)
# # send a, b, G, A to receiver and receive B
MySocket.send(a)
MySocket.send(b)
MySocket.send(p)
MySocket.send(G[0])
MySocket.send(G[1])
MySocket.send(A[0])
MySocket.send(A[1])
temp = MySocket.receive()   # B[0]
B.append(int(temp))
temp = MySocket.receive()   # B[1]
B.append(int(temp))

# # compute the shared secret key, store it and inform receiver that sender is ready for transmission
Ra = ECDH.double_and_add_algo(B, ka, p, a, b)
Ra_in_hex = hex(Ra[0])[2:]

# construct a list of strings where each character is composed of two hex digits
if len(Ra_in_hex) % 2 != 0:
     Ra_in_hex = '0' + Ra_in_hex

key = [Ra_in_hex[i:i+2] for i in range(0, len(Ra_in_hex), 2)]
w = AES_CBC.schedule_key(key[0:16])

# # # sender will send the AES encrypted ciphertext (CT) to receiver using the sockets
to_send = "Never Gonna Give you up Never Gonna Give you up Never Gonna Give you up Never Gonna Give you up"
to_send_encrypt = AES_CBC.encrypt(to_send, iv_in_hex.copy(), w)
to_send_encrypt = iv_in_hex.copy() + to_send_encrypt
MySocket.send_text(to_send_encrypt)

