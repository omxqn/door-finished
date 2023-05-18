import RPi.GPIO as GPIO
from gpiozero import AngularServo
import time

# GPIO pin numbers
LED_PIN = 25
LED_RED_PIN = 17
SERVO_PIN = 18
servo = AngularServo(SERVO_PIN, min_pulse_width=0.0006, max_pulse_width=0.0023)




def turn_on_red():
    # Set up GPIO mode and warnings
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set up LED pin as output
    GPIO.setup(LED_RED_PIN, GPIO.OUT)
    GPIO.output(LED_RED_PIN, GPIO.HIGH)
    print("LED_RED_PIN turned on")

def turn_off_red():
    # Set up GPIO mode and warnings
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(LED_RED_PIN, GPIO.OUT)
    GPIO.output(LED_RED_PIN, GPIO.LOW)
    print("LED_RED_PIN turned off")

def turn_on_led():
    # Set up LED pin as output
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED turned on")

def turn_off_led():
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED turned off")

def cleanup():
    GPIO.cleanup()  # Reset GPIO pins

def main_f(card):
    try:
        # Turn on LED for 3 seconds
        turn_on_led()
        time.sleep(1)
        if card == False:
            servo.angle = 90
            time.sleep(10)
            servo.angle = 0
        time.sleep(2)

        # Turn off LED
        turn_off_led()

    except KeyboardInterrupt:
        print("Script interrupted.")
    finally:
        cleanup()