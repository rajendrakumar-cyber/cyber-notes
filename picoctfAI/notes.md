# PicoCTF Forensics Challenge Notes

This document compiles the flags, files, and techniques used to solve the various forensics and steganography challenges in this workspace.

---

## 1. Challenge: Extensions

* **Target File:** [flag.png](file:///home/white/white/Music/PICO-CTF/forencisis/flag.png) (originally named `flag.txt`)
* **Description:** The challenge tests the understanding of file signatures/magic bytes vs. file extensions.
* **Method:** 
  1. Ran `file flag.png` to inspect the magic bytes of the file, showing it was actually a PNG image:
     ```bash
     flag.png: PNG image data, 1697 x 608, 8-bit/color RGB, non-interlaced
     ```
  2. Opened the file as an image to read the flag.
* **Flag:** `picoCTF{now_you_know_about_extensions}`

---

## 2. Challenge: Sleuthkit Apprentice

* **Target File:** [disk.flag.img](file:///home/white/white/Music/PICO-CTF/forencisis/disk.flag.img)
* **Description:** A forensics challenge involving disk image investigation using Sleuthkit tools.
* **Method:**
  1. Listed partitions using `mmls` or `binwalk` to identify the starting sector offset for the Linux ext4 partitions (offset: `360448` sectors).
  2. Explored the file system history using `fls` to list `/root`'s home directory. The `.ash_history` file showed:
     ```bash
     iconv -f ascii -t utf16 flag.txt > flag.uni.txt
     shred -zu flag.txt
     ```
  3. Located the `flag.uni.txt` file (inode `2371`) inside `/root/my_folder`.
  4. Extracted `flag.uni.txt` to read the UTF-16 encoded flag.
* **Flag:** `picoCTF{by73_5urf3r_adac6cb4}`

---

## 3. Challenge: pico.flag.png (Steganography)

* **Target File:** [pico.flag.png](file:///home/white/white/Music/PICO-CTF/forencisis/pico.flag.png)
* **Description:** LSB (Least Significant Bit) steganography challenge.
* **Method:**
  1. Ran `zsteg pico.flag.png` to analyze the least significant bits of the image.
  2. Found the hidden text in the `b1,rgb,lsb,xy` data stream.
* **Flag:** `picoCTF{7h3r3_15_n0_5p00n_96ae0ac1}`

---

## 4. Challenge: buildings.png (Steganography)

* **Target File:** [buildings.png](file:///home/white/white/Music/PICO-CTF/forencisis/buildings.png)
* **Description:** LSB steganography challenge.
* **Method:**
  1. Ran `zsteg buildings.png` to inspect the image layers.
  2. Found the hidden flag in the `b1,rgb,lsb,xy` data stream.
* **Flag:** `picoCTF{h1d1ng_1n_th3_b1t5}`

---

## 5. Challenge: Forencisis

* **Target File:** [logs.txt](file:///home/white/white/Music/PICO-CTF/forencisis/logs.txt) / [flag.png](file:///home/white/white/Music/PICO-CTF/forencisis/flag.png)
* **Description:** Base64 decoding and image analysis/hex translation.
* **Method:**
  1. Decoded the Base64 data inside `logs.txt` to retrieve a PNG file `flag.png` (dimensions 896 x 1152):
     ```bash
     base64 -d logs.txt > flag.png
     ```
  2. Inspected the resulting image to find a hexadecimal string embedded at the bottom:
     `7069636F4354467B666F72656E736963735F616E616C797369735F69735F616D617A696E675F35636363376362307D`
  3. Decoded the hexadecimal string to reveal the ASCII flag:
     ```bash
     python3 -c "import binascii; print(binascii.unhexlify('7069636F4354467B666F72656E736963735F616E616C797369735F69735F616D617A696E675F35636363376362307D').decode())"
     ```
* **Flag:** `picoCTF{forensics_analysis_is_amazing_5ccc7cb0}`

---

## 6. Challenge: Corrupted file

* **Target File:** [file](file:///home/white/white/Music/PICO-CTF/forencisis/file) / [restored.jpg](file:///home/white/white/Music/PICO-CTF/forencisis/restored.jpg)
* **Description:** Fixing a corrupted file header to restore a JPEG image.
* **Method:**
  1. Ran `file file` which showed it was generic `data` instead of a recognized format.
  2. Inspected the first 32 bytes of the file in hex:
     `5c 78 ff e0 00 10 4a 46 49 46 ...`
  3. Identified that the header matches a JPEG file with APP0 `JFIF` segment, but the first two bytes are `5c 78` (representing `\x` in ASCII) instead of `ff d8`.
  4. Restored the correct JPEG Start of Image (SOI) bytes:
     ```bash
     python3 -c "data = bytearray(open('file', 'rb').read()); data[0:2] = b'\xff\xd8'; open('restored.jpg', 'wb').write(data)"
     ```
  5. Opened `restored.jpg` to read the flag.
* **Flag:** `picoCTF{r3st0r1ng_th3_by73s_31cc795d}`

---

## 7. Challenge: DISKO 1

* **Target File:** [disko-1.dd](file:///home/white/white/Music/PICO-CTF/forencisis/disko-1.dd)
* **Description:** Finding a flag in a raw FAT32 disk image.
* **Method:**
  1. Ran `file disko-1.dd` which showed it was a FAT32 filesystem / MBR boot sector.
  2. Searched the raw binary file for string representations of the picoCTF flag pattern:
     ```bash
     strings disko-1.dd | grep -i pico
     ```
  3. Found the plain text flag.
* **Flag:** `picoCTF{1t5_ju5t_4_5tr1n9_be6031da}`

---

## 8. Challenge: Red Steganography

* **Target File:** [red.png](file:///home/white/white/Music/PICO-CTF/forencisis/red.png)
* **Description:** Steganography challenge hidden in the LSB of image channels.
* **Method:**
  1. Ran `zsteg red.png` to inspect the image layers.
  2. Found a Base64-encoded string repeated in the `b1,rgba,lsb,xy` data stream:
     `cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==`
  3. Decoded the Base64 string to reveal the flag.
* **Flag:** `picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}`

---

## 9. Challenge: Network Traffic Analysis

* **Target File:** [myNetworkTraffic.pcap](file:///home/white/white/Music/PICO-CTF/forencisis/myNetworkTraffic.pcap)
* **Description:** Analysis of TCP payloads in network packet captures.
* **Method:**
  1. Extracted and sorted TCP payloads from the `.pcap` capture file:
     ```bash
     tshark -r myNetworkTraffic.pcap -T fields -e frame.time -e tcp.payload 2>/dev/null | sort -n | cut -f2 | xxd -r -p | base64 -d
     ```
  2. The decoded stream reconstructed the flag.
* **Flag:** `picoCTF{1t_w4snt_th4t_34sy_tbh_4r_d1065384}`

---

## 10. Challenge: Verify

* **Target File:** SSH Sandbox (`rhea.picoctf.net`)
* **Description:** Verification of file checksums to decrypt the correct flag file.
* **Method:**
  1. Computed and grepped for the correct SHA256 checksum from the list:
     ```bash
     sha256sum files/* | grep 55b983afdd9d10718f1db3983459efc5cc3f5a66841e2651041e25dec3efd46a
     ```
  2. Identified `files/2cdcb2de` as the matching file and decrypted it:
     ```bash
     ./decrypt.sh files/2cdcb2de
     ```
* **Flag:** `picoCTF{trust_but_verify_2cdcb2de}`

---

## 11. Challenge: QR Code Peek-a-boo

* **Target File:** [flag.png](file:///home/white/white/Music/PICO-CTF/forencisis/home/ctf-player/drop-in/flag.png) (extracted from `challenge.zip`)
* **Description:** Scanning a hidden QR Code inside a PNG image.
* **Method:**
  1. Extracted the file `flag.png` from `challenge.zip`.
  2. Scanned the QR Code using `zbarimg`:
     ```bash
     zbarimg flag.png
     ```
* **Flag:** `picoCTF{p33k_@_b00_b5ce2572}`

---

## 12. Challenge: Secret of the Polyglot

* **Target File:** [flag2of2-final.pdf](file:///home/white/white/Music/PICO-CTF/forencisis/flag2of2-final.pdf)
* **Description:** Extracting information from a file that is a valid PNG and PDF simultaneously.
* **Method:**
  1. Inspected file type of `flag2of2-final.pdf` which showed it was actually a PNG image:
     ```bash
     file flag2of2-final.pdf
     ```
  2. Opened the file as a PNG image to read the first half of the flag (`picoCTF{f13u3n7_`).
  3. Extracted PDF text using `pdftotext` to read the second half of the flag (`1n_pn9_&_pdf_90974127}`).
  4. Concatenated both halves to get the full flag.
* **Flag:** `picoCTF{f13u3n7_1n_pn9_&_pdf_90974127}`

---

## 13. Challenge: CanYouSee

* **Target File:** [ukn_reality.jpg](file:///home/white/white/Music/PICO-CTF/forencisis/ukn_reality.jpg) (extracted from `unknown.zip`)
* **Description:** Extracting hidden base64 encoded flags from image metadata.
* **Method:**
  1. Extracted metadata from `ukn_reality.jpg` using `exiftool`:
     ```bash
     exiftool ukn_reality.jpg
     ```
  2. Located a Base64-encoded string inside the `Attribution URL` field:
     `cGljb0NURntNRTc0RDQ3QV9ISUREM05fZDhjMzgxZmR9Cg==`
  3. Decoded the Base64 string to retrieve the flag.
* **Flag:** `picoCTF{ME74D47A_HIDD3N_d8c381fd}`

---
*Notes compiled on 2026-07-14.*
