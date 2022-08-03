from machine import Pin
import utime
import network
import urequests

# Replace these with your own settings
ssid = "<Your Wifi Network Name>"
password = "<Your Wifi Password>"
lat = "52.1966242" # Treat as string
lon = "0.1285178" # Treat as string
api_key = "<OpenWeatherMap API Key>"

# Make sure these are the pins connected to your LEDs!
leds = {
    1: Pin(28, Pin.OUT),
    2: Pin(27, Pin.OUT),
    3: Pin(26, Pin.OUT),
    4: Pin(22, Pin.OUT),
}

buzzer = Pin(16, Pin.OUT)

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

# Make some noise
def buzz(ms):
    buzzer.on()
    utime.sleep_ms(ms)
    buzzer.off()

# Wrap up error check and response parsing into a single function
def call_openweathermap_api(endpoint):
    global lat, lon, api_key
    url = "https://api.openweathermap.org/data/2.5/{endpoint}?lat={lat}&lon={lon}&appid={appid}&units=metric".format(
        endpoint=endpoint,
        lat=lat,
        lon=lon,
        appid=api_key
    )

    # Make request and convert JSON response to Python dict
    print("Calling {endpoint} API".format(endpoint=endpoint))
    response = urequests.get(url)
    print("Status code: {status_code}".format(status_code=response.status_code))
    
    # Check the response status (200 = Success)
    if response.status_code is not 200:
        print('Error!')
        buzz(1000)
        raise SystemExit

    # Indicate we've got the data
    buzz(100)
    
    data = response.json()
    response.close()

    return data

# Get the latest weather
weather_data = call_openweathermap_api('weather')

# Get the air polution report
ap_data = call_openweathermap_api('air_pollution')

# Get the info we want
temp = weather_data['main']['temp']
wind = weather_data['wind']['speed']

# Rain info is not returned if there is none, so we provide a default value
if 'rain' in weather_data:
    rain = weather_data['rain']['1h']
else:
    rain = 0

aqi = ap_data['list'][0]['main']['aqi']

# Output our findings
print("Temp: {temp}C".format(temp=temp))
print("Wind: {wind}kph".format(wind=wind))
print("Rain: {rain}mmph".format(rain=rain))
print("Air Quality Index: {aqi}/5".format(aqi=aqi))

# Light up the LEDs in sequence
def light_range(value, bands):
    global leds
    led_to_light = 0

    # Every time we pass or equal a band, light an LED
    for band in bands:
        if value >= band:
            led_to_light += 1
            leds[led_to_light].on()

    utime.sleep(3)

    # Switch everything off again
    for led_number in range(1, 5):
        leds[led_number].off()
    utime.sleep(1)

light_range(temp, [10, 20, 30, 40])
light_range(wind, [0, 10, 20, 30])
light_range(rain, [10, 20, 30, 40])
light_range(aqi, [1, 2, 3, 4])

# Important to tidy up the connection
wlan.disconnect()