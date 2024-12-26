# xmasort
_Christmas. Sorted._

## Introduction

I have a few strings of ws2812 LEDs and some Pimoroni Plasma 2040 boards to run them as Christmas lights. In the past, I had just downloaded a ready-made library to make pretty patterns with them, but this year I wanted to challenge myself by programming the light sequences myself. I wasn't sure what patterns to try and make, until my son --- knowing that I am a bit of a geek --- jokingly asked "What's your favourite sorting algorithm?"

**The aim of this project is to visualise twelve different sorting algorithms --- one for each of the 12 days of Christmas --- using strings of RGB LEDs**!

## Hardware

The hardware consists of [Pimoroni Plasma 2040](https://shop.pimoroni.com/products/plasma-2040) boards connected to a variety of programmable RGB LED strings and powered using USB-C. I have three types of LED string:

- [10-metre LED star wire](https://shop.pimoroni.com/products/10m-addressable-rgb-led-star-wire) with 66 star-shaped leds
- [5-metre flexible LED wire](https://shop.pimoroni.com/products/5m-flexible-rgb-led-wire-50-rgb-leds-aka-neopixel-ws2812-sk6812) with 50 diffused LEDs
- A 1-metre strip of ws2812 60-LEDs/m, which I use for prototyping and testing

The Plasma 2040 boards are encased in [these 3D-printed enclosures](https://www.printables.com/model/261123-plasma-2040-case), which keeps them protected while potentially allowing the use of the additional buttons for control of the lights.

## Advent: Basic setup

The sort order is represented as integer Hue values on the colour wheel (0-360 degrees) in an array (actually a Python list) equal in size to the number of LEDs on the string. The colour of each LED is set by converting HSV colour values to RGB, using the Hue set in the corresponding array element, with Saturation = 1 and Value set to a default brightness. The "active" elements (the ones being swapped to randomise or sort the array) are shown in white (Saturation = 0). When the array is properly sorted, the LEDs should show a smooth rainbow of colours. 

The Plasma 2040s are all flashed with Pimoroni's [Pirate-brand MicroPython](https://github.com/pimoroni/pimoroni-pico/releases) version 1.23.0. [Microsoft Visual Studio Code](https://code.visualstudio.com/) is used to program them, with the help of the recently-released official [Raspberry Pi Pico Extension](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico). The `main.py` program installed on each Plasma 2040 will run automatically whenever it is powered on.

The basic `main.py` imports necessary libraries, sets up constants for things like the number of LEDs and default brightness, and has functions for initialising the array, randomising the array, and updating the LED colours from the array. It then enters an infinite loop, randomising and then sorting the array using the chosen algorithm.

## First Day: Bubble sort

**On the first day of Christmas** (Christmas Day), I thought I would start with something straightforward. Bubble sort is often used as the first example in a discussion of sorting algorithms because, while it is not particularly quick or efficient, it is easy to visualise how it works and is therefore simple to program.

The bubble sort algorithm simply iterates repeatedly through the unsorted array, comparing neighbouring elements and swapping them if they are in the wrong order. The first iteration works through the whole array and guarantees at the end that the last element must be in the right position, therefore the next iteration can skip the last element, and so on, skipping more and more elements at the end on each iteration, until the whole array is sorted. If the algorithm runs through a whole iteration without swapping any elements, then the complete array must be sorted and the routine can end prematurely.

The LED animation shows a "bubble" of active (white) elements repeatedly walking along a shorter and shorter section of the lights until it reaches the start and the colours are sorted. Colours that should appear near the beginning of the array appear to walk backwards along the LED string with each iteration.

## Second Day: Gnome sort (and some efficiency improvements)

**On the second day of Christmas** (Boxing Day), I chose the Christmassy-sounding [Gnome sort](https://en.wikipedia.org/wiki/Gnome_sort). Gnome sort is unusual in that the algorithm doesn't rely on a series of nested loops to traverse the array. Instead, It imagines a garden gnome rearranging a line of plant pots into size order according to a few simple movement rules. The gnome starts at the beginning (current position, _p_ = 0) and uses the rules to determine its current working position and how to arrange the pots at that position:

- If _p_ = 0, **move forwards** to _p_ + 1
- If the pot at _p_ is bigger than the pot at _p_ - 1, **move forwards** to _p_ + 1
- If the pot at _p_ < smaller than the pot at _p_ - 1, **swap** the pots at _p_ and _p_ - 1 and then **move backwards** to _p_ - 1
- If the pot at _p_ is bigger than the pot at _p_ - 1 and there are no pots at _p_ + 1 (i.e. the gnome is at the end of the array), **finish**

The LED animation shows a white dot (the gnome) running up and down the string of LEDs, gradually sorting them into the right order.

I also decided to make a few efficiency improvements to the main program. Firstly, there was no need to update the whole LED string when only a few elements had changed, so I added a couple of optional arguments to the update_leds routine to provide a list of which LEDs to update and to set whether or not they were "active" (white). Secondly, to save storage space, I no longer store the Saturation and Value of each LED in the array, since these don't change much and aren't used for sorting --- the array now simply contains the Hue values, which are rounded to the nearest integer to allow me to use some integer-only sorting methods in future.
