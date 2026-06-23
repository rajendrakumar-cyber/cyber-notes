import base64

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

with open("thm_flags.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        decoded = base64.b64decode(line).decode()
        nums = list(map(int, decoded[4:-1].split(",")))

        prime_count = sum(is_prime(x) for x in nums)

        if prime_count == 3:
            print("REAL FLAG:", decoded)
            break
