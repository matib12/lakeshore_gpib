# lakeshore_gpib
Cryogenic temperature continous monitoring using Lakeshore 331.

# Dependencies
    pip install prologix-gpib-async

# Init file for InfluxDB
A configuration file is necessary to connect to the InfluxDB database.
    [Influx]
    URL = http://SERVER_IP:8086  
    Token = YOUR_ACCESS_TOKEN  
    Org = YOUR_ORGANIZATION  
    Bucket = YOUR_BUCKET
  
    [Prologix]  
    IP = PROLOGIX_IP  
    Addr = PROLOGIX_GPIB_ADDR

