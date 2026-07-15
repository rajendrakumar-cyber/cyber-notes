from pwn import *
from string import ascii_letters, digits
import json
from tqdm import trange


def gen_plaintext(length):
    return ''.join(random.choice(ascii_letters + digits) for _ in range(length))


pt = [gen_plaintext(16) for _ in range(50)]
print(pt)
json_file = [None] * len(pt)

for i in trange(len(pt)):
    r = remote('saturn.picoctf.net', 61161)
    r.sendlineafter(b'hex: ', pt[i].encode('utf-8').hex().encode())
    r.recvuntil(b'power measurement result:  ')
    pm = r.recvline().decode().strip()
    json_file[i] = {}
    json_file[i]["pt"] = [ord(digit) for digit in pt[i]]
    json_file[i]["pm"] = pm

    r.close()

json_object = json.dumps(json_file)
with open("./Crypto/PowerAnalysis- Part 1/trace.json", 'w') as outfile:
    outfile.write(json_object)
