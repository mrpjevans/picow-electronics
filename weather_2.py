import utime
import network
import urequests

# Replace these with your own settings
ssid = "<Your Wifi Network Name>"
password = "<Your Wifi Password>"
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
    utime.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('Network connection failed')

print('Connected')
status = wlan.ifconfig()
print( 'IP Address = ' + status[0] )

# Build request string
url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}&units=metric".format(
    lat=lat,
    lon=lon,
    appid=api_key
)

# Make request and convert JSON response to Python dict
response = urequests.get(url)
weather_data = response.json()
response.close()

# Get the info we want
temp = weather_data['main']['temp']
wind = weather_data['wind']['speed']

# Rain info is not returned if there is none, so we provide a default value
if 'rain' in weather_data:
    rain = weather_data['rain']['1h']
else:
    rain = 0

# Now request air pollution data
url = "https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={appid}&units=metric".format(
    lat=lat,
    lon=lon,
    appid=api_key
)

# Make request and convert JSON response to Python dict
ap_response = urequests.get(url)
ap_data = ap_response.json()
ap_response.close()

aqi = ap_data['list'][0]['main']['aqi']

# Output our findings
print("Temp: {temp}C".format(temp=temp))
print("Wind: {wind}kph".format(wind=wind))
print("Rain: {rain}mmph".format(rain=rain))
print("Air Quality Index: {aqi}/5".format(aqi=aqi))

# Important to tidy up the connection
wlan.disconnect()