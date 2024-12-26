import plasma
from plasma import plasma2040
import time
import random

NUM_LEDS = 66
BRIGHTNESS = 0.7

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)
led_array = []

led_strip.start()

def update_leds(leds=range(NUM_LEDS),active=False):
  for led in leds:
    h = led_array[led] / 360
    if active:
      s = 0
    else:
      s = 1.0
    v = BRIGHTNESS
    led_strip.set_hsv(led,h,s,v)

def init_rainbow():
  for i in range(NUM_LEDS):
    led_array.append(round((i / NUM_LEDS) * 360))

def shuffle_array():
  for i in range(NUM_LEDS-1,0,-1):
         
    j = random.randint(0,i)
    
    # Highlight the elements being swapped
    update_leds([i, j], active = True)
    
    # Swap the elements
    led_array[i],led_array[j] = led_array[j],led_array[i]
    time.sleep(0.1)
    
    # Remove the highlight
    update_leds([i, j], active = False)

def bubble_sort():
  for i in range(len(led_array)):

    already_sorted = True

    for j in range(len(led_array) - i - 1):

      # highlight the elements being compared
      update_leds([j, j + 1], active = True)

      # See if elements are the right way around...
      if led_array[j] > led_array[j + 1]:
        # ... and swap them if they are not
        led_array[j], led_array[j + 1] = led_array[j + 1], led_array[j]
        already_sorted = False
      time.sleep(0.05)

      # Remove highlight
      update_leds([j, j + 1], active = False)
    
    # Don't bother continuing if elements 0 to i are already sorted!
    if already_sorted:
      break

def gnome_sort():
  # Set the gnome's starting position
  i = 0
  while i < len(led_array):
    # highlight the current position of the gnome
    update_leds([i], active = True)
    time.sleep(0.05)

    if (i == 0) or (led_array[i] >= led_array[i-1]):
      # Nothing to do. Remove the highlight and move the gnome forwards
      update_leds([i], active = False)
      i += 1
    else:
      # Swap the current LED with the one before it, remove the highlight and move the gnome backwards
      led_array[i], led_array[i - 1] = led_array[i - 1], led_array[i]
      update_leds([i - 1, i], active = False)
      i -= 1
  
init_rainbow()
update_leds()

while True:
  shuffle_array()
  time.sleep(1)
  gnome_sort()
  # bubble_sort()
  time.sleep(10)