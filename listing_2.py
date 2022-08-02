# Remove the while True: block and replace with this
def button_handler(pin):
    button_pressed = int(str(pin)[4:6]) - 17
    print(str(button_pressed))
    leds[button_pressed].toggle()

for gpio_number in range(18, 22):
    button = Pin(gpio_number, Pin.IN, Pin.PULL_DOWN)
    button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
    