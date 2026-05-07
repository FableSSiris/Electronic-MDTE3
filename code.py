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

button_back = digitalio.DigitalInOut(board.GP13)
button_back.direction = digitalio.Direction.INPUT
button_back.pull = digitalio.Pull.UP

last_click_state = True
last_back_state = True

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
imgms2 = "main_menu-s2.bmp"
bitmap, palette = adafruit_imageload.load(
    imgms2,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_main_s2 = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)

imgs3 = "main_menu-s3.bmp"
bitmap, palette = adafruit_imageload.load(
    imgs3,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_main_s3 = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)

imgs1 = "main_menu-s1.bmp"
bitmap, palette = adafruit_imageload.load(
    imgs1,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)

tile_main_s1 = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)
#imageload---------------------------------------------

#text label--------------------------------------------
weeks = 0

#text label--------------------------------------------

#display constant--------------------------------------
main_group = displayio.Group()
display.root_group = main_group
#display constant--------------------------------------

main_menu = [tile_main_s1, tile_main_s2, tile_main_s3]

main_group.append(main_menu[0])

layer = 0
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:
    
    current_click = button1.value
    current_back = button_back.value

    if layer == 0:
        current_position = encoder.position


    selectron = (current_position % 3) + 1
    

    text_area = label.Label(
        terminalio.FONT,
        text= f"{selectron} weeks remaining",
        scale = 1,
        x=20,
        y=display.height//2
    )
#control variables-_---------------------------------------------

#rotary switch---------------------------------------------

    if current_position != last_position:
            main_group.pop()
            main_group.append(main_menu[current_position % 3])
            last_position = current_position
            time.sleep(0.05)
#rotary switch---------------------------------------------
    
    
    
#push button----------------------------------------------

    if not current_click and last_click_state: #press
        main_group.pop()
        main_group.append(text_area)
        time.sleep(0.05)
        layer = 1

    if not current_back and last_back_state and layer == 1: #back
        main_group.pop()
        main_group.append(main_menu[current_position % 3])
        last_position = -1 #resets the position so that the display updates when the rotary switch is turned again after pressing the back button
        time.sleep(0.05)
        layer = 0
    
    last_click_state = current_click
    last_back_state = current_back



#push button----------------------------------------------


    

