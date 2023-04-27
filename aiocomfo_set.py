#!/usr/bin/env python3

import asyncio
import argparse
import socket

from aiocomfoconnect import ComfoConnect, discover_bridges
from aiocomfoconnect.const import (
    VentilationBalance,
    VentilationMode,
    VentilationSetting,
    VentilationTemperatureProfile,
    VentilationSpeed,
)
from aiocomfoconnect.sensors import (
    SENSOR_BYPASS_ACTIVATION_STATE,
    SENSOR_OPERATING_MODE,
    SENSOR_PROFILE_TEMPERATURE,
    SENSORS,
    Sensor as AioComfoConnectSensor,
)


pin = 0
local_name = 'FHEM'
local_uuid = '00000000000000000000000000000010'

parser = argparse.ArgumentParser()
parser.add_argument('--ip', help='ip address of the comfocontrol bridge (auto)')
parser.add_argument('--uuid', help='uuid of the comfocontrol bridge (auto)')
parser.add_argument('--AIOType', help='Befehlstype')
parser.add_argument('--AIOComm', help='Befehlswert')
args = parser.parse_args()


AIOType = None if args.AIOType == None else args.AIOType
AIOComm = None if args.AIOComm == None else args.AIOComm
bridge_ip = None if args.ip == None else args.ip
bridge_uuid = None if args.uuid == None else args.uuid
newreading = None


async def bridge_discovery():
    """ ComfoConnect LAN C Bridge discovery example."""
    
    # Discover all ComfoConnect LAN C Bridges on the subnet.
    bridges = await discover_bridges()
    print(bridges) #gibt die bridge aus z.B. [<Bridge 192.168.1.100, UID=00000000002a10128003388fd71e111c>]

    # Aufteilen des Ergebnisses in IP-Adresse und UID
    output = str(bridges[0])
    bridge_info = output.strip("[]")  # Entfernt eckige Klammern aus der Ausgabe
    bridge_ip, bridge_uuid = bridge_info.split(", UID=")  # Teilt die IP-Adresse und die UID auf
    bridge_uuid = bridge_uuid.rstrip(">")
    bridge_ip = bridge_ip.split(" ")[-1]  # Entfernt "Bridge" aus der IP-Adresse
    
    return bridge_ip, bridge_uuid
    

async def main(local_uuid, bridge_ip, bridge_uuid, AIOType, AIOComm):
    """ Basic example."""
    print(f"Bridge IP: {bridge_ip} -#- Bridge UID: {bridge_uuid}")
    if bridge_uuid is None and bridge_ip is None:
        bridge_ip, bridge_uuid = await bridge_discovery()
    

    print(f"Bridge IP: {bridge_ip}")
    print(f"Bridge UID: {bridge_uuid}")

    comfoconnect = ComfoConnect(bridge_ip, bridge_uuid)
    await comfoconnect.connect(local_uuid)
    print(f"testen2")
# Select command type based on AIOType argument
    command = None
    if AIOType == 'Ventilation_Mode':
        command = comfoconnect.set_mode
    elif AIOType == 'Bypass_Mode':
        command = comfoconnect.set_bypass
    elif AIOType == 'Balance_Mode':
        command = comfoconnect.set_balance_mode
    elif AIOType == 'Temperature_Profile':
        command = comfoconnect.set_temperature_profile
    elif AIOType == 'SPEED':
        command = comfoconnect.set_speed
    elif AIOType == 'BOOST':
        command = comfoconnect.set_boost
    elif AIOType == 'AWAY_Mode':
        command = comfoconnect.set_away
    elif AIOType == None:
        command = None
    else:
        print(f"Invalid AIOType: {AIOType}")
        await comfoconnect.disconnect()
        return
        

    # Select command value based on AIOComm argument
    if AIOType == 'Ventilation_Mode':
        if AIOComm == 'AUTO':
            value = VentilationMode.AUTO
        elif AIOComm == 'MANUAL':
            value = VentilationMode.MANUAL
        else:
            print(f"Invalid AIOComm for {AIOType}: {AIOComm}")
            await comfoconnect.disconnect()
            return
        print(f"Valid AIOComm for {AIOType}: {AIOComm}")
    elif AIOType == 'Bypass_Mode':
        if AIOComm == 'AUTO':
            value = VentilationSetting.AUTO
        elif AIOComm == 'ON':
            value = VentilationSetting.ON
        elif AIOComm == 'OFF':
            value = VentilationSetting.OFF
        else:
            print(f"Invalid AIOComm for {AIOType}: {AIOComm}")
            await comfoconnect.disconnect()
            return
        print(f"Valid AIOComm for {AIOType}: {AIOComm}")
    elif AIOType == 'Balance_Mode':
        if AIOComm == 'BALANCE':
            value = VentilationBalance.BALANCE
        elif AIOComm == 'SUPPLY_ONLY':
            value = VentilationBalance.SUPPLY_ONLY
        elif AIOComm == 'EXHAUST_ONLY':
            value = VentilationBalance.EXHAUST_ONLY
        else:
            print(f"Invalid AIOComm for {AIOType}: {AIOComm}")
            await comfoconnect.disconnect()
            return
        print(f"Valid AIOComm for {AIOType}: {AIOComm}")
    elif AIOType == 'Temperature_Profile':
        if AIOComm == 'WARM':
            value = VentilationTemperatureProfile.WARM
        elif AIOComm == 'NORMAL':
            value = VentilationTemperatureProfile.NORMAL
        elif AIOComm == 'COOL':
            value = VentilationTemperatureProfile.COOL
        else:
            print(f"Invalid AIOComm for {AIOType}: {AIOComm}")
            await comfoconnect.disconnect()
            return
        print(f"Valid AIOComm for {AIOType}: {AIOComm}")
    elif AIOType == 'SPEED':
        if AIOComm == 'AWAY':
            value = VentilationSpeed.AWAY
        elif AIOComm == 'LOW':
            value = VentilationSpeed.LOW
        elif AIOComm == 'MEDIUM':
            value = VentilationSpeed.MEDIUM
        elif AIOComm == 'HIGH':
            value = VentilationSpeed.HIGH
        else:
            print(f"Invalid AIOComm for {AIOType}: {AIOComm}")
            await comfoconnect.disconnect()
            return
        print(f"Valid AIOComm for {AIOType}: {AIOComm}")
        
    elif AIOType == 'BOOST':
        if AIOComm == 'OFF':
            value = False
            value2 = 0
        elif AIOComm is not None and AIOComm != '' and AIOComm.isdigit():
            AIOComm = int(AIOComm)
            value = True
            value2 = AIOComm
        else:
            print(f"Invalid AIOComm for {AIOType}: {AIOComm}")
            await comfoconnect.disconnect()
            return
        print(f"Valid AIOComm for {AIOType}:")
        print(f"Valid value1 {value} and value2 {value2}")
        
    elif AIOType == 'AWAY_Mode':
        if AIOComm == 'OFF':
            value = False
            value2 = 0
        elif AIOComm is not None and AIOComm != '' and AIOComm.isdigit():
            AIOComm = int(AIOComm)
            value = True
            value2 = AIOComm
        else:
            print(f"Invalid AIOComm for {AIOType}: {AIOComm}")
            await comfoconnect.disconnect()
            return
        print(f"Valid AIOComm for {AIOType}:")
        print(f"Valid value1 {value} and value2 {value2}")

    elif AIOType == None:
        print(f"nothing")
        await comfoconnect.disconnect()
        return

    # Execute the selected command
    if AIOType == 'BOOST' or AIOType == 'AWAY_Mode':
        print(f"{command} and {value} and {value2}")
        await command(value, timeout=value2)
    else:
        print(f"{command} and {value}")
        await command(value)

    # Disconnect from the bridge
    await comfoconnect.disconnect()


if __name__ == "__main__":
    asyncio.run(main(local_uuid, bridge_ip, bridge_uuid, args.AIOType, args.AIOComm))
