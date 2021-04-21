from selenium import webdriver
from selenium.webdriver.support.color import Color
from selenium.webdriver import ActionChains
from math import cos, sin, pi
import mouse
import time

from PIL import Image
import os

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://paint-online.ru')


# Set right color
colorPicker = driver.find_element_by_class_name(
    "drawing-board-control-colors-current")
colorPicker.click()

# search for red square
squares = driver.find_elements_by_class_name(
    "drawing-board-control-colors-picker")
RED = Color.from_string('rgb(255, 0, 0)')
needed_square = None
for sq in squares:
    if Color.from_string(sq.value_of_css_property("background-color")) == RED:
        needed_square = sq
if needed_square:
    needed_square.click()


# Set pen size
slider = driver.find_element_by_xpath(
    "//input[@class='drawing-board-control-size-range-input']")
slider_length = slider.size['width']
move = ActionChains(driver)
move.move_to_element_with_offset(slider, 1, 0).click_and_hold(
).move_by_offset(slider_length/3, 0).release().perform()

# function for drawing spiral
def draw_spiral(a, step=0.1, loops=5):
    theta = 0.0
    r = 0
    prev_x = int(r*cos(theta))
    prev_y = int(r*sin(theta))
    while theta < 2 * loops * pi:
        theta += step
        r = a*theta
        x = int(r*cos(theta))
        y = int(r*sin(theta))
        mouse.move(x-prev_x, y-prev_y, absolute=False, duration=0.0001)
        prev_x = x
        prev_y = y


# Draw spiral
canvas = driver.find_element_by_class_name("drawing-board-canvas")
location = canvas.location
size = canvas.size

# Obtain absolute coordinates of the canvas center
browser_navigation_panel_height = driver.execute_script(
    'return window.outerHeight - window.innerHeight;')
x = location['x'] + size['width']/2
y = location['y'] + size['height']/2 + browser_navigation_panel_height

mouse.move(x, y)
mouse.press(button='left')
draw_spiral(5)
time.sleep(0.1) # Иначе не дорисовывает
mouse.release(button='left')

# Make screenshot
driver.save_screenshot('pageImage.png')

# Crop image
border = 5
x = location['x']
y = location['y']
width = location['x']+size['width']
height = location['y']+size['height']
im = Image.open('pageImage.png')
im = im.crop((int(x) + border, int(y) + border,
             int(width) - border, int(height) - border))
im.save('canvas.png')
os.remove("pageImage.png")

driver.quit()
