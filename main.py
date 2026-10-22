import level00.Ressource.Script.script as l00
import level00.Ressource.Script.payload as pl00
import sys

p00 = pl00.payload()
r00 = l00.run_level(user="level00", pwd="level00", binary_name="case", payload=p00)

print("[+] Pwd Level00: " + r00)