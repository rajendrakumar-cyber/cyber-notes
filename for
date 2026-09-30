Today you've been grinding through picoCTF Academy Forensics (Medium) challenges:

Weird File Forensics Medium — extracted a VBA macro from a .docm, decoded base64 → academy{m4cr0s_r_d4ng3r0us}
Pitter, Patter, Platters — found flag in slack space using strings -e l | rev → academy{b3_5t111_mL|_<3_d18a1e1e}
Shark on Wire 2 — decoded flag from UDP source ports (port − 5000 = ASCII) → academy{p1LLf3r3d_data_v1a_st3g0}
Like1000 — extracted 1000 nested .tar files in a loop → academy{l0t5_0f_TAR5}
c0rrupt — fixing a corrupted PNG header byte-by-byte in hexedit (in progress)
Basically: forensics bootcamp — VBA macros, disk slack space, network steganography, nested archives, and binary file repair. Solid session.


Copy


Elaborate


Summarized c0rrupt challenge techniques
Your Forensics Session — Detailed Breakdown
1. Weird File Forensics Medium
Concept: Office file macro extraction

.docm = Word file with macros enabled (OLE compound document containing OpenXML + VBA)
The VBA code was compressed using MS-OVBA compression (a custom RLE-like algorithm), which is why strings couldn't find the base64 payload
olevba (from oletools) handles decompression automatically
The macro used AutoOpen (triggers on file open) + Shell() to run Python, which printed a base64 string
Key lesson: Never enable macros in untrusted documents. olevba is your go-to tool.

olevba oletools documentation

View all
2. Pitter, Patter, Platters
Concept: Slack space steganography

Slack space = the unused padding between the end of a file's data and the end of its allocated disk block (typically 4096 bytes on ext3/4)
The flag was hidden after the visible file content, encoded in UTF-16LE (each ASCII char followed by \x00) and reversed
strings -e l extracts little-endian 16-bit strings; rev reverses them
fls/icat (from sleuthkit) let you inspect filesystem metadata and file contents from a raw disk image
Key lesson: Data can hide in "empty" space on a disk. strings -e l | rev is a quick check.
3. Shark on Wire 2
Concept: Network steganography (UDP port encoding)

The flag was encoded in UDP source ports: sport - 5000 = ASCII character
Packets were sent from 10.0.0.66 to 10.0.0.1 on dport 22 (mimicking SSH to avoid suspicion)
tshark (CLI Wireshark) or scapy (Python) extract the ports programmatically
Key lesson: Any field in a packet can carry hidden data — ports, TTL, packet sizes, timing, etc.

Shark on Wire 2 tutorial

View all
4. Like1000
Concept: Nested archive extraction

1000 .tar files, each containing the next one (1000.tar → 999.tar → ... → 1.tar → flag.png)
A simple for loop handles it: for i in {1000..1}; do tar -xf $i.tar; done
Key lesson: Script repetitive tasks. 1000 manual extractions would take forever.
5. c0rrupt (in progress)
Concept: Binary file repair / format knowledge

A PNG with 5 corrupted spots: magic bytes, chunk names, and chunk lengths
PNG structure: 8-byte signature → chunks (4-byte length + 4-byte name + data + 4-byte CRC)
Each chunk name must be valid ASCII (IHDR, pHYs, IDAT, IEND)
The AA bytes were the giveaway — clearly invalid in their context
Key lesson: Understanding file format specs lets you repair corrupted files by hand. pngcheck validates the result.
Skills you've practiced today:
Skill	Tools
OLE/VBA extraction	olevba, oletools
Base64 decoding	base64 -d
Disk forensics	fls, icat, strings -e l
Network analysis	tshark, scapy, tcpdump
Archive handling	tar
Binary editing	hexedit, xxd
File format knowledge	PNG spec, OLE compound files, ext3

You've covered a solid range of forensics techniques in one session.


Copy


