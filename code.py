import random
import board
import rotaryio
import busio
import digitalio
import time 
import displayio
import terminalio
import neopixel     
import i2cdisplaybus
from adafruit_displayio_ssd1306 import SSD1306
import adafruit_imageload
from adafruit_display_text import label
from adafruit_displayio_sh1106 import SH1106

# Initialize the pixel strip
pixels = neopixel.NeoPixel(board.GP18, 8, brightness=0, auto_write=False)

red = (255, 0, 0)
orange = (255, 64, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
purple = (128, 0, 255)
magenta = (255, 0, 255)

gay_list0 = [red, orange, yellow, green,cyan, blue, purple, magenta]
gay_list1 = [orange, yellow, green, cyan, blue, purple, magenta, red]
gay_list2 = [yellow, green, cyan, blue, purple, magenta, red, orange]
gay_list3 = [green, cyan, blue, purple, magenta, red, orange, yellow]
gay_list4 = [cyan, blue, purple, magenta, red, orange, yellow, green]
gay_list5 = [blue, purple, magenta, red, orange, yellow, green, cyan]
gay_list6 = [purple, magenta, red, orange, yellow, green, cyan, blue]
gay_list7 = [magenta, red, orange, yellow, green, cyan, blue, purple]

cycle = 0


led = digitalio.DigitalInOut(board.GP10)
led.direction = digitalio.Direction.OUTPUT

led.value = False

encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP16, divisor=4)

last_position = 0

button1 = digitalio.DigitalInOut(board.GP14)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button_back = digitalio.DigitalInOut(board.GP13)
button_back.direction = digitalio.Direction.INPUT
button_back.pull = digitalio.Pull.UP

buttonC = digitalio.DigitalInOut(board.GP20)
buttonC.direction = digitalio.Direction.INPUT
buttonC.pull = digitalio.Pull.UP

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


def gay_beam(cycle, selectron, layer):
    # rainbow animation
    pixels[0] = gay_list0[cycle]
    pixels[1] = gay_list1[cycle]
    pixels[2] = gay_list2[cycle]
    pixels[3] = gay_list3[cycle]
    pixels[4] = gay_list4[cycle]
    pixels[5] = gay_list5[cycle]
    pixels[6] = gay_list6[cycle]
    pixels[7] = gay_list7[cycle]

    # update animation cycle
    if cycle < 7:
        cycle += 1
    else:
        cycle = 0

    time.sleep(0.0011)
    pixels.show()

    # brightness / LED logic
    if selectron == 2 and layer == 1:
        led.value = True
        pixels.brightness = 0

    elif selectron == 3:
        if layer == 1:
            pixels.brightness = 1
            led.value = False
        else:
            pixels.brightness = 0.05
            led.value = False

    else:
        pixels.brightness = 0
        led.value = False

    return cycle

def gilded_beam():
    pixels.fill((255, 130, 0))
    pixels.brightness = 1
    pixels.show()
    time.sleep(0.01)
    pixels.fill((0, 0, 0))
    pixels.brightness = 0
    pixels.show()
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:
    current_click = button1.value
    current_back = button_back.value
    current_C = buttonC.value

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
        led.value = True
        time.sleep(0.005)
        led.value = False
        layer = 1

    if not current_back and last_back_state and layer == 1: #back
        main_group.pop()
        main_group.append(main_menu[current_position % 3])
        last_position = -1 #resets the position so that the display updates when the rotary switch is turned again after pressing the back button
        led.value = True
        time.sleep(0.005)
        led.value = False
        layer = 0
    
    if not current_C and last_C_state: #gilded beam
        led.value = True
        time.sleep(0.005)
        led.value = False
        gilded_beam()
    
    last_click_state = current_click
    last_back_state = current_back
    last_C_state = current_C

    cycle = gay_beam(cycle, selectron, layer)
    
#push button----------------------------------------------
