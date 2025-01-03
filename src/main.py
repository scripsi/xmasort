import plasma
from plasma import plasma2040
from machine import Pin
import time
import random
import math

try:
  import config
except:
  print("No config file found! Using default values.")
  NUM_LEDS = 50
  BRIGHTNESS = 0.7
  STEP_DELAY = 0.05
  LED_COLOR_ORDER = 2 # RGB:0; RBG:1; GRB:2; GBR:3; BRG:4; BGR:5
else:
  NUM_LEDS = config.NUM_LEDS
  BRIGHTNESS = config.BRIGHTNESS
  STEP_DELAY = config.STEP_DELAY
  LED_COLOR_ORDER = config.LED_COLOR_ORDER

delay = STEP_DELAY

day = 10

next_sort_method = day - 1

def button_a_pressed(event):
  global delay
  delay = min(delay * 2, 1.0)
  print("Button A pressed. Delay is now: ", delay)

def button_b_pressed(event):
  global delay
  delay = max(delay / 2, 0.01)
  print("Button B pressed. Delay is now: ", delay)

def button_user_pressed(event):
  global next_sort_method
  next_sort_method = (next_sort_method + 1) % day
  print("Button USER pressed. Next sort method is Day", next_sort_method + 1)

button_a = Pin(plasma2040.BUTTON_A,Pin.IN,Pin.PULL_UP)
button_a.irq(handler=button_a_pressed, trigger=Pin.IRQ_FALLING)
button_b = Pin(plasma2040.BUTTON_B,Pin.IN,Pin.PULL_UP)
button_b.irq(handler=button_b_pressed, trigger=Pin.IRQ_FALLING)
button_user = Pin(plasma2040.USER_SW,Pin.IN,Pin.PULL_UP)
button_user.irq(handler=button_user_pressed, trigger=Pin.IRQ_FALLING)

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT, color_order = LED_COLOR_ORDER)
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
  for i in range(len(led_array)-1,0,-1):
         
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

  # sort the values back into the LED array
  for i in range(len(led_array)):
    sum = 0
    for j in range(max_val):
      sum += bead_array[i][j]
    led_array[i] = sum
    # Light up the LEDs again in the right order
    update_leds([i])
    time.sleep(delay)

def pancake_sort():

  def biggest_pancake_in_stack(stack_bottom, stack_top: int) -> int:
    pancake = stack_bottom
    for i in range(stack_bottom,stack_top):
      if led_array[i] > led_array[pancake]:
        pancake = i
    return pancake

  def flip_stack(stack_bottom, stack_top: int):
    top_pancake = stack_top
    bottom_pancake = stack_bottom
    while bottom_pancake < top_pancake:
      led_array[bottom_pancake], led_array[top_pancake] = led_array[top_pancake], led_array[bottom_pancake]
      update_leds([bottom_pancake,top_pancake])
      time.sleep(delay)
      top_pancake -= 1
      bottom_pancake +=1
    
  pancake_stack = len(led_array)
  while pancake_stack > 1:
    biggest = biggest_pancake_in_stack(0,pancake_stack)
    if biggest != pancake_stack - 1:
      flip_stack(biggest,pancake_stack - 1)
    pancake_stack -= 1

def tree_sort():

  global led_array

  class TreeNode:
    def __init__(self, hue):
      self.left = None
      self.right = None
      self.hue = hue

  def insert(root, hue):
    if root is None:
        return TreeNode(hue)
    
    if hue < root.hue:
        root.left = insert(root.left, hue)
    else:
        root.right = insert(root.right, hue)
    
    return root

  def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        led_array.append(root.hue)
        update_leds(range(len(led_array)))
        time.sleep(delay)
        inorder_traversal(root.right)
  
  root = None
  for h in led_array:
    root = insert(root, h)

  led_array.clear()
  inorder_traversal(root)

def cocktail_sort():
  start_position = 0
  end_position = len(led_array) - 1
  while start_position < end_position:
    for i in range(start_position,end_position):
      # highlight the elements being compared
      update_leds([i + 1], active = True)

      # See if elements are the right way around...
      if led_array[i] > led_array[i + 1]:
        # ... and swap them if they are not
        led_array[i], led_array[i + 1] = led_array[i + 1], led_array[i]
        last_swap_position = i
      time.sleep(delay)
      # Remove highlight
      update_leds([i, i + 1], active = False)  

    end_position = last_swap_position
    
    for j in range(end_position,start_position - 1,-1):

      # highlight the elements being compared
      update_leds([j], active = True)

      # See if elements are the right way around...
      if led_array[j] > led_array[j + 1]:
        # ... and swap them if they are not
        led_array[j], led_array[j + 1] = led_array[j + 1], led_array[j]
        last_swap_position = j
      time.sleep(delay)
      # Remove highlight
      update_leds([j, j + 1], active = False)

    start_position = last_swap_position

def selection_sort():
  for i in range(len(led_array)-1):
    min = i
    for j in range(i+1,len(led_array)):
      update_leds([j], active = True)
      time.sleep(delay)
      if led_array[j] < led_array[min]:
        update_leds([min], lit = True)
        update_leds([j], active = False, lit = False)
        min = j
      else:
        update_leds([j], active = False)
    
    if min != i:
      led_array[i], led_array[min] = led_array[min], led_array[i]
      update_leds([i,min], active = False, lit = True)
      time.sleep(delay)

def bucket_sort():
  # set up some empty buckets
  bucket_number = 12
  buckets = []
  for bucket in range(bucket_number):
    buckets.append([])

  # Run through the unsorted array putting the values into the right buckets
  # Note: values in led_array are 0-360, so dividing by 30 gives 12 buckets!
  for i in range(len(led_array)):
    bucket = led_array[i] // 30
    buckets[bucket].append(led_array[i])
  
  # clear the array ...
  update_leds(lit = False)
  time.sleep(delay)
  led_array.clear()

  # ... and pour the buckets into it
  for bucket in range(bucket_number):
    led_array.extend(buckets[bucket])
    update_leds(range(len(led_array)), lit = True)
    time.sleep(delay*5)

  # Finally, run insertion sort
  insertion_sort()

def heap_sort():

  def left_child(root):
    l = (2 * root) + 1
    return l

  def right_child(root):
    r = (2 * root) + 2
    return r

  def parent(root):
    p = math.floor((root - 1) / 2)
    return p

  def sift_down(root, end):
    while left_child(root) < end:
      child = left_child(root)
      if (child + 1 < end) and (led_array[child] < led_array[child + 1]):
        child += 1
      
      if led_array[root] < led_array[child]:
        update_leds([root,child], active = True)
        time.sleep(delay)
        led_array[root], led_array[child] = led_array[child], led_array[root]
        update_leds([root,child])
        root = child
      else:
        return

  def heapify(count):
    start = parent(count - 1) + 1

    while start > 0:
      start -= 1
      sift_down(start,count)
    
  heapify(len(led_array))
  
  end = len(led_array)
  while end > 1:
    end -= 1
    update_leds([0, end], active = True)
    time.sleep(delay)
    led_array[0], led_array[end] = led_array[end], led_array[0]
    update_leds([0,end])
    sift_down(0, end)
  
  update_leds()

init_rainbow()
update_leds(range(len(led_array)))

sort_methods = [bubble_sort,
                gnome_sort,
                insertion_sort,
                bead_sort,
                pancake_sort,
                tree_sort,
                cocktail_sort,
                selection_sort,
                bucket_sort,
                heap_sort]

while True:
  print("Randomising LEDs")
  shuffle_array()
  time.sleep(1)
  print("Sorting LEDs with Day",next_sort_method + 1,"-",sort_methods[next_sort_method].__name__)
  sort_methods[next_sort_method]()
  time.sleep(10)