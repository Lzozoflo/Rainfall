from pwn import *

def run_level(user, pwd, binary_name):

    connection = ssh(host="localhost", user=user, password=pwd, port=4242)
    sh = connection.process("/bin/bash") # sh = bash at the home user


    # output = sh.recvall(timeout=2) 


    sh.sendline(f"./{binary_name}".encode())

    # payload
    sh.sendline(b"test")


    

    # sh.interactive()










    sh.close()
    connection.close()
    return "chaussure"