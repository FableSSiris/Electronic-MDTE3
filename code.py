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
pixels = neopixel.NeoPixel(board.GP18, 8, brightness=0.2, auto_write=False)

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

pixels.fill((0,0,0))
pixels.show()

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

migs1 = "mode-menu_s1.bmp"
bitmap, palette = adafruit_imageload.load(
    migs1,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_mode_s1 = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)

migs2 = "mode-menu_s2.bmp"
bitmap, palette = adafruit_imageload.load(
    migs2,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_mode_s2 = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)

migs3 = "mode-menu_s3.bmp"
bitmap, palette = adafruit_imageload.load(
    migs3,
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
tile_mode_s3 = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette, 
    x = (display.width - bitmap.width) // 2, 
    y=(display.height - bitmap.height) // 2
)
#imageload---------------------------------------------


#display constant--------------------------------------
main_group = displayio.Group()
display.root_group = main_group
main_menu = [tile_main_s1, tile_main_s2, tile_main_s3]
mode_menu = [tile_mode_s1, tile_mode_s2, tile_mode_s3]
main_group.append(main_menu[0])

#lovibabeles---------------------------------------------
layer = 0
lSet = ["DEBUG", "OFF", "ON"]
debug = True
dir = 0
briper = int(pixels.brightness * 100)
pixelState = 0
main_menu_state = 0
mode_menu_state = 0
led_state = 0
colourState = (255, 255, 255)

def gay_beam(cycle, main_menu_state, layer):
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
    if main_menu_state == 1 and layer == 1:
        led.value = True
        pixels.brightness = 0

    elif main_menu_state == 2:
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
    pixels.fill(yellow)
    pixels.brightness = 1
    pixels.show()
    time.sleep(0.01)
    pixels.fill((0, 0, 0))
    pixels.brightness = 0
    pixels.show()

def debug_print():
    led.value = True
    time.sleep(0.005)
    led.value = False

def pixel_switch(what):
    global pixelState
    if what == "on":
        pixels.fill(colourState)
        pixels.show()
        print(f"Pixels turned on with colour {colourState}")
        pixelState = 1
    elif what == "off":
        pixels.fill((0,0,0))
        pixels.show()
        print("Pixels turned off")
        pixelState = 0

def LED_toggle(lever):
    global debug
    if debug == False:
        if lever == "off":
            led.value = False
        elif lever == "on":
            led.value = True
text_area_brightness = label.Label( #filler
        terminalio.FONT,
        text= f"BRIGHTNESS [{briper}%]",
        scale = 1,
        x=20,
        y=display.height//2
    )
text_area_mode = label.Label( #filler
        terminalio.FONT,
        text= f"MODE SHOW",
        scale = 1,
        x=40,
        y=display.height//2
    )
text_area_LED = label.Label( #filler
        terminalio.FONT,
        text= f"TOGGLE <{lSet[0]}>",
        scale = 1,
        x=28,
        y=display.height//2
    )        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:
    text_area_brightness.text = f"BRIGHTNESS [{briper}%]"

    if text_area_LED.text == f"TOGGLE <{lSet[0]}>":
        LED_toggle("off")
        debug = True
    
    elif text_area_LED.text == f"TOGGLE <{lSet[1]}>":
        debug = False
        LED_toggle("off")
    elif text_area_LED.text == f"TOGGLE <{lSet[2]}>":
        debug = False
        LED_toggle("on")

    current_click = button1.value
    current_back = button_back.value
    current_C = buttonC.value

    current_position = encoder.position

    if not current_C and last_C_state: #give confirm button a purpose
            if pixelState == 0:
                pixel_switch("on")
            elif pixelState == 1:
                pixel_switch("off")
            if debug == True:
                    debug_print()

    if layer == 0:        
        
        #rotary switch---------------------------------------------
        if current_position != last_position:
            main_menu_state = current_position % 3
            main_group.pop()
            main_group.append(main_menu[main_menu_state])
            print(f"Current main menu option selected [{main_menu_state + 1}]")
            last_position = current_position
        #rotary switch---------------------------------------------

        if not current_click and last_click_state:
            if main_menu_state == 0: 
                main_group.pop()
                main_group.append(text_area_brightness)
                dir = 1
                print(f"Opened brightness menu")
                last_position = current_position
            if main_menu_state == 1: 
                main_group.pop()
                main_group.append(mode_menu[mode_menu_state])
                dir = 2
                encoder.position = mode_menu_state
                current_position = encoder.position
                print(f"Opened mode menu")
                print(f"Current mode menu option selected [{mode_menu_state + 1}]")
                last_position = current_position
                current_position = last_position
            if main_menu_state == 2: 
                main_group.pop()
                main_group.append(text_area_LED)
                dir = 3
                encoder.position = led_state
                current_position = encoder.position
                print(f"Opened LED toggle menu")
                last_position = current_position
            if debug == True:
                debug_print()
            layer = 1
            print(f"Directory layer changed to [{layer}]")

    if layer == 1:
        if dir == 1:
            if current_position != last_position:

                change = -(current_position - last_position)
                
                briper += 2*change

                if briper < 0:
                    briper = 0
                elif briper > 100:
                    briper = 100

                pixels.brightness = briper / 100
                pixels.show()

                text_area_brightness.text = f"BRIGHTNESS [{briper}%]"
                print(f"BRIGHTNESS changed to [{briper}%]")
                last_position = current_position
      
        if dir == 2:
            if current_position != last_position:
                mode_menu_state = current_position % 3
                print(f"Mode menu state changed to [{mode_menu_state}]")
                main_group.pop()
                main_group.append(mode_menu[mode_menu_state])
                last_position = current_position
        if dir == 3:
            if current_position != last_position:
                led_state = (current_position) % 3
                text_area_LED.text = f"TOGGLE <{lSet[led_state]}>"
                print(f"LED mode changed to [{lSet[led_state]}]")
                last_position = current_position

        if not current_back and last_back_state:
            main_group.pop()
            main_group.append(main_menu[main_menu_state])
            layer = 0
            dir = 0
            encoder.position = main_menu_state
            print(f"Directory layer changed to [{layer}]")
            last_position = encoder.position

            if debug == True:
                debug_print()
            

    last_click_state = current_click
    last_back_state = current_back
    last_C_state = current_C

    #Experimental functions
    #cycle = gay_beam(cycle, main_menu_state, layer)
    #gilded_beam()
#push button----------------------------------------------
