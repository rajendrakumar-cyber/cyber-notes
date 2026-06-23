import hashlib

username = "BENNETT"
# Calculate SHA-256 hash
hash_hex = hashlib.sha256(username.encode()).hexdigest()

# The indices used in the code (0-indexed)
# Note: The code uses 1-based logic in the description, but Python is 0-indexed.
# The code accesses: , , , , , , , 
# These are the correct 0-based indices.
indices = [4, 5, 3, 6, 2, 7, 1, 8]

# Construct the suffix
suffix = "".join([hash_hex[i] for i in indices])

# Construct the full key
prefix = "picoCTF{1n_7h3_kk3y_of_"
full_key = prefix + suffix + "}"

print(f"SHA-256 of {username}: {hash_hex}")
print(f"Generated Key: {full_key}")
