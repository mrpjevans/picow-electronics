from machine import Pin

leds = {
    1: Pin(28, Pin.OUT),
    2: Pin(27, Pin.OUT),
    3: Pin(26, Pin.OUT),
    4: Pin(22, Pin.OUT),
}

# This function is trigged when any button is pressed
def button_handler(pin):
    # This weird line determines which button was pressed
    # (Not as easy as you'd think!)
    button_pressed = int(str(pin)[4:6]) - 17
    print(str(button_pressed))
    leds[button_pressed].toggle()

# This is an efficient way of setting up all four buttons
# If we have a bug, we only have to fix it once!
for gpio_number in range(18, 22):
    # Assign a pin to be a button and use the pull-down resistor
    button = Pin(gpio_number, Pin.IN, Pin.PULL_DOWN)
    # Trigger the button_handler function when pressed
    button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
