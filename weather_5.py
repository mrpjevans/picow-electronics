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

for led_number in range(1, 5):
        leds[led_number].off()
    
buzzer = Pin(16, Pin.OUT)

# This function is trigged when any button is pressed
def button_handler(pin):
    # This weird line determines which button was pressed
    # (Not as easy as you'd think!)
    bouncy_button_pressed = int(str(pin)[4:6])
    utime.sleep_ms(20) # This debounces the keypress
    if buttons[bouncy_button_pressed].value() is 1:
        
        button_pressed = bouncy_button_pressed - 17
        print("Button {button} pressed".format(button=button_pressed))
        if button_pressed is not 4:
            data = call_openweathermap_api("weather")

            if button_pressed is 1:
                temp = data['main']['temp']
                print("Temp: {temp}C".format(temp=temp))
                light_range(temp, [10, 20, 30, 40])
            
            elif button_pressed is 2:
                wind = data['wind']['speed']
                print("Wind: {wind}kph".format(wind=wind))
                light_range(wind, [0, 10, 20, 30])
            
            elif button_pressed is 3:
                if 'rain' in data:
                    rain = data['rain']['1h']
                else:
                    rain = 0
                print("Rain: {rain}mmph".format(rain=rain))
                light_range(rain, [10, 20, 30, 40])

        else:
            data = call_openweathermap_api("air_pollution")
            aqi = data['list'][0]['main']['aqi']
            print("Air Quality Index: {aqi}/5".format(aqi=aqi))
            light_range(aqi, [1, 2, 3, 4])

def connect_to_wifi():
    global ssid, password

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

    return wlan

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

# Start here!
buzz(5)
connect_to_wifi()
buzz(5)

# Add the handler code to the four buttons
buttons = {};
for gpio_number in range(18, 22):
    buttons[gpio_number] = Pin(gpio_number, Pin.IN, Pin.PULL_DOWN)
    buttons[gpio_number].irq(trigger=Pin.IRQ_RISING, handler=button_handler)


# Loop but let the system breath, 
while True:
    utime.sleep_ms(10)
