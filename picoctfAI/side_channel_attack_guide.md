# Side-Channel Attack Guide: Correlation Power Analysis (CPA) on AES

This guide outlines the step-by-step methodology to solve AES Side-Channel Power Analysis challenges. It covers the physics of the leakage, mathematical modeling, trace collection strategies, and windowing (template) techniques to resolve keys when trace counts are limited.

---

## Overview of the Attack
In microprocessors and hardware systems, logic gates consuming power charge and discharge internal capacitances. This dynamic power consumption is directly correlated with:
1. **The values of the data bits being processed** (Hamming Weight model).
2. **The number of bits changing state** (Hamming Distance model).

By analyzing power traces recorded during the execution of cryptographic algorithms (like AES-128), we can correlate our guesses of the secret key bytes with the measured power consumption.

```mermaid
graph TD
    A[Collect Traces: Plaintexts & Power Traces] --> B[Model Intermediate State: Sbox[P_i ^ K_i]]
    B --> C[Compute Hypothetical Hamming Weights]
    C --> D[Calculate Pearson Correlation Coefficients]
    D --> E{High Noise / Few Traces?}
    E -- Yes --> F[Apply Windowed CPA / Template Attack]
    E -- No --> G[Recover Key from Global Correlation Peaks]
    F --> H[Recover Key within Target Windows]
    G --> I[Done]
    H --> I
```

---

## Step 1: Modeling the Leakage
To attack a software AES implementation, we target the output of the first-round **Sbox (SubBytes)** operation. The Sbox is non-linear, which ensures that incorrect key guesses do not correlate with the power measurements.

For each byte index $i \in [0, 15]$:
1. **Intermediate State**: We guess a key byte candidate $k \in [0, 255]$ and compute:
   $$V = \text{Sbox}[P_i \oplus k]$$
   where $P_i$ is the known plaintext byte.
2. **Leakage Metric**: We translate the intermediate byte value $V$ to its **Hamming Weight** (number of $1$ bits in binary).
   $$HW(V) = \sum \text{bits}(V)$$

---

## Step 2: Collecting Traces
### A. Collecting Traces via Server Queries (Part 1)
When collecting power traces from a live server, follow these rules:
- **Randomize the plaintext**: Ensure all bytes of the plaintext are random in each query. This keeps other bytes' operations uncorrelated, making the target byte stand out.
- **Respect connection limits**: PicoCTF containers rate-limit connections. Use concurrent thread pools with a small number of workers (typically 3) and robust retry logic to handle dropped packets.
- **Avoid NumPy encoding bugs**: In Python, raw `bytes` arrays passed directly to NumPy can truncate at trailing null bytes (`\x00`). Always store the plaintexts as integer arrays or pad them using `.ljust(16, b'\x00')` to preserve shape.

### B. Parsing Provided Traces (Part 2)
If the traces are pre-collected (as in Part 2), parse them sequentially from the filesystem:
1. Read the Plaintext hex string and convert it to a list of bytes.
2. Read the Power trace list string (using `eval` or `json.loads`) into an array of floats.

---

## Step 3: Correlation Power Analysis (CPA) Math
To identify the correct key byte candidate, we compute the **Pearson Correlation Coefficient** ($\rho$) between our Hamming weight hypotheses matrix $H$ and the actual power trace matrix $Y$.

For $D$ traces and a trace length of $T$:
- $H$ is a matrix of shape $(D, 256)$ representing predictions for all candidate keys.
- $Y$ is a matrix of shape $(D, T)$ representing the power trace signals.

$$\rho_{k, t} = \frac{\sum_{d=1}^{D} (H_{d, k} - \bar{H}_k)(Y_{d, t} - \bar{Y}_t)}{\sqrt{\sum_{d=1}^{D} (H_{d, k} - \bar{H}_k)^2} \sqrt{\sum_{d=1}^{D} (Y_{d, t} - \bar{Y}_t)^2}}$$

For the correct candidate $k = K_i$, there will be a time index $t$ corresponding to the Sbox operation where $|\rho|$ is significantly higher than the noise level ($1/\sqrt{D}$).

### Efficient Vectorized CPA in NumPy
Using Python loops for this calculation is extremely slow. We can compute the correlation matrix for all 256 candidates across all time points instantly using NumPy matrix operations:

```python
# Subtract means to center the matrices
H_centered = H - np.mean(H, axis=0, keepdims=True)
Y_centered = Y - np.mean(Y, axis=0, keepdims=True)

# Standard deviations
H_std = np.sqrt(np.sum(H_centered**2, axis=0))
Y_std = np.sqrt(np.sum(Y_centered**2, axis=0))

# Avoid division by zero
H_std[H_std == 0] = 1.0
Y_std[Y_std == 0] = 1.0

# Calculate correlation matrix
corr_matrix = np.abs(np.dot(H_centered.T, Y_centered) / np.outer(H_std, Y_std))
```

---

## Step 4: Windowing (Overcoming Limited Traces)
When trace counts are limited (e.g., only 100 traces in Part 2), the background noise is high enough that incorrect candidates will exhibit random correlation peaks at wrong time indices.

### The Windowing Strategy
If the target system running the AES encryption is identical to a profiled run (Part 1):
1. **Identify Operation Times**: Extract the exact peak times ($t_i$) for each byte $i$ from a clean, large trace-set run.
2. **Restrict the Search**: During the limited trace-set attack, search only in a tiny window around $t_i$ (e.g., $[t_i - 2, t_i + 2]$).
3. **Filter Out Noise**: This ignores all random noise peaks occurring outside the Sbox execution window, yielding a clear correlation ratio for the correct candidate.

### Target Windows Profile
Based on our profiling of the PicoCTF AES firmware, the Sbox operations occur at these exact time indices:

| Byte Index | Sbox Time Sample ($t_i$) |
|:---:|:---:|
| **Byte 0** | 326 |
| **Byte 1** | 326 |
| **Byte 2** | 360 |
| **Byte 3** | 327 |
| **Byte 4** | 354 |
| **Byte 5** | 351 |
| **Byte 6** | 332 |
| **Byte 7** | 331 |
| **Byte 8** | 384 |
| **Byte 9** | 335 |
| **Byte 10**| 335 |
| **Byte 11**| 391 |
| **Byte 12**| 364 |
| **Byte 13**| 337 |
| **Byte 14**| 358 |
| **Byte 15**| 379 |

---

> [!TIP]
> **Dealing with Misalignment**: If traces are misaligned due to CPU clock jitter, align them beforehand using **Dynamic Time Warping (DTW)** or **Cross-Correlation** alignment techniques against a reference trace before running the CPA analysis.
