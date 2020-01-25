
Listen on UDP port 9012

UDP datagram should contain the sensor id and the measurment values comma separated:

ID: Sensor ID,
P0: <value>,  # PM 1
P1: <value>,  # PM 10
P2: <value>,  # PM 2.5
P4: <value>,  # PM 4
T: <value>,   # Temperature
H: <value>,   # Relative humidity
P: <value>,   # Preessure

Example:
"ID:12847178,P0:61.14,P1:66.04,P2:53.32,P4:42.27,T:22.30,H:34.70,P:1002.70"

