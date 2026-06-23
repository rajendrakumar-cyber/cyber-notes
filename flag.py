python3 - << 'EOF'
import base64, sympy

with open('/mnt/data/Pasted text(2).txt','r',errors='ignore') as f:
    data=f.read().splitlines()

for line in data:
    line=line.strip()
    if line.startswith("dGhte"):
        try:
            dec=base64.b64decode(line).decode()
            if dec.startswith("thm{"):
                nums=list(map(int,dec[4:-1].split(',')))
                primes=sum(sympy.isprime(n) for n in nums)
                if primes==3:
                    print(dec)
        except:
            pass
EOF
