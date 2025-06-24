
from gmpy2 import mpz, next_prime, is_prime, bit_length, random_state, mpz_urandomb, powmod
from time import time

rand = random_state(int(time()))

def gen_safe_prime(bits=256):
    while True:
        p_ = next_prime(mpz_urandomb(rand, bits - 1))
        p = 2 * p_ + 1
        if is_prime(p, 25) and p % 4 == 3:
            return p

with open("primes.txt") as f:
    p, q = map(int, f.read().split())


def hybrid(x, N, s, taps, k=8, n=1000):
    output = []
    for _ in range(n):
        lsb_s = s&1
        lsb_x = x&1

        new_bit  = 0
        for  i in taps:
            new_bit ^= (s>>i)&1
            s = ((s<<1) | new_bit) & ((1<<k)-1)
        
        exp = 2 + (lsb_s^lsb_x)
        x = powmod(x, exp, N)

        out = ((s>>(k-1))&1) ^ (x&1)

        output.append(out)

    return output

def bbs(x, N, n=1000):
    output = []
    for _ in range(n):
        x = powmod(x, 2, N)
        out = x.bit_count() & 1
        output.append(out)
    
    return output


def write_to_binfile(bits, filename):
    with open(filename, "wb") as f:
        byte = 0
        count = 0
        for bit in bits:
            byte = ((byte << 1) & 0xFF) | bit   # mask to 8 bits
            count += 1
            if count == 8:
                f.write(bytes([byte]))
                byte = 0
                count = 0
        if count > 0:
            byte = (byte << (8 - count)) & 0xFF
            f.write(bytes([byte]))


N = p*q
s = 121 #8 bit register
x = 42
taps = [3, 4, 6]
k, n = 8, 1000

# start_time = time()
# keystream = hybrid(x, N, s, taps, k, 10**6)
# print(time() - start_time)

# start_time = time()
# keystream = bbs(x, N, 10**6)
# print(time()-start_time)

write_to_binfile(hybrid(x, N, s, taps, k, 10**6+8), "hybrid.bin")
write_to_binfile(bbs(x, N, 10**6+8), "bbs.bin")


