import plasma
from plasma import plasma2040
import time
import random

NUM_LEDS = 50
BRIGHTNESS = 0.7

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)
led_array = []

led_strip.start()

def update_leds():
  for i in range(NUM_LEDS):
    led_strip.set_hsv(i,led_array[i]["hue"],led_array[i]["saturation"],led_array[i]["value"])

def init_rainbow():
  for i in range(NUM_LEDS):
    led_array.append({"hue": i / NUM_LEDS,
                      "saturation": 1.0,
                      "value": BRIGHTNESS})

def shuffle_array():
  for i in range(NUM_LEDS-1,0,-1):
         
    j = random.randint(0,i)
    
    # Highlight the elements being swapped
    led_array[i]["saturation"] = 0
    led_array[j]["saturation"] = 0  
    
    # Swap the elements
    led_array[i],led_array[j] = led_array[j],led_array[i]
    update_leds()
    time.sleep(0.1)
    
    # Remove the highlight
    led_array[i]["saturation"] = 1.0
    led_array[j]["saturation"] = 1.0
    update_leds()

def bubble_sort():
  for i in range(NUM_LEDS):

    already_sorted = True

    for j in range(NUM_LEDS - i - 1):

      # highlight the elements being compared
      led_array[j]["saturation"] = 0
      led_array[j + 1]["saturation"] = 0

      # See if elements are the right way around...
      if led_array[j]["hue"] > led_array[j + 1]["hue"]:
        # ... and swap them if they are not
        led_array[j], led_array[j + 1] = led_array[j + 1], led_array[j]
        already_sorted = False
      update_leds()
      time.sleep(0.05)

      # Remove highlight
      led_array[j]["saturation"] = 1.0
      led_array[j + 1]["saturation"] = 1.0
      update_leds()
    
    # Don't bother continuing if elements 0 to i are already sorted!
    if already_sorted:
      break

init_rainbow()
update_leds()

while True:
  shuffle_array()
  time.sleep(1)
  bubble_sort()
  time.sleep(10)