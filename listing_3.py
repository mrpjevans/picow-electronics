# Based on code by Pete Gallagher
# https://www.petecodes.co.uk/
import time
import network
 
ssid = "<Your Wifi Network Name>"
password = "<Your Wifi Password>"
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
 
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('Network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'IP Address = ' + status[0] )

# Important to tidy up the connection
wlan.disconnect()