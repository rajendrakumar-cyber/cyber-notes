import hashlib

# Read the target hash
with open('level5.hash.bin', 'rb') as f:
    target_hash = f.read()

# Read the encrypted flag
with open('level5.flag.txt.enc', 'rb') as f:
    flag_enc = f.read().decode()

# Function to XOR decrypt (copied from level5.py)
def str_xor(secret, key):
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)
    return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c, new_key_c) in zip(secret, new_key)])

# Iterate through the dictionary
with open('dictionary.txt', 'r') as f:
    for line in f:
        password = line.strip() # Remove newline characters
        if not password:
            continue
            
        # Calculate MD5 hash
        candidate_hash = hashlib.md5(password.encode()).digest()
        
        if candidate_hash == target_hash:
            print(f"Password found: {password}")
            # Decrypt the flag
            flag = str_xor(flag_enc, password)
            print(f"Flag: {flag}")
            break
