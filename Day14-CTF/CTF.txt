Today I practiced CTF (Capture The Flag) challenges in the lab environment.

CTF challenges are designed to improve practical cybersecurity skills.
They simulate real-world security problems in a safe and legal way.

What I worked on:

Basic file analysis

Linux commands (cat, ls, diff, chmod)

File permissions and access control

Encryption and decryption concepts

Searching for hidden flags in directories

I learned that CTF challenges require:

Careful observation

Reading error messages properly

Understanding file ownership and permissions

Thinking logically before running commands

In one challenge, I explored directories and checked permissions using:

ls -l
ls -ld
cat filename

I noticed some files were restricted due to permissions.
This helped me understand how Linux protects sensitive files.

I also practiced encryption using OpenSSL and compared files using:

diff file1 file2


====================
labex:secret/ $ ls
decoy.conf  flag.txt
labex:secret/ $ ls -ld /etc/secret
drwxr-xr-x 2 root root 40 Feb 13 23:40 /etc/secret
labex:secret/ $ ls -l /etc/secret 
total 8
-rw-r----- 1 root  root  42 Feb 13 23:40 decoy.conf
---------- 1 labex labex 31 Feb 13 23:40 flag.txt
labex:secret/ $ cat /etc/secret/decoy.conf
cat: /etc/secret/decoy.conf: Permission denied
labex:secret/ $ chmod 600 /etc/secret/flag.txt
labex:secret/ $ cat flag.txt 
labex{p3rm15510n_3spl017_fl4g}
                                