#!/usr/bin/env python3

import time
import datetime
import asyncio
from prologix_gpib_async import AsyncPrologixGpibEthernetController

IPaddr = '192.168.11.13'
GPIBaddr = 12

async def init():
    try: 
        async with AsyncPrologixGpibEthernetController(IPaddr, pad=GPIBaddr) as gpib_device:
            version = await gpib_device.version()
            print("Controller version:", version)
            
            #gpib_device.write("INTYPE A,0,0")  # Select Silicon diode input
            #gpib_device.write("INTYPE B,0,0")  # Select Silicon diode input
            
            #gpib_device.write("INCRV A,21")  # DT-670 curve. Check number
            #gpib_device.write("INCRV B,21")  # DT-670 curve. Check number
            
    except (ConnectionError, ConnectionRefusedError):
        print("Could not connect to remote target. Is the device connected?")

async def read_room_temp():
    try: 
        async with AsyncPrologixGpibEthernetController(IPaddr, pad=GPIBaddr) as gpib_device:
            gpib_device.write("TEMP?")
            # Instruct the controller to read until the device sets <EOI>, then read until '\n'
            # from the prologix controller
            th_couple_T = gpib_device.read()
            print("Thermocouple Junction Temperature:", th_couple_T)
    except (ConnectionError, ConnectionRefusedError):
        print("Could not connect to remote target. Is the device connected?")

async def read_temp(chan):
    if chan not in ['A', 'B']:
        print("Wrong channel")
        return
    
    try: 
        async with AsyncPrologixGpibEthernetController(IPaddr, pad=GPIBaddr) as gpib_device:
            await gpib_device.write(("CRDG? " + chan).encode(encoding='UTF-8'))
            # Instruct the controller to read until the device sets <EOI>, then read until '\n'
            # from the prologix controller
            T = await gpib_device.read()
            return T
    except (ConnectionError, ConnectionRefusedError):
        print("Could not connect to remote target. Is the device connected?")


async def main():
    avg_n = 2
    
    T_A = 0.
    T_B = 0.

    for i in range(avg_n):
        T_A += float(await read_temp('A'))
        T_B += float(await read_temp('B'))
        time.sleep(3)

    T_A /= avg_n
    T_B /= avg_n

    n = datetime.datetime.now(datetime.timezone.utc)

    current_time = n.isoformat()

    print(current_time + "\t{:.2f}\t{:.2f}".format(T_A, T_B))


if __name__ == "__main__":
    asyncio.run(main())

