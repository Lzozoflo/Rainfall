# level00

In the home user we have:

```sh

```

<br>

---

<br>


## Expected Exploit


<br>

---

<br>

## Exploit

```
unset environment
disas run_diagnostic
break *0x4013b8
<!-- 0x00000000004013b8 this is the line that calls read itself -->
info reg rsi
```
