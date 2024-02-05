import random
from sympy import isprime
import time

# a = 0
# b = 7
# G = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 
#      32670510020758816978083085130507043184471273380659243275938904335757337482424)
# p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)

def gen_num_with_bits(k, mustBePrime):      # returns a 'k' bit number, if 'mustBePrime == True', then returns a prime number
    while True:
        num = random.getrandbits(k)
        num |= 1 << (k - 1)
        
        if(mustBePrime == True):
            num |= 1
            if(isprime(num)):
                return num
        else:
            return num
        
def point_addition(P, Q, p):    # P,Q -> points located on elliptic curve, p -> modulus
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]
    
    s = (y2 - y1) * pow(x2 - x1, -1, p)
    
    x3 = (pow(s, 2) - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    
    return x3, y3

def point_doubling(P, p, a):    # P -> point located on elliptic curve, p -> modulus, a -> curve parameter
    x1 = P[0]
    y1 = P[1]
    
    s = (3 * pow(x1,2) + a) * pow(2 * y1, -1, p)
    
    x3 = (pow(s, 2) - 2 * x1) % p
    y3 = (s * (x1 - x3) - y1) % p
    
    return x3, y3
    
def double_and_add_algo(P, d, p, a, b):       # P -> elliptic curve generating point, d -> scalar multiplier, p -> modulus, a,b -> curve parameter
    temp = P
    
    mult_bin = bin(d)[2:]               # binary of the scalar multiplier d
    
    for i in range(1, len(mult_bin)):        
        temp = point_doubling(temp, p, a)
        
        if(mult_bin[i] == '1'):
            temp = point_addition(temp, P, p)
            
    assert pow(temp[1], 2) % p == (pow(temp[0], 3, p) + a * temp[0] + b) % p

    return temp

# key generation
def gen_stats(k, G, p, a, b):   # k -> number of iterations to generate statistics, G -> base point, p -> modulus, a,b -> curve parameter
    A_gen_time, B_gen_time, Ra_gen_time, Rb_gen_time = 0, 0, 0, 0
    for i in range(10):
        # private keys
        ka = gen_num_with_bits(k, False)
        kb = gen_num_with_bits(k, False)

        # public keys
        start = time.time()
        A = double_and_add_algo(G, ka, p, a, b)
        end = time.time()
        A_gen_time += (end - start) * 1000

        start = time.time()
        B = double_and_add_algo(G, kb, p, a, b)
        end = time.time()
        B_gen_time += (end - start) * 1000

        # shared secret keys
        start = time.time()
        Ra = double_and_add_algo(B, ka, p, a, b)
        end = time.time()
        Ra_gen_time += (end - start) * 1000

        start = time.time()
        Rb = double_and_add_algo(A, kb, p, a, b)
        end = time.time()
        Rb_gen_time += (end - start) * 1000

    return A_gen_time/10, B_gen_time/10, (Ra_gen_time + Rb_gen_time)/10

# print(gen_stats(128, G, p, a, b))
# print(gen_stats(192, G, p, a, b))
# print(gen_stats(256, G, p, a, b))