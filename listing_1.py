from machine import Pin
import utime

# Make sure these are the pins connected to your LEDs!
leds = {
    1: Pin(28, Pin.OUT),
    2: Pin(27, Pin.OUT),
    3: Pin(26, Pin.OUT),
    4: Pin(22, Pin.OUT),
}

# Loop through the LEDs toggling each one then sleeping a second
while True:
    for i, (k, led) in enumerate(leds.items()):
        led.toggle()
        utime.sleep_ms(1000)
