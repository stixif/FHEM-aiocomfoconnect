# FHEM-aiocomfoconnect
aiocomfoconnect script für FHEM

### um AIOComfoconnect von michaelarnauts mit FHEM zu verwenden
https://github.com/michaelarnauts/aiocomfoconnect

## aiocomfo_sensors.py
is zum auslesen der Sensoren und schreiben als Reading ins FHEM Dummy
```
  --Fhost HOST           fhem server address. (localhost)
  --Fport PORT           fhem telnet port. (7072)
  --host IP              ip address of the comfocontrol bridge (auto)
  --uuid UUID            uuid of the comfocontrol bridge (auto)
  --fhemdummy            FHEMDUMMY name of the fhem dummy (comfoconnect)
```


## aiocomfo_set.py
hiermit kann die Lüftung über FHEM gesteuert werden
```
  --host IP            ip address of the comfocontrol bridge (auto)
  --uuid UUID        uuid of the comfocontrol bridge (auto)
 usw. siehe file
```

### Beispiel
```
python3 /opt/fhem/scripts/aiocomfo_set.py --boost 0 --boost_timeout 0 --mode auto --temperature_profile warm --bypass auto  <- Automatikbetrieb WARM
python3 /opt/fhem/scripts/aiocomfo_set.py --mode auto --boost 200 --boost_timeout 3600 <- PartyModus für 1std
```



### mein FHEM DUMMY:
```
defmod comfoconnect dummy
attr comfoconnect devStateIcon {".*:vent_ventilation_level_".ReadingsVal("$name","Fan_Speed",0).(ReadingsVal("$name","Operating_Mode",0) ne -1 ? '@green' : "")}
attr comfoconnect event-min-interval .*:800
attr comfoconnect event-on-change-reading .*:30
attr comfoconnect event-on-update-reading .*:300
attr comfoconnect userReadings Operating_ModeTXT {if(ReadingsVal("$name","Operating_Mode","") == -1) {return "Auto"} elsif (ReadingsVal("$name","Operating_Mode","") == 1) {return "Manuell Zeit"} elsif (ReadingsVal("$name","Operating_Mode","") == 5) {return "Manuell"} elsif (ReadingsVal("$name","Operating_Mode","") == 6) {return "Party Timer"}elsif (ReadingsVal("$name","Operating_Mode","") == 0) {return "Abwesend"} else {return "Fehler"}},\
Temperature_Profile_ModeTXT {if(ReadingsVal("$name","Temperature_Profile_Mode","") == 0) {return "Normal"} elsif (ReadingsVal("$name","Temperature_Profile_Mode","") == 1) {return "Cold"} elsif (ReadingsVal("$name","Temperature_Profile_Mode","") == 2) {return "Warm"} else {return "Fehler"}},\
STATUS {if (ReadingsAge($name,"Fan_Speed_Next_Change",0) > 1000) {return "offline"} else {return "online"}}
```

### mein AT für die Sensorwerte:
```
defmod at_comfoconnect at +*00:02:00 {system("/opt/fhem/scripts/aiocomfo_sensors.py &");;;;}
```
