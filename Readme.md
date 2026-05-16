```sh
chmod 777 .
ll
find / -user $USER  2>/dev/null | grep -v "^/proc"
find / -user flag  2>/dev/null | grep -v "^/proc"
```