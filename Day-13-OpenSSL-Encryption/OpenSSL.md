OpenSSL Encryption Practice – Lab Notes

Today I practiced file encryption and decryption using OpenSSL in the lab environment.

First, I checked the OpenSSL version:

openssl version

It showed OpenSSL 3.0.2.

Then I created a simple text file:

echo "LabEx has the best labs for fun, hands-on learning." > secret.txt

I verified the content using:

cat secret.txt

After that, I encrypted the file using AES-256-CBC:

openssl enc -aes-256-cbc -salt -in secret.txt -out secret.enc -pbkdf2

The system asked me to enter a password.
After encryption, a new file called secret.enc was created.

When I opened secret.enc using cat, the content was unreadable.
This confirmed that the file was properly encrypted.

To decrypt the file, I used:

openssl enc -aes-256-cbc -d -in secret.enc -out decrypted.txt -pbkdf2

After entering the correct password, I checked the decrypted file:

cat decrypted.txt

The original message appeared again.

I also compared the original and decrypted files:

diff secret.txt decrypted.txt

There was no difference, which means the encryption and decryption worked correctly.

What I learned today:

Encryption converts readable data into unreadable format.

AES-256-CBC is a strong encryption algorithm.

The -salt option improves security by adding randomness.

The -pbkdf2 option strengthens password-based encryption.

Without the correct password, decryption should fail.

Encryption is important for protecting sensitive data.

This lab helped me understand practical encryption, not just theory.