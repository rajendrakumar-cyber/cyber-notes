import socket
import concurrent.futures
import time
import sys

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

HOST = "saturn.picoctf.net"
PORT = 60174

def query_server_once(pt_hex):
    for attempt in range(5):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.connect((HOST, PORT))
            
            data = b""
            while b":" not in data:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
            
            s.sendall(pt_hex.encode() + b"\n")
            
            resp = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                resp += chunk
            
            s.close()
            resp_str = resp.decode()
            if "leakage result:" in resp_str:
                val = resp_str.split("leakage result:")[1].strip()
                return int(val)
        except Exception as e:
            # Sleep slightly longer on consecutive retries to let server recover
            time.sleep(1.0 + attempt * 0.5)
            continue
    raise RuntimeError(f"Failed to query server for plaintext {pt_hex} after 5 attempts")

results = {i: {} for i in range(16)}

# 1. Base phase: 16 queries per byte
print("Starting base phase (16 queries per byte)...")
start_time = time.time()

base_tasks = []
for i in range(16):
    for x in range(16):
        pt = bytearray(16)
        pt[i] = x
        base_tasks.append((i, x, pt.hex()))

def worker(task):
    byte_idx, x, pt_hex = task
    leak = query_server_once(pt_hex)
    return byte_idx, x, leak

# We run with max_workers=3
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(worker, task) for task in base_tasks]
    for idx, future in enumerate(concurrent.futures.as_completed(futures)):
        try:
            byte_idx, x, leak = future.result()
            results[byte_idx][x] = leak
            if (idx + 1) % 25 == 0 or idx == len(base_tasks) - 1:
                print(f"Completed {idx + 1}/{len(base_tasks)} base queries...")
        except Exception as e:
            print(f"CRITICAL: error in base query: {e}")
            sys.exit(1)

print(f"Base phase completed in {time.time() - start_time:.2f} seconds.")

# Helper to find candidates for a given byte
def get_candidates(byte_idx):
    measurements = sorted(results[byte_idx].items())
    candidates = []
    for k in range(256):
        diffs = []
        for x, leak in measurements:
            diffs.append(leak - (Sbox[x ^ k] & 0x01))
        if len(set(diffs)) == 1:
            candidates.append((k, diffs[0]))
    return candidates

# 2. Adaptive refinement phase
print("\nStarting adaptive refinement phase...")
refinement_queries = 0

for target_byte in range(16):
    candidates = get_candidates(target_byte)
    print(f"Byte {target_byte}: initially {len(candidates)} candidates.")
    
    # If more than 1 candidate, query more values of x for this byte
    x_next = 16
    while len(candidates) > 1 and x_next < 256:
        pt = bytearray(16)
        pt[target_byte] = x_next
        
        # Get the measurement
        try:
            leak = query_server_once(pt.hex())
            results[target_byte][x_next] = leak
            refinement_queries += 1
        except Exception as e:
            print(f"CRITICAL: error in refinement query for Byte {target_byte}, x={x_next}: {e}")
            sys.exit(1)
            
        candidates = get_candidates(target_byte)
        x_next += 1
        
    print(f"Byte {target_byte}: resolved to {len(candidates)} candidates after querying up to x={x_next-1}.")

# Check final key
recovered_key = bytearray(16)
success = True
for target_byte in range(16):
    candidates = get_candidates(target_byte)
    if len(candidates) == 1:
        recovered_key[target_byte] = candidates[0][0]
    else:
        print(f"Error: Could not uniquely identify byte {target_byte}")
        success = False

print(f"Total refinement queries made: {refinement_queries}")

if success:
    key_hex = recovered_key.hex()
    print("\n--- RECOVERY SUCCESSFUL ---")
    print(f"Recovered Key (hex): {key_hex}")
    print(f"Flag: picoCTF{{{key_hex}}}")
else:
    print("\n--- RECOVERY FAILED ---")
