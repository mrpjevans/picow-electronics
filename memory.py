from machine import Pin
import urandom
import utime

# Play with these variables (ms) to change the speed of the game
speed = 1000 # How long the LEDs are lit
timeout = 5000  # How long you have to press a button

sequence = []       # Array to hold the sequence of lights
need_to_press = 0   # The next button you need to press in the sequence
button_pressed = 0  # What you actually pressed
restart = False     # Does the game need to end?

# Set up the LED pins
leds = {
    1: Pin(28, Pin.OUT),
    2: Pin(27, Pin.OUT),
    3: Pin(26, Pin.OUT),
    4: Pin(22, Pin.OUT),
}

buzzer = Pin(16, Pin.OUT)

# The button handler records the latest button pressed in a global variable
# The loop later on watches this variable for changes
def button_handler(pin):
    global button_pressed, buttons, leds
    bouncy_button_pressed = int(str(pin)[4:6])
    utime.sleep_ms(20) # This debounces the keypress
    if buttons[bouncy_button_pressed].value() is 1:
        button_pressed = bouncy_button_pressed - 17
        print(button_pressed)
        leds[button_pressed].on()
        utime.sleep_ms(200)
        leds[button_pressed].off()

# Add the handler code to the four buttons
buttons = {};
for gpio_number in range(18, 22):
    buttons[gpio_number] = Pin(gpio_number, Pin.IN, Pin.PULL_DOWN)
    buttons[gpio_number].irq(trigger=Pin.IRQ_RISING, handler=button_handler)


for led in leds:
    leds[led].off()

# Play FOREVER
while True:

    # New game? Let's make some noise.
    if len(sequence) is 0:
        restart = False

        # Ensure all the LEDs are off
        for led in leds:
            leds[led].off()
        
        # Sound gthe buzzer
        buzzer.on()
        utime.sleep_ms(500)
        buzzer.off()
        utime.sleep_ms(500)

    # Add a random number betwee 1-4 to the game
    next_led = urandom.randrange(1, 5)
    sequence.append(next_led)

    # For each part of the sequence
    for led_number in sequence:
        
        # Pulse the appropraite LED
        leds[led_number].on()
        utime.sleep_ms(speed)
        leds[led_number].off()

        # If the next LED is the same as the previous, this creates a
        # blink effect to make that clear
        utime.sleep_ms(100)

    # Now wait for the buttons in turn
    for led_number in sequence:

        # Reset everything
        button_pressed = 0
        need_to_press = led_number
        time_elapsed = 0

        # Await the button press within the timeou allowed
        while True:

            # A button has been pressed!
            if button_pressed is not 0:

                # If it's correct, jump out of the loop
                if button_pressed is need_to_press:
                    print('Correct!')
                    break
                else:
                    # Oh dear, it's wrong. Restart.
                    print('Oops!')
                    restart = True
                    break

            # Let the system breathe
            utime.sleep_ms(10)
            time_elapsed += 10

            # Check whether we've waited too long for an input
            if time_elapsed >= timeout:
                print('Took too long!')
                restart = True
                break

        # If the restart flag has been triggered, leave the loop
        if restart:
            break

    # If the restart flag has been triggered by a wrong press or
    # timeout, restart the game
    if restart:
        sequence = []
        print('Game Over')
        for led in leds:
            leds[led].on()
    
    utime.sleep_ms(1000)

