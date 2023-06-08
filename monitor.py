#!/usr/bin/env python3

import asyncio
from prologix_gpib_async import AsyncPrologixGpibEthernetController

IPaddr = '10.42.0.64'
GPIBaddr = 21

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
            gpib_device.write("CRDG? ")
            # Instruct the controller to read until the device sets <EOI>, then read until '\n'
            # from the prologix controller
            th_couple_T = gpib_device.read()
            print("Thermocouple Junction Temperature:", th_couple_T)
    except (ConnectionError, ConnectionRefusedError):
        print("Could not connect to remote target. Is the device connected?")


async def main():
    await init()

if __name__ == "__main__":
    asyncio.run(main())
