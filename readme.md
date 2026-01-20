

#### Features

* Use piper to convert text received via MQTT to speech.
* Use a button to cancel alarms.
* Use raspberry pi zero and python
* Speaker connected using i2s


#### Dependencies

Install using pip

 * piper-tts
 * paho-mqtt > 2

Also required :-

```shell
sudo apt install python3-pyaudio
```


#### Piper voices

Down load a voice for piper (this takes along time and there is no indication that it is progressing - so be patient)


```shell
python3 -m piper.download_voices en_GB-jenny_dioco-medium
```



[Neokey](https://learn.adafruit.com/neokey-breakout)



| **Connection**   | **Value** | **Pin** | **Pin** | **Value** | **Connection**   |
| ---------------- | --------: | ------- | ------- | --------- | ---------------- |
|                  |       3V3 | 1       | 2       | 5V        |                  |
|                  |     GPIO2 | 3       | 4       | 5V        |                  |
|                  |     GPIO3 | 5       | 6       | GND       |                  |
|                  |     GPIO4 | 7       | 8       | GPIO14    |                  |
|                  |       GND | 9       | 10      | GPIO15    |                  |
|                  |    GPIO17 | 11      | 12      | GPIO18    | I2S BLCK blue    |
|                  |    GPIO27 | 13      | 14      | GND       | NeoKey S- black  |
| NeoKey S+ yellow |    GPIO22 | 15      | 16      | GPIO23    |                  |
| Neokey 3v red    |       3V3 | 17      | 18      | GPIO24    |                  |
| NeoKey (I) blue  |    GPIO10 | 19      | 20      | GND       | NeoKey GND black |
|                  |     GPIO9 | 21      | 22      | GPIO25    |                  |
|                  |    GPIO11 | 23      | 24      | GPIO8     |                  |
|                  |       GND | 25      | 26      | GPIO7     |                  |
|                  |     GPIO0 | 27      | 28      | GPIO1     |                  |
|                  |     GPIO5 | 29      | 30      | GND       |                  |
|                  |     GPIO6 | 31      | 32      | GPIO12    |                  |
|                  |    GPIO13 | 33      | 34      | GND       |                  |
| I2S LRC  white   |    GPIO19 | 35      | 36      | GPIO16    |                  |
|                  |    GPIO26 | 37      | 38      | GPIO20    |                  |
| I2S GND          |       GND | 39      | 40      | GPIO21    | I2S DIN yellow   |


`NeoPixels must be connected to GPIO10, 

GPIO12, GPIO18 or GPIO21 to work! GPIO18 is the standard pin.`


```shell
pip install rpi_ws281x --break-system-packages
```

```shell
pip install adafruit-blinka --break-system-packages
```

```shell
pip install adafruit-circuitpython-neopixel --break-system-packages
```


```python
import RPi.GPIO as GPIO
import time
import threading

# Set up the GPIO pin for the button
BUTTON_PIN = 18  # Change this to the GPIO pin you are using
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Flag to control the loop
running = True

def button_callback(channel):
    global running
    running = False  # Set the flag to False when the button is pressed

# Set up an interrupt to detect button presses
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while running:
        # Perform your action here
        print("Action performed")
        
        # Wait for 20 seconds
        time.sleep(20)

except KeyboardInterrupt:
    print("Script interrupted by user")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
    print("Exiting script")
```


#### Non neopixel version

| **Connection** | **Value** | **Pin** | **Pin** | **Value** | **Connection**       |
| -------------- | --------: | ------- | ------- | --------- | -------------------- |
|                |       3V3 | 1       | 2       | 5V        |                      |
|                |     GPIO2 | 3       | 4       | 5V        |                      |
|                |     GPIO3 | 5       | 6       | GND       |                      |
|                |     GPIO4 | 7       | 8       | GPIO14    |                      |
|                |       GND | 9       | 10      | GPIO15    |                      |
|                |    GPIO17 | 11      | 12      | GPIO18    | I2S BLCK blue        |
| LED+           |    GPIO27 | 13      | 14      | GND       | Button/LED-  - black |
| Button yellow  |    GPIO22 | 15      | 16      | GPIO23    |                      |
|                |       3V3 | 17      | 18      | GPIO24    |                      |
|                |    GPIO10 | 19      | 20      | GND       |                      |
|                |     GPIO9 | 21      | 22      | GPIO25    |                      |
|                |    GPIO11 | 23      | 24      | GPIO8     |                      |
|                |       GND | 25      | 26      | GPIO7     |                      |
|                |     GPIO0 | 27      | 28      | GPIO1     |                      |
|                |     GPIO5 | 29      | 30      | GND       |                      |
|                |     GPIO6 | 31      | 32      | GPIO12    |                      |
|                |    GPIO13 | 33      | 34      | GND       |                      |
| I2S LRC  white |    GPIO19 | 35      | 36      | GPIO16    |                      |
|                |    GPIO26 | 37      | 38      | GPIO20    |                      |
| I2S GND        |       GND | 39      | 40      | GPIO21    | I2S DIN yellow       |

