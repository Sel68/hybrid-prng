from gmpy2 import next_prime, is_prime, random_state, mpz_urandomb, powmod
from time import time
from multiprocessing import Pool, cpu_count

def gen_safe_prime(bits=256):
    while True:
        p_ = next_prime(mpz_urandomb(rand, bits - 1))
        p = 2 * p_ + 1
        if is_prime(p, 25) and p % 4 == 3:
            return p

def hybrid_generator(x, N, s, taps, k=8, n=10**6):
    output = []
    for _ in range(n):
        lsb_s = s & 1
        lsb_x = x & 1
        new_bit = 0
        for i in taps:
            new_bit ^= (s >> i) & 1
        s = ((s << 1) | new_bit) & ((1 << k) - 1)
        exp = 2 + (lsb_s ^ lsb_x)
        x = powmod(x, exp, N)
        out = ((s >> (k - 1)) & 1) ^ (x & 1)
        output.append(int(out))
    return output

def bbs_generator(x, N, n=10**6):
    output = []
    for _ in range(n):
        x = powmod(x, 2, N)
        out = x.bit_count() & 1
        output.append(out)
    
    return output

def write_bits_to_bin(bits):
    output_bytes = bytearray()
    byte = 0
    count = 0
    for bit in bits:
        byte = ((byte << 1) & 0xFF) | bit
        count += 1
        if count == 8:
            output_bytes.append(byte)
            byte = 0
            count = 0
    if count > 0:
        byte = (byte << (8 - count)) & 0xFF
        output_bytes.append(byte)
    return output_bytes

def generate_stream(i, N):
    seed = 42 + i
    sreg = (121 + i) % 256
    bits = hybrid_generator(seed, N, sreg, [3, 4, 6])
    return write_bits_to_bin(bits)

def worker(args):
    i, N = args
    return i, generate_stream(i, N)


def write_hybrid_test_stream(file):

    p = gen_safe_prime()
    q = gen_safe_prime()
    while q == p:
        q = gen_safe_prime()
    N = p * q
    counter = 500
    start_time = time()

    # multiproc
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(worker, [(i, N) for i in range(counter)])

    results.sort()

    #need to write in order
    with open(file, "wb") as f:
        for i, data in results:
            f.write(data)

    print(f"Hybrid Completed.\nTotal time: {time() - start_time:.2f} seconds")


if __name__ == "__main__":
    rand = random_state(int(time()))
    write_hybrid_test_stream("hybrid_test_stream.bin")
