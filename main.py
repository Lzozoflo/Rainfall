import level00.Ressource.Script.script as l00
import level00.Ressource.Script.payload as pl00
import level01.Ressource.Script.script as l01
import level01.Ressource.Script.payload as pl01
import sys

p00 = pl00.payload()
r00 = l00.run_level(user="level00", pwd="level00", binary_name="case", payload=p00)
print("[+] Pwd Level00: " + r00)

p01 = pl01.payload()
r01 = l01.run_level(user="level01", pwd=r00, binary_name="ono", payload=p01)
print("[+] Pwd Level01: " + r01)