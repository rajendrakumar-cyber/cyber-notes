Today I practiced creating and managing users in Linux using LabEx.

1>>Creating a User

First attempt without sudo:

useradd b.smith

Result:
Permission denied.
This showed that normal users cannot modify system files like /etc/passwd.

Then I used sudo:

sudo useradd b.smith

Verified the user:

id b.smith

Output showed:
uid=5002(b.smith) gid=5004(b.smith)

Checked inside passwd file:

grep "b.smith" /etc/passwd

Confirmed user entry exists.

2>>Creating Home Directory

Tried:

sudo useradd -m -d /home/b.smith b.smith

But user already existed.

So I deleted and recreated:

sudo userdel b.smith
sudo useradd -m -d /home/b.smith b.smith

Verified home directory:

ls -ld /home/b.smith

Directory was created successfully.

3>>Setting Password

sudo passwd b.smith

Password updated successfully.

This shows password hashes are managed securely.

4>>Adding User to Group

Added user to developers group:

sudo usermod -aG developers b.smith

Verified:

id b.smith

Output showed:
groups=5004(b.smith),5003(developers)

5>>Checked group file:

grep "^developers:" /etc/group

Confirmed user added to group.

Locking User Account

6>>Locked account:

sudo usermod -L j.doe

Verified in shadow file:

sudo grep j.doe /etc/shadow

Output showed:

j.doe:!:

The "!" symbol means the account is locked.

Mistakes I Noticed

I accidentally typed:

grep "b.smith" /etc/passwdd

There is no file called /etc/passwdd.
Correct file is /etc/passwd.

