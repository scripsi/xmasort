# *** MODULE IMPORTS ***

import plasma
from plasma import plasma2040
from machine import Pin
import time
import random
import math

# *** GLOBAL VALUES ***

# If config.py exists, import starting values from there, otherwise use sensible defaults
try:
  import config

except:
  print("No config file found! Using default values.")
  NUM_LEDS = 50
  BRIGHTNESS = 0.7
  STEP_DELAY = 0.05
  LED_COLOR_ORDER = 2 # Possible values are: RGB = 0; RBG = 1; GRB = 2; GBR = 3; BRG = 4; BGR = 5

else:
  NUM_LEDS = config.NUM_LEDS
  BRIGHTNESS = config.BRIGHTNESS
  STEP_DELAY = config.STEP_DELAY
  LED_COLOR_ORDER = config.LED_COLOR_ORDER

delay = STEP_DELAY
day = 12
next_sort_method = day - 1

array = []

# *** HELPER FUNCTIONS ***

# *** BUTTON MANAGEMENT ***

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

button_a = Pin(plasma2040.BUTTON_A, Pin.IN, Pin.PULL_UP)
button_a.irq(handler = button_a_pressed, trigger = Pin.IRQ_FALLING)
button_b = Pin(plasma2040.BUTTON_B, Pin.IN, Pin.PULL_UP)
button_b.irq(handler = button_b_pressed, trigger = Pin.IRQ_FALLING)
button_user = Pin(plasma2040.USER_SW, Pin.IN, Pin.PULL_UP)
button_user.irq(handler = button_user_pressed, trigger = Pin.IRQ_FALLING)

# *** LED MANAGEMENT ***

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT, color_order = LED_COLOR_ORDER)
led_strip.start()

def wait(t = delay):
  time.sleep(t)

def update_leds(leds = range(NUM_LEDS), active = False, lit = True):
  
  for led in leds:
    h = array[led] / 360
    
    if active:
      s = 0
    else:
      s = 1.0
    
    if lit:
      v = BRIGHTNESS
    else:
      v = 0
    led_strip.set_hsv(led, h, s, v)

def highlight_leds(leds = []):
  
  if len(leds) > 0:
    update_leds(leds, active = True)
  
def swap_leds(i, j):
  highlight_leds([i, j])
  swap(i, j)
  wait()
  update_leds([i, j])

# *** ARRAY MANAGEMENT ***

def init_array():
  
  for i in range(NUM_LEDS):
    array.append(round((i / NUM_LEDS) * 360))

def swap(i, j):
  array[i], array[j] = array[j], array[i]

def shuffle_array():
  
  for i in range(len(array) - 1, 0, -1):
    j = random.randint(0, i)
    swap_leds(i, j)


# *** SORT FUNCTIONS ***

# First Day: Bubble sort
def bubble_sort():
  
  for i in range(len(array)):           # Main loop iterating through whole array
    already_sorted = True
    
    for j in range(len(array) - i - 1): # Iterate through the remaining unsorted elements, ...
      highlight_leds([j, j + 1])
      if array[j] > array[j + 1]:       # ... see if pairs of elements are the right way around ...
        swap(j, j + 1)                  # ... and swap them if they are not
        already_sorted = False
      wait()
      update_leds([j, j + 1])
    
    if already_sorted:                  # Don't bother continuing if elements 0 to i are already sorted!
      break


# Second Day: Gnome sort
def gnome_sort():
  
  i = 0                                         # Set the gnome's starting position
  while i < len(array):                         # Repeatedly apply movement rules until the gnome reaches the end of the sorted array         
    highlight_leds([i])
    wait()

    if (i == 0) or (array[i] >= array[i - 1]):  # Nothing to do. Just move the gnome forwards
      update_leds([i])
      i += 1
    else:                                       # Swap the current element with the one before it, and move the gnome backwards
      swap(i, i - 1)
      update_leds([i, i - 1])
      i -= 1


# Third Day: Insertion sort
def insertion_sort():
  
  for i in range(1, len(array)):       # Main loop iterating through the array, starting at position 1
    h = array[i]                       # Save the source value
    j = i - 1
    
    while j >= 0 and h < array[j]:     # Work backwards to find the correct position for the source value
      highlight_leds([i, j])
      array[j + 1] = array[j]          # Shift elements to the right
      wait()
      update_leds([i, j, j + 1])
      j -= 1
    
    array[j + 1] = h                   # Once the correct position has been found, set it to the source value
    update_leds([j + 1])


# Fourth Day: Bead sort
def bead_sort():
  
  max_val = array[0]
  for i in range(1, len(array)):       # Find the maximum value in the array
    if array[i] > max_val:
      max_val = array[i]

                                       # Initialise the bead array
  bead_array = [[0 for i in range(max_val)] for j in range(len(array))]
  
  for i in range(len(array)):          # Fill in the bead array from the unsorted array
    
    for j in range(array[i]):
      bead_array[i][j] = 1   
    update_leds([i], lit = False)      # Blank out the LEDs as they are put into the bead array
    wait()
  
  
  for j in range(max_val):             # "Drop" the beads
    sum = 0
    
    for i in range(len(array)):
      sum += bead_array[i][j]
      bead_array[i][j] = 0
    
    for i in range(len(array) - 1, len(array) - sum - 1, -1):
      bead_array[i][j] = 1
  
  for i in range(len(array)):         # Sort the values back into the array
    sum = 0
    
    for j in range(max_val):
      sum += bead_array[i][j]
    array[i] = sum
    update_leds([i])
    wait()


# Fifth Day: Pancake sort
def pancake_sort():

  # pancake_sort(): *** HELPER FUNCTIONS ***
  def biggest_pancake_in_stack(bottom, top: int) -> int:
    pancake = bottom
    
    for i in range(bottom, top):         # Iterate through the stack to find the biggest pancake
      if array[i] > array[pancake]:
        pancake = i
    
    return pancake

  def flip_stack(bottom, top: int):
    top_pancake = top
    bottom_pancake = bottom
    
    while bottom_pancake < top_pancake: # Reverse the stack, working from each end into the middle
      swap(bottom_pancake, top_pancake)
      update_leds([bottom_pancake, top_pancake])
      wait()
      top_pancake -= 1
      bottom_pancake +=1

  # pancake_sort(): *** MAIN ROUTINE ***  
  stack = len(array)
  
  while stack > 1:                      # Repeatedly flip the biggest pancake to the top until the array is sorted
    biggest = biggest_pancake_in_stack(0, stack)
    
    if biggest != stack - 1:
      flip_stack(biggest, stack - 1)
    stack -= 1


# Sixth Day: Tree sort
def tree_sort():

  global array

  class TreeNode:
    def __init__(self, hue):
      self.left = None
      self.right = None
      self.hue = hue

  # tree_sort(): *** HELPER FUNCTIONS ***
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
        array.append(root.hue)
        update_leds(range(len(array)))
        wait()
        inorder_traversal(root.right)
  
  # tree_sort(): *** MAIN ROUTINE ***
  root = None
  
  for h in array:
    root = insert(root, h)

  array.clear()
  inorder_traversal(root)


# Seventh Day: Cocktail sort
def cocktail_sort():
  start = 0
  end = len(array) - 1
  
  while start < end:
    
    for i in range(start,end):           # Iterate upwards from the start
      highlight_leds([i + 1])

      if array[i] > array[i + 1]:        # See if the elements are the right way around...   
        swap(i, i + 1)                   # ... and swap them if they are not
        last_swap_position = i
      wait()
      update_leds([i, i + 1])  

    end = last_swap_position
    
    for j in range(end, start - 1,-1):   # Iterate downwards from the end
      highlight_leds([j])

      if array[j] > array[j + 1]:        # See if elements are the right way around...        
        swap(j,j + 1)                    # ... and swap them if they are not
        last_swap_position = j
      wait()
      update_leds([j, j + 1])

    start = last_swap_position


# Eighth Day: Selection sort
def selection_sort():
  
  for i in range(len(array)-1):
    min = i
    
    for j in range(i+1,len(array)):
      highlight_leds([j])
      wait()
      
      if array[j] < array[min]:
        update_leds([min], lit = True)
        update_leds([j], active = False, lit = False)
        min = j
      else:
        update_leds([j])
    
    if min != i:
      swap(i, min)
      update_leds([i,min])
      wait()


# Ninth Day: Bucket sort
def bucket_sort():
  bucket_number = 12                  # Set up some empty buckets
  buckets = []
  
  for bucket in range(bucket_number):
    buckets.append([])

  for i in range(len(array)):         # Run through the unsorted array putting the values into the right buckets
    bucket = array[i] // 30           # values in the array are 0-360, so dividing by 30 gives 12 buckets!
    buckets[bucket].append(array[i])
  
  update_leds(lit = False)
  wait()
  array.clear()                       # Clear the array ...

  for bucket in range(bucket_number): # ... and pour the buckets into it
    array.extend(buckets[bucket])
    update_leds(range(len(array)), lit = True)
    wait(delay*5)                     # Make it easier to see the buckets being placed into array with a longer delay

  insertion_sort()                    # Finally, run insertion sort (Third Day) over the whole array


# Tenth Day: Heapsort
def heap_sort():

  # heap_sort(): *** HELPER FUNCTIONS ***
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
      if (child + 1 < end) and (array[child] < array[child + 1]):
        child += 1
      
      if array[root] < array[child]:
        update_leds([root, child], active = True)
        wait()
        array[root], array[child] = array[child], array[root]
        update_leds([root, child])
        root = child
      else:
        return

  def heapify(count):
    start = parent(count - 1) + 1

    while start > 0:
      start -= 1
      sift_down(start,count)
  
  # heap_sort(): *** MAIN ROUTINE ***
  heapify(len(array))
  
  end = len(array)
  while end > 1:
    end -= 1
    update_leds([0, end], active = True)
    wait()
    array[0], array[end] = array[end], array[0]
    update_leds([0,end])
    sift_down(0, end)
  
  update_leds()


# Eleventh Day: Quicksort
def quick_sort():

  # quick_sort(): *** HELPER FUNCTIONS ***
  def partition(start, end):
    middle = math.floor((start+end) / 2)
    if array[middle] < array[start]:
      update_leds([start, middle], active = True)
      wait()
      array[start], array[middle] = array[middle], array[start]
      update_leds([start,middle], active = False)
    if array[end] < array[start]:
      update_leds([start,end], active = True)
      wait()
      array[start], array[end] = array[end], array[start]
      update_leds([start,end], active = False)
    if array[middle] < array[end]:
      update_leds([middle,end], active = True)
      wait()
      array[middle], array[end] = array[end], array[middle]
      update_leds([middle,end], active = False)

    pivot = array[end]
    i = start
    j = end

    while True:
      while array[i] < pivot:
        i += 1

      while array[j] > pivot:
        j -= 1

      if i >= j:
        return j

      update_leds([i,j], active = True)
      wait()
      array[i], array[j] = array[j], array[i]
      update_leds([i,j], active = False)

  def qsort(start, end):
    if (start >= end) or (start < 0):
      return
    
    pivot = partition(start,end)
    qsort(start,pivot)
    qsort(pivot + 1, end)

  # quick_sort(): *** MAIN ROUTINE ***
  qsort(0, len(array) - 1)


# Twelfth Day: Bogosort
def bogo_sort():

  # bogo_sort(): *** HELPER FUNCTIONS ***
  def not_sorted_yet():
    
    for i in range(len(array)):
      
      if array[i] > array[i + 1]:
        return True

    return False

  # bogo_sort(): *** MAIN ROUTINE ***
  while not_sorted_yet():
    shuffle_array()


# *** MAIN ROUTINE ***    

sort_methods = [bubble_sort,
                gnome_sort,
                insertion_sort,
                bead_sort,
                pancake_sort,
                tree_sort,
                cocktail_sort,
                selection_sort,
                bucket_sort,
                heap_sort,
                quick_sort,
                bogo_sort]

init_array()
update_leds(range(len(array)))

while True:
  print("Randomising LEDs")
  shuffle_array()
  wait(1)
  print("Sorting LEDs with Day", next_sort_method + 1, "-", sort_methods[next_sort_method].__name__)
  sort_methods[next_sort_method]()
  wait(10)