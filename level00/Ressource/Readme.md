# level00

In the home user we have:

```sh
level00@RainFall:~$ 

-rwsr-x---  1 flag00  level00 16792 Jun  9 23:13 case*
-r--r--r--  1 level00 level00  2416 Jun  9 23:13 case.c
-r--r--r--  1 level00 level00    77 Jun  9 23:13 README
```

<br>

---

<br>

## case

binary file to execute with ur user with suid byte priviagle on flag00

<br>

---

<br>

## case.c

Its was the source code of the binary file [case.c](./source_code/case.c)

<br>

---

<br>

## README

in the file:  
```txt
The sky above the port was the color of television, tuned to a dead channel.
```

<br>

---

<br>

## theorie Exploit


```c
static void auth_loop(void) {       // rbp + 8 return addr (8 octets) rbp : last RBP  (8 octets) = (16 octets)
    char credentials[64];           // credentials = potential stack exploit  (64 octet)
    int sid = create_session();     // int sid on the stack count on the padding value (4 octect + 4 padding octect)

    ...

    gets(credentials);              // with get we can input in credentials

    ...
                                    // return addr at 88 to 94 ((8 + 8) + 64 + (4 + 4)) from the start of credentials
}
```

<br>

la vm est en 64 bit il faut donc faire des cacule avec  
  
> rbp + 8 : return addr (8 octets)  
> 8 octets  
> rbp :     last addr (8 octets)  
> 16 octets  
> rbp - 4 : sid (4 octets)  
> 20 octets  
> rbp - 4 : padding (4 pour aligner RBP sur 8) 
> 24 octets  
> rbp - 0x40 : credentials (64 octets)  
> 88 octets  

so now we have to find the start addr of credentials inject a NOP byte + shellcode + replace the return addr by the start of credentials 

<br>

---

<br>

## Exploit

find start of credentials with gdb :
```
break auth_loop
run 
print $rbp - 0x50
    $1 = (void *) 0x7fffffffe210
```
credentials addr = `0x7fffffffe210`

