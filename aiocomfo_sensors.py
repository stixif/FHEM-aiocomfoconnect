#!/usr/bin/python3
import asyncio
import argparse
import socket

from aiocomfoconnect import ComfoConnect, discover_bridges
from aiocomfoconnect.const import VentilationSpeed
from aiocomfoconnect.sensors import SENSORS

pin = 0
local_name = 'FHEM'
local_uuid = '00000000000000000000000000000010'

debug = False

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='fhem server address. (localhost)')
parser.add_argument('--port', help='fhem telnet port. (7072)')
parser.add_argument('--ip', help='ip address of the comfocontrol bridge (auto)')
parser.add_argument('--uuid', help='uuid of the comfocontrol bridge (auto)')
parser.add_argument('--fhemdummy', help='name of the fhem dummy (comfoconnect)')
args = parser.parse_args()

args.host = 'localhost' if args.host == None else args.host
args.port = 7072 if args.port == None else args.port
servhost = 'localhost'
args.fhemdummy = "comfoconnect" if args.fhemdummy == None else args.fhemdummy

bridge_ip = None if args.ip == None else args.ip
bridge_uuid = None if args.uuid == None else args.uuid
newreading = None
async def bridge_discovery():
    """ ComfoConnect LAN C Bridge discovery example."""
    
    # Discover all ComfoConnect LAN C Bridges on the subnet.
    bridges = await discover_bridges()
    if debug:
        print(bridges) #gibt die bridge aus z.B. [<Bridge 192.168.1.100, UID=00000000002a10128003388fd71e111c>]

    # Aufteilen des Ergebnisses in IP-Adresse und UID
    output = str(bridges[0])
    bridge_info = output.strip("[]")  # Entfernt eckige Klammern aus der Ausgabe
    bridge_ip, bridge_uuid = bridge_info.split(", UID=")  # Teilt die IP-Adresse und die UID auf
    bridge_uuid = bridge_uuid.rstrip(">")
    bridge_ip = bridge_ip.split(" ")[-1]  # Entfernt "Bridge" aus der IP-Adresse

    if debug:
        print(f"Bridge IP: {bridge_ip}")
        print(f"Bridge UID: {bridge_uuid}")
    
    return bridge_ip, bridge_uuid

async def main(local_uuid, bridge_ip, bridge_uuid):
    
    if bridge_uuid is None and bridge_ip is None:
        bridge_ip, bridge_uuid = await bridge_discovery()
        
    if debug:
        print(f"Bridge IP: {bridge_ip}")
        print(f"Bridge UID: {bridge_uuid}")

    ############# Create Outgoing FHEM connection ###################
    if debug:
        print(args.host)
        print(args.port)
    fhem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fhem.connect((args.host, args.port))
    
    def fhemsend(msg):
        ## fhem send here for comfoconnect requests
        msg+="\r\n"
        fhem.send(msg.encode('ascii'))
        #print(f"{msg}")
    
    def setreading(var, value, unit):
        var = var.replace(" ", "_")
        cmd = "setreading %s %s %s" % (args.fhemdummy, str(var), str(value))
        #print(f"{cmd} + {unit}")
        fhemsend(cmd)

        
    def sensor_callback(sensor, value):
        """ Print sensor updates. """
        unit = sensor.unit if hasattr(sensor, 'unit') else None
        setreading(sensor.name, value, sensor.unit)
        if debug:
            print(f"{sensor.name} = {value} = {sensor.unit}")

        
    # Connect to the Bridge
    comfoconnect = ComfoConnect(bridge_ip, bridge_uuid, sensor_callback=sensor_callback)
    await comfoconnect.connect(local_uuid)
    
    # Register all sensors
    for key in SENSORS:
        await comfoconnect.register_sensor(SENSORS[key])

    # Wait 2 minutes so we can see some sensor updates
    await asyncio.sleep(10)

    # Disconnect from the bridge
    fhem.close()
    await comfoconnect.disconnect()

    
if __name__ == "__main__":
        asyncio.run(main(local_uuid, bridge_ip, bridge_uuid))  # Replace with your bridge's IP and UUID
