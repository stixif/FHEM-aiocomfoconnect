#!/usr/bin/python3

import argparse
import asyncio
import socket
from aiocomfoconnect import ComfoConnect, discover_bridges
from aiocomfoconnect.sensors import SENSORS

# Lokale Konfigurationsparameter
local_uuid = '00000000000000000000000000000010'

# Kommandozeilenargumente
parser = argparse.ArgumentParser(description='aiocomfoconnect sende Sensorwerte an FHEM')
parser.add_argument('--Fhost', help='FHEM-Serveradresse (localhost)')
parser.add_argument('--Fport', help='FHEM-Telnet-Port (7072)')
parser.add_argument('--host', help='IP-Adresse der ComfoControl-Bridge')
parser.add_argument('--uuid', help='UUID der ComfoControl-Bridge (auto)')
parser.add_argument('--fhemdummy', help='Name des FHEM-Dummies (comfoconnect)')
args = parser.parse_args()

args.Fhost = 'localhost' if args.Fhost is None else args.Fhost
args.Fport = 7072 if args.Fport is None else int(args.Fport)
args.fhemdummy = 'comfoconnect' if args.fhemdummy is None else args.fhemdummy

async def discover_bridge():
    # Automatisch die Bridge entdecken und deren UUID und IP auslesen.
    bridges = await discover_bridges()
    if bridges:
        return bridges[0].uuid, bridges[0].host
    return None, None

def format_sensor_name(name):
    return name.replace(" ", "_")

def fhemsend(fhem, msg):
    msg += "\r\n"
    fhem.send(msg.encode('ascii'))

def setreading(fhem, var, value, unit):
    var = var.replace(" ", "_")
    cmd = f"setreading {args.fhemdummy} {var} {value}"
    fhemsend(fhem, cmd)

async def control_comfoconnect(params):
    host = params.get('host')
    uuid = params.get('uuid')

    if not host or not uuid:
        discovered_uuid, discovered_host = await discover_bridge()
        uuid = uuid or discovered_uuid
        host = host or discovered_host
        if not uuid or not host:
            print("Keine Bridge gefunden. Bitte geben Sie eine UUID und Host-IP an.")
            return

    fhem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fhem.connect((args.Fhost, args.Fport))

    def sensor_callback(sensor, value):
        # Callback-Funktion für Sensoraktualisierungen.
        sensor_name = format_sensor_name(sensor.name)
        sensor_unit = sensor.unit if hasattr(sensor, 'unit') else None
        #print(f"{sensor_name}: {value} {sensor_unit}")
        setreading(fhem, sensor_name, value, sensor_unit)

    conn = ComfoConnect(host, uuid, sensor_callback=sensor_callback)
    await conn.connect(local_uuid)

    # Registrieren aller Sensoren
    for key in SENSORS:
        await conn.register_sensor(SENSORS[key])

    # Kurze Zeit warten, damit Sensordaten empfangen werden können
    await asyncio.sleep(5)
    
    print(f"AIOcomfoconnect get FINISH")
    fhem.close()
    await conn.disconnect()

def main():
    print(f"AIOcomfoconnect get START")
    params = {
        'host': args.host,
        'uuid': args.uuid
    }
    asyncio.run(control_comfoconnect(params))

if __name__ == '__main__':
    main()
