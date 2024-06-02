#!/usr/bin/python3
import argparse
import asyncio
from aiocomfoconnect import ComfoConnect, discover_bridges

async def discover_bridge():
    # Automatisch die Bridge entdecken und deren UUID und IP auslesen.
    bridges = await discover_bridges()
    if bridges:
        return bridges[0].uuid, bridges[0].host
    return None, None

async def control_comfoconnect(params):
    uuid = params.get('uuid')
    host = params.get('host')

    if not uuid or not host:
        discovered_uuid, discovered_host = await discover_bridge()
        uuid = uuid or discovered_uuid
        host = host or discovered_host
        #print(uuid)
        print(host)
        if not uuid or not host:
            print("Keine Bridge gefunden. Bitte geben Sie eine UUID und Host-IP an.")
            return

    conn = ComfoConnect(host, uuid)
    local_uuid = '00000000000000000000000000000010'
    # Verbinden mit dem GerÃ¤t
    await conn.connect(local_uuid)

    # Setze die entsprechenden Werte basierend auf den übergebenen Argumenten
    if params.get('mode'):
        await conn.set_mode(params['mode'])
    if params.get('comfocool_mode'):
        await conn.set_comfocool_mode(params['comfocool_mode'])
    if params.get('speed'):
        await conn.set_speed(params['speed'])
    if params.get('bypass'):
        await conn.set_bypass(params['bypass'], params.get('bypass_timeout', -1))
    if params.get('balance_mode'):
        await conn.set_balance_mode(params['balance_mode'], params.get('balance_mode_timeout', -1))
    if params.get('boost') is not None:
        await conn.set_boost(params['boost'], params.get('boost_timeout', -1))
    if params.get('away') is not None:
        await conn.set_away(params['away'], params.get('away_timeout', -1))
    if params.get('temperature_profile'):
        await conn.set_temperature_profile(params['temperature_profile'])
    if params.get('ventmode_temperature_passive'):
        await conn.set_sensor_ventmode_temperature_passive(params['ventmode_temperature_passive'])
    if params.get('ventmode_humidity_comfort'):
        await conn.set_sensor_ventmode_humidity_comfort(params['ventmode_humidity_comfort'])
    if params.get('ventmode_humidity_protection'):
        await conn.set_sensor_ventmode_humidity_protection(params['ventmode_humidity_protection'])

    # Beispiel fÃ¼r Sensorregistrierung/Deregistrierung
    if params.get('register_sensor'):
        await conn.register_sensor(params['register_sensor'])
    if params.get('deregister_sensor'):
        await conn.deregister_sensor(params['deregister_sensor'])

    # Andere Methoden, die keinen Parameter erfordern, können auch hier aufgerufen werden.
    if params.get('get_mode'):
        mode = await conn.get_mode()
        print(f"Ventilation mode: {mode}")
    if params.get('get_comfocool_mode'):
        comfocool_mode = await conn.get_comfocool_mode()
        print(f"Comfocool mode: {comfocool_mode}")
    if params.get('get_speed'):
        speed = await conn.get_speed()
        print(f"Ventilation speed: {speed}")
    if params.get('get_bypass'):
        bypass = await conn.get_bypass()
        print(f"Bypass mode: {bypass}")
    if params.get('get_balance_mode'):
        balance_mode = await conn.get_balance_mode()
        print(f"Balance mode: {balance_mode}")
    if params.get('get_boost'):
        boost = await conn.get_boost()
        print(f"Boost mode: {boost}")
    if params.get('get_away'):
        away = await conn.get_away()
        print(f"Away mode: {away}")
    if params.get('get_temperature_profile'):
        temperature_profile = await conn.get_temperature_profile()
        print(f"Temperature profile: {temperature_profile}")
    if params.get('get_sensor_ventmode_temperature_passive'):
        ventmode_temperature_passive = await conn.get_sensor_ventmode_temperature_passive()
        print(f"Ventmode temperature passive: {ventmode_temperature_passive}")
    if params.get('get_sensor_ventmode_humidity_comfort'):
        ventmode_humidity_comfort = await conn.get_sensor_ventmode_humidity_comfort()
        print(f"Ventmode humidity comfort: {ventmode_humidity_comfort}")
    if params.get('get_sensor_ventmode_humidity_protection'):
        ventmode_humidity_protection = await conn.get_sensor_ventmode_humidity_protection()
        print(f"Ventmode humidity protection: {ventmode_humidity_protection}")

    # Trennen der Verbindung
    print(f"AIOcomfoconnect set FINISH")
    await conn.disconnect()

def main():
    print(f"AIOcomfoconnect set START")
    parser = argparse.ArgumentParser(description='Steuere aiocomfoconnect')
    parser.add_argument('--uuid', help='UUID des Geräts (wird automatisch erkannt, falls nicht angegeben)')
    parser.add_argument('--host', help='IP-Adresse des Geräts (wird automatisch erkannt, falls nicht angegeben)')
    parser.add_argument('--mode', choices=['auto', 'manual'], help='Lüftungsmodus')
    parser.add_argument('--comfocool_mode', choices=['auto', 'off'], help='Comfocool Modus')
    parser.add_argument('--speed', choices=['away', 'low', 'medium', 'high'], help='Lüftergeschwindigkeit')
    parser.add_argument('--bypass', choices=['auto', 'on', 'off'], help='Bypass Modus')
    parser.add_argument('--bypass_timeout', type=int, help='Timeout für Bypass Modus')
    parser.add_argument('--balance_mode', choices=['balance', 'supply only', 'exhaust only'], help='Balance Modus')
    parser.add_argument('--balance_mode_timeout', type=int, help='Timeout für Balance Modus')
    parser.add_argument('--boost', type=bool, help='Boost Modus')
    parser.add_argument('--boost_timeout', type=int, help='Timeout für Boost Modus')
    parser.add_argument('--away', type=bool, help='Away Modus')
    parser.add_argument('--away_timeout', type=int, help='Timeout für Away Modus')
    parser.add_argument('--temperature_profile', choices=['warm', 'normal', 'cool'], help='Temperaturprofil')
    parser.add_argument('--ventmode_temperature_passive', choices=['auto', 'on', 'off'], help='Passiver Temperaturkontrollmodus')
    parser.add_argument('--ventmode_humidity_comfort', choices=['auto', 'on', 'off'], help='Luftfeuchtigkeitskomfortmodus')
    parser.add_argument('--ventmode_humidity_protection', choices=['auto', 'on', 'off'], help='Luftfeuchtigkeitsschutzmodus')
    parser.add_argument('--register_sensor', type=int, help='Sensor registrieren')
    parser.add_argument('--deregister_sensor', type=int, help='Sensor deregistrieren')
    parser.add_argument('--get_mode', action='store_true', help='LÃ¼ftungsmodus abfragen')
    parser.add_argument('--get_comfocool_mode', action='store_true', help='Comfocool Modus abfragen')
    parser.add_argument('--get_speed', action='store_true', help='LÃ¼ftergeschwindigkeit abfragen')
    parser.add_argument('--get_bypass', action='store_true', help='Bypass Modus abfragen')
    parser.add_argument('--get_balance_mode', action='store_true', help='Balance Modus abfragen')
    parser.add_argument('--get_boost', action='store_true', help='Boost Modus abfragen')
    parser.add_argument('--get_away', action='store_true', help='Away Modus abfragen')
    parser.add_argument('--get_temperature_profile', action='store_true', help='Temperaturprofil abfragen')
    parser.add_argument('--get_sensor_ventmode_temperature_passive', action='store_true', help='Passiver Temperaturkontrollmodus abfragen')
    parser.add_argument('--get_sensor_ventmode_humidity_comfort', action='store_true', help='Luftfeuchtigkeitskomfortmodus abfragen')
    parser.add_argument('--get_sensor_ventmode_humidity_protection', action='store_true', help='Luftfeuchtigkeitsschutzmodus abfragen')

    args = parser.parse_args()

    # Argumente in ein Dictionary umwandeln
    params = vars(args)

    # Event Loop starten
    asyncio.run(control_comfoconnect(params))

if __name__ == '__main__':
    main()
