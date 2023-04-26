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




mein FHEM DUMMY:

defmod comfoconnect dummy
attr comfoconnect devStateIcon {".*:vent_ventilation_level_".ReadingsVal("$name","Fan_Speed",0).(ReadingsVal("$name","Operating_Mode",0) ne -1 ? '@green' : "")}
attr comfoconnect event-min-interval .*:800
attr comfoconnect event-on-change-reading .*:30
attr comfoconnect event-on-update-reading .*:300
attr comfoconnect userReadings Operating_ModeTXT {if(ReadingsVal("$name","Operating_Mode","") == -1) {return "Auto"} elsif (ReadingsVal("$name","Operating_Mode","") == 1) {return "Manuell Zeit"} elsif (ReadingsVal("$name","Operating_Mode","") == 5) {return "Manuell"} elsif (ReadingsVal("$name","Operating_Mode","") == 6) {return "Party Timer"}elsif (ReadingsVal("$name","Operating_Mode","") == 0) {return "Abwesend"} else {return "Fehler"}},\
Temperature_Profile_ModeTXT {if(ReadingsVal("$name","Temperature_Profile_Mode","") == 0) {return "Normal"} elsif (ReadingsVal("$name","Temperature_Profile_Mode","") == 1) {return "Cold"} elsif (ReadingsVal("$name","Temperature_Profile_Mode","") == 2) {return "Warm"} else {return "Fehler"}},\
STATUS {if (ReadingsAge($name,"Fan_Speed_Next_Change",0) > 1000) {return "offline"} else {return "online"}}


mein AT für die Sensorwerte:

defmod at_comfoconnect at +*00:01:00 {system("/opt/fhem/scripts/aiocomfo_sensors.py &");;;;}
