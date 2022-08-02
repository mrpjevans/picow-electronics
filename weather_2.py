import time
import network
import urequests

# Replace these with your own settings
ssid = '<Your Wifi Network Name>'
password = '<Your Wifi Password>'
lat = "52.1966242" # Treat as string
lon = "0.1285178" # Treat as string
api_key = "<OpenWeatherMap API Key>"
 
# Connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
 
# Wait for connect or fail
max_wait = 30
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('Network connection failed')

print('Connected')
status = wlan.ifconfig()
print( 'IP Address = ' + status[0] )

# Build request string
url = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=" + api_key + "&units=metric"

# Make request
response = urequests.get(url)
print(response.content)
response.close()

# Important to tidy up the connection
wlan.disconnect()