import plasma
from plasma import plasma2040
from machine import Pin
import time
import random

try:
  import config
except:
  print("No config file found! Using default values.")
  NUM_LEDS = 50
  BRIGHTNESS = 0.7
  STEP_DELAY = 0.05
else:
  NUM_LEDS = config.NUM_LEDS
  BRIGHTNESS = config.BRIGHTNESS
  STEP_DELAY = config.STEP_DELAY

delay = STEP_DELAY

def button_a_pressed(event):
  global delay
  delay = min(delay * 2, 1.0)
  print("Button A pressed. Delay is now: ", delay)

def button_b_pressed(event):
  global delay
  delay = max(delay / 2, 0.01)
  print("Button B pressed. Delay is now: ", delay)

button_a = Pin(plasma2040.BUTTON_A,Pin.IN,Pin.PULL_UP)
button_a.irq(handler=button_a_pressed, trigger=Pin.IRQ_FALLING)
button_b = Pin(plasma2040.BUTTON_B,Pin.IN,Pin.PULL_UP)
button_b.irq(handler=button_b_pressed, trigger=Pin.IRQ_FALLING)

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)
led_array = []

led_strip.start()

def update_leds(leds=range(NUM_LEDS),active=False,lit=True):
  for led in leds:
    h = led_array[led] / 360
    if active:
      s = 0
    else:
      s = 1.0
    if lit:
      v = BRIGHTNESS
    else:
      v = 0
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
    time.sleep(delay)
    
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
      time.sleep(delay)

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
    time.sleep(delay)

    if (i == 0) or (led_array[i] >= led_array[i-1]):
      # Nothing to do. Remove the highlight and move the gnome forwards
      update_leds([i], active = False)
      i += 1
    else:
      # Swap the current LED with the one before it, remove the highlight and move the gnome backwards
      led_array[i], led_array[i - 1] = led_array[i - 1], led_array[i]
      update_leds([i - 1, i], active = False)
      i -= 1

def insertion_sort():
  # iterate through the array, starting at position 1
  for i in range(1,len(led_array)):
    
    # save the source value
    h = led_array[i]

    j = i - 1
    # work backwards to find the correct position for the source value
    while j >= 0 and h < led_array[j]:
      # highlight the current source and search positions
      update_leds([i,j], active = True)
      # shift elements to the right
      led_array[j+1] = led_array[j]
      update_leds([j + 1])
      time.sleep(delay)
      # remove the highlights
      update_leds([i,j], active = False)
      j -= 1
    # set the correct position to the source value
    led_array[j+1] = h
    update_leds([j+1])

def bead_sort():
  # find the maximum value in the array
  max_val = led_array[0]
  for i in range(1,len(led_array)):
    if led_array[i] > max_val:
      max_val = led_array[i]

  # initialise the bead array
  bead_array = [[0 for i in range(max_val)] for j in range(len(led_array))]
  
  # fill in the bead array from the unsorted array
  for i in range(len(led_array)):
    for j in range(led_array[i]):
      bead_array[i][j] = 1
    # turn off the LEDs as their values are sucked into the bead array
    update_leds([i],lit=False)
    time.sleep(delay)
  
  # "drop" the beads
  for j in range(max_val):
    sum = 0
    for i in range(len(led_array)):
      sum += bead_array[i][j]
      bead_array[i][j] = 0
    for i in range(len(led_array)-1, len(led_array)-sum-1, -1):
      bead_array[i][j] = 1

  # sort the values back into the led_array
  for i in range(len(led_array)):
    sum = 0
    for j in range(max_val):
      sum += bead_array[i][j]
    led_array[i] = sum
    # Light up the LEDs again in the right order
    update_leds([i])
    time.sleep(delay)
  
init_rainbow()
update_leds()

while True:
  shuffle_array()
  time.sleep(1)
  bead_sort()
  # insertion_sort()
  # gnome_sort()
  # bubble_sort()
  time.sleep(10)