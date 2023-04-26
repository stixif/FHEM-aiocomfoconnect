# FHEM-aiocomfoconnect
aiocomfoconnect script für FHEM

um AIOComfoconnect von michaelarnauts mit FHEM zu verwenden
https://github.com/michaelarnauts/aiocomfoconnect

aiocomfo_sensors.py
is zum auslesen der Sensoren und schreiben als Reading ins FHEM Dummy

aiocomfo_set.py
hiermit kann die Lüftung über FHEM gesteuert werden

Fehler:
aus einem mir noch nicht bekannten grund will der BOOST und der AWAY_Mode noch nicht so ganz...
eine einzele aktivierung mit dem aufruf
await comfoconnect.set_boost(True, timeout=100) <- funktioniert
