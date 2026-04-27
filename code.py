import random
import board
import rotaryio
import busio
import digitalio
import time 
import displayio
import terminalio
import i2cdisplaybus
from adafruit_displayio_ssd1306 import SSD1306
import adafruit_imageload
from adafruit_display_text import label
from adafruit_displayio_sh1106 import SH1106



encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP16, divisor=4)



last_position = 0

button1 = digitalio.DigitalInOut(board.GP14)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button_back = digitalio.DigitalInOut(board.GP18)
button_back.direction = digitalio.Direction.INPUT
button_back.pull = digitalio.Pull.UP

#display setup-----------------------------------------
displayio.release_displays()
i2c = busio.I2C(scl=board.GP27, sda=board.GP26)
big_bus = i2cdisplaybus.I2CDisplayBus(
    i2c, 
    device_address=0x3C
)
display = SH1106(
    big_bus, 
    width = 130, 
    height = 64
)
#display setup-----------------------------------------

#imageload--------------------------------------------- (dumbest way to do this but it works (adding seperate lines for each image), will improve on this later)
img = "apple2.bmp"
bitmap, palette = adafruit_imageload.load(
    img,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_grid = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)

img2 = "netflix.bmp"
bitmap, palette = adafruit_imageload.load(
    img2,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_grid2 = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)

img4 = "among.bmp"
bitmap, palette = adafruit_imageload.load(
    img4,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_among = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)

img3 = "srbrrrrr.bmp"
bitmap, palette = adafruit_imageload.load(
    img3,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_grid3 = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)
#imageload---------------------------------------------

#text label--------------------------------------------
text_area = label.Label(
    terminalio.FONT,
    text="1 week remaining",
    scale = 1,
    x=20,
    y=display.height//2
)
#text label--------------------------------------------

counter = 0

#display constant--------------------------------------
main_group = displayio.Group()
display.root_group = main_group
#display constant--------------------------------------

main_menu = [tile_grid, tile_grid3, tile_among]

main_group.append(main_menu[0])

held = False

while True:

#rotary switch---------------------------------------------
    current_position = encoder.position
    
    if current_position != last_position:
        main_group.pop()
        main_group.append(main_menu[current_position % 3])
        last_position = current_position
#rotary switch---------------------------------------------

#push button----------------------------------------------
    if button1.value == False: #press
        if held == False:
            main_group.pop()
            main_group.append(tile_grid2)
            held = True
    else: #release
        if held == True:
            main_group.pop()
            main_group.append(text_area)
            time.sleep(0.1)
            main_group.pop()
            main_group.append(main_menu[current_position % 3])
            held = False
            last_position = current_position
        elif current_position != last_position:
            main_group.pop()
            main_group.append(main_menu[current_position % 3])
            last_position = current_position
#push button----------------------------------------------


    time.sleep(0.001)

