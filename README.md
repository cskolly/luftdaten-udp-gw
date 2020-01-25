# luftdaten-udp-gw
UDP gateway for NB sensors to upload their data to Luftdaten.info (Sensor.community)


Listen on UDP port 9012

UDP datagram should contain the sensor id and the measurment values comma separated:

ID: Sensor ID, <br>
P0: \<value\>,  # PM 1 <br>
P1: \<value\>,  # PM 10 <br>
P2: \<value\>,  # PM 2.5 <br>
P4: \<value\>,  # PM 4 <br>
T: \<value\>,   # Temperature <br>
H: \<value\>,   # Relative humidity <br>
P: \<value\>,   # Preessure <br>

Example:
"ID:12847178,P0:61.14,P1:66.04,P2:53.32,P4:42.27,T:22.30,H:34.70,P:1002.70"

