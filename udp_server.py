#!/usr/bin/env python
from __future__ import print_function # needs to be first statement in file
import logging
import socket
import json
import requests

apiLuftdaten = "http://api.luftdaten.info/v1/push-sensor-data/"
apiMadavi = "https://api-rrd.madavi.de/data.php"

log = logging.getLogger('udp_server')
listenHost = "127.0.0.1"                                      # Listen on this IP adress

def udp_server(host=listenHost, port=9012):                   # Listen on this UDP port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    log.info("Listening on udp %s:%s<br>" % (host, port))
    s.bind((host, port))
    while True:
        (data, addr) = s.recvfrom(128*1024)
        yield data, addr

FORMAT_CONS = "%(asctime)s %(name)-12s %(levelname)8s\t%(message)s"
logging.basicConfig(filename="logfile.log", level=logging.INFO, format=FORMAT_CONS)

# receive UDP data and source addr, port
for data, addr in udp_server():
    log.info("%r       %r<br>" % (addr, data))
    #udpdata = "ID:12847178,P1:66.04,P2:53.32,P4:42.27,T:22.30,H:34.70,P:1002.70"
    udpDataDict = dict(x.split(":") for x in data.split(","))

# prepare header for PM values
    headers = {
      "X-Pin": "1",
      "X-Sensor": "esp8266-" + str(udpDataDict["ID"]) 
    }
    postdata = {
      "software_version": "kcs-udp-gw",
      "sensordatavalues": [
         {"value_type": "P0", "value": str(udpDataDict["P0"])},   # PM 1
         {"value_type": "P1", "value": str(udpDataDict["P1"])},   # PM 10
         {"value_type": "P2", "value": str(udpDataDict["P2"])},   # PM 2.5
         {"value_type": "P4", "value": str(udpDataDict["P4"])}    # PM 4
      ]
    }
    r = requests.post(apiLuftdaten, headers=headers, json=postdata)
    rr = requests.post(apiMadavi, headers=headers, json=postdata)
    log.info("PM Lufi: %s, Madavi: %s <br>" % (r.status_code, rr.status_code))

# prepare headers for Temp, Humidity and Pressure values
    headers = {
      "X-Pin": "11",
      "X-Sensor": "esp8266-" + str(udpDataDict["ID"])
    }
    postdata = {
      "software_version": "kcs-udp-gw",
      "sensordatavalues": [
         {"value_type": "temperature", "value": str(udpDataDict["T"])},
         {"value_type": "humidity", "value": str(udpDataDict["H"])},
         {"value_type": "pressure", "value": str(float(udpDataDict["P"])*100)} # hPa to Pa
      ]
    }
    r = requests.post(apiLuftdaten, headers=headers, json=postdata)
    rr = requests.post(apiMadavi, headers=headers, json=postdata)
    log.info("Temp Lufi: %s, Madavi: %s <br>" % (r.status_code, rr.status_code))

