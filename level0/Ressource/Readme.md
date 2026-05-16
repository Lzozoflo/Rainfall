# level0


```sh
level0@RainFall:~$ 


level0@RainFall:~$ chmod 777 .


level0@RainFall:~$ ll


total 737
-rwsr-x---+ 1 level1 users  747441 Mar  6  2016 level0*


level0@RainFall:~$ find / -user $USER  2>/dev/null | grep -v "^/proc"


level0@RainFall:~$ ./level0 
Segmentation fault (core dumped)


```

i have used ghidra do decompile "level0"

there is the binary file in the rainfall vm [/home/user/level0/level0](./level0)



## copy the file on hote machine
```sh
scp -P 4242  level0@127.0.0.1:/home/user/level0/level0 $drain/level00/Ressource
``` 


then the binary file need an argument (param_2 = argv)
```c
  iVar1 = atoi(*(char **)(param_2 + 4));
  if (iVar1 == 0x1a7) {
```
he check atoi of the arg[1] if its [423](https://www.rapidtables.com/convert/number/hex-to-decimal.html?x=1A7)

so ...
```sh
level0@RainFall:~$ ./level0 423
$
```
we got need sh with the right of the binary file (level1) then
```sh
$ cat /home/user/level1.pass	
1fe8a524fa4bec01ca4ea2a869af2a02260d4a7d5fe7e7c24d8617e6dca12d3a
``` 