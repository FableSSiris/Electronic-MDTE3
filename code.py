import random
import board
import rotaryio
import busio
import digitalio
import time 
import displayio
import terminalio
import neopixel 
import gc    
import i2cdisplaybus
from adafruit_displayio_ssd1306 import SSD1306
import adafruit_imageload
from adafruit_display_text import label
from adafruit_displayio_sh1106 import SH1106

INTERVAL = 5.0
last_action_time = time.time()

# Initialize the pixel strip
pixels = neopixel.NeoPixel(board.GP18, 8, brightness=0.20, auto_write=False)
last_colour = None

def set_pixels(colour):
    global last_colour

    if colour != last_colour:
        pixels.fill(colour)
        pixels.show()
        last_colour = colour

print("Initializing...")

colour_dex = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "orange": (255, 64, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "purple": (128, 0, 255),
    "magenta": (255, 0, 255)
    }

wheel = [
    'white',
    'red',
    'orange',
    'green',
    'blue',
    'yellow',
    'cyan',
    'purple',
    'magenta']

"""
gay_list0 = [wheel[1], wheel[2], wheel[3], wheel[4], wheel[5], wheel[6], wheel[7], wheel[8]]
gay_list1 = [wheel[2], wheel[3], wheel[4], wheel[5], wheel[6], wheel[7], wheel[8], wheel[1]]
gay_list2 = [wheel[3], wheel[4], wheel[5], wheel[6], wheel[7], wheel[8], wheel[1], wheel[2]]
gay_list3 = [wheel[4], wheel[5], wheel[6], wheel[7], wheel[8], wheel[1], wheel[2], wheel[3]]
gay_list4 = [wheel[5], wheel[6], wheel[7], wheel[8], wheel[1], wheel[2], wheel[3], wheel[4]]
gay_list5 = [wheel[6], wheel[7], wheel[8], wheel[1],wheel[2],wheel[3],wheel[4],wheel[5]]
gay_list6 = [wheel[7],wheel[8],wheel[1],wheel[2],wheel[3],wheel[4],wheel[5],wheel[6]]
gay_list7 = [wheel[8],wheel[1],wheel[2],wheel[3],wheel[4],wheel[5],wheel[6],wheel[7]]
"""
#cycle = 0

set_pixels((0,0,0))

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
last_C_state = True

jlabel = label.Label
jload = adafruit_imageload.load

#custom<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
font = terminalio.FONT
red_value = 0
blue_value = 0
green_value = 0
amp = 3
custom_status = "OFF"
cms = "main"
menu_labels = [
    label.Label(font, text="Status <OFF>", x=15, y=10),
    label.Label(font, text="RED   <0>", x=15, y=25),
    label.Label(font, text="GREEN <0>", x=15, y=40),
    label.Label(font, text="BLUE  <0>", x=15, y=55),
]
cursor = jlabel(font, text=">", x=0, y=10)
current_index = 0

def lighters(really):
    global red_value, blue_value, green_value, cms
    if really == "red":
        menu_labels[1].text = f"RED    {red_value}"
    elif really == "green":
        menu_labels[2].text = f"GREEN  {green_value}"
    elif really == "blue":
        menu_labels[3].text = f"BLUE   {blue_value}"

def extinguishers(really):
    global red_value, blue_value, green_value, cms, layer, last_position, current_position
    if cms != "main":
        if really == "red":
            menu_labels[1].text = f"RED   <{red_value}>"
        if really == "green":
            menu_labels[2].text = f"GREEN <{green_value}>"
        if really == "blue":
            menu_labels[3].text = f"BLUE  <{blue_value}>"
    cms = "main"
    layer = 2
    last_position = encoder.position
    print("main")

def nozzle(delta):
    global red_value, blue_value, green_value
    delta = current_position - last_position
    if cms == "red":
        red_value -= delta * amp
        red_value %= 258

    elif cms == "green":
        green_value -= delta * amp
        green_value %= 258

    elif cms == "blue":
        blue_value -= delta * amp
        blue_value %= 258

    if custom_status == "ON":
        update_custom_status()
        set_pixels((red_value,green_value,blue_value))      
#custom}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}

#display setup-----------------------------------------
displayio.release_displays()
i2c = busio.I2C(scl=board.GP27, sda=board.GP26, frequency=400000)
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
bitmap, palette = jload(
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
bitmap, palette = jload(
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
bitmap, palette = jload(
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
bitmap, palette = jload(
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
bitmap, palette = jload(
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
bitmap, palette = jload(
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
#lovibabeles---------------------------------------------
layer = 0
lSet = ["OFF", "DEBUG", "ON"]
debug = True
dir = 0
des = 0
custom_status = "OFF"
briper = round(int(pixels.brightness * 100))
old_briper = briper
pixelState = 0
main_menu_state = 0
mode_menu_state = 0
led_state = 0
colour_index = 0
colourState = colour_dex[(wheel[0])]

text_area_brightness = jlabel( #filler
        font,
        text= f"BRIGHTNESS [{briper}%]",
        scale = 1,
        anchor_point=(0.5, 0.5),
        anchored_position=(display.width // 2, display.height // 2)
    )
text_area_mode_colour = jlabel( #filler
        font,
        text= f"<{wheel[0].upper()}>",
        scale = 1,
        anchor_point=(0.5, 0.5),
        anchored_position=(display.width // 2, display.height // 2)
    )
text_area_LED = jlabel( #filler
        font,
        text= f"TOGGLE <{lSet[0]}>",
        scale = 1,
        anchor_point=(0.5, 0.5),
        anchored_position=(display.width // 2, display.height // 2)
    )
#display constant--------------------------------------
main_menu = [tile_main_s1, tile_main_s2, tile_main_s3]
mode_menu = [tile_mode_s1, tile_mode_s2, tile_mode_s3]


main_menu_group = displayio.Group()
main_menu_group.append(tile_main_s1)

mode_menu_group = displayio.Group()
mode_menu_group.append(tile_mode_s1)

brightness_group = displayio.Group()
brightness_group.append(text_area_brightness)

led_group = displayio.Group()
led_group.append(text_area_LED)

colour_group = displayio.Group()
colour_group.append(text_area_mode_colour)

custom_group = displayio.Group()
for lbl in menu_labels:
    custom_group.append(lbl)
custom_group.append(cursor)

display.root_group = main_menu_group
print("Loaded main menu")




"""
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
    pixels.fill(colour_dex.get(wheel[5]))
    pixels.brightness = 1
    pixels.show()
    time.sleep(0.01)
    pixels.fill((0, 0, 0))
    pixels.brightness = 0
    pixels.show()
"""


def debug_print():
    led.value = True
    led.value = False

def pixel_switch(on):
    global pixelState
    if on:
        pixelState = 1
        if custom_status == "ON":
            set_pixels((red_value, green_value, blue_value))
        else:
            set_pixels(colourState)        
        #print("Pixels turned on")
    else:
        set_pixels((0,0,0))
        #print("Pixels turned off")
        pixelState = 0

def LED_toggle(lever):
    global debug
    if debug == False:
        if lever == "off":
            led.value = False
        elif lever == "on":
            led.value = True

def frenzy():
    if pixelState != 1:
        return

    if custom_status == "ON":
        set_pixels((red_value, green_value, blue_value))
    else:
        set_pixels(colourState)

def update_custom_status():
    menu_labels[0].text = f"Status <{custom_status}>"

def update_briper():
    text_area_brightness.text = f"BRIGHTNESS [{briper}%]"


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------     
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



while True:
###debug den#########################################################
    current_time = time.time()
    if current_time - last_action_time >= INTERVAL:
        #gc.collect()
        print(gc.mem_free(), gc.mem_alloc(), len(main_menu_group))
        print(encoder.position)
        last_action_time = current_time
#####################################################################
    current_position = encoder.position

    delta = current_position - last_position

    

    if briper != old_briper:
        old_briper = briper
        update_briper()

    if led_state == 1:
        LED_toggle("off")
        debug = True
    
    elif led_state == 2:
        debug = False
        LED_toggle("on")
    elif led_state == 0:
        debug = False
        LED_toggle("off")

    current_click = button1.value
    current_back = button_back.value
    current_C = buttonC.value
    
    if not current_C and last_C_state: #give confirm button a purpose
        print("Confirm button pressed")
        pixel_switch(not pixelState)
        if debug == True:
            debug_print()

    if layer == 0:        
        #rotary switch---------------------------------------------
        if delta:
            main_menu_state += delta
            main_menu_state %= 3
            try:
                main_menu_group[0]=main_menu[main_menu_state]
            except ValueError as e:
                print("Display Error: " ,e)
            #print(f"Current main menu option selected [{main_menu_state + 1}]")
        #rotary switch---------------------------------------------

        if not current_click and last_click_state:
            if main_menu_state == 0: 
                display.root_group = brightness_group
                dir = 1
                print(f"Opened brightness menu")
            elif main_menu_state == 1: 
                display.root_group = mode_menu_group
                dir = 2
                print(f"Opened mode menu")
                last_position = encoder.position
                #print(f"Mode menu option selected [{mode_menu_state + 1}]")
            elif main_menu_state == 2: 
                display.root_group = led_group
                dir = 3
                print(f"Opened LED toggle menu")
            if debug == True:
                debug_print()
            last_click_state = current_click
            layer = 1
            print(f"Directory layer changed to [{layer}]")

    if layer == 1:
        if dir == 1:
            if delta:
                briper -= delta * 2

                if briper < 0:
                    briper = 0
                elif briper > 100:
                    briper = 100

                pixels.brightness = briper / 100
                if pixelState == 1:
                    pixels.show()
                #print(f"BRIGHTNESS changed to [{briper}%]")
      
        if dir == 2:
            if delta:
                mode_menu_state = (mode_menu_state + delta) % 3
                #print(f"Mode menu option selected [{mode_menu_state + 1}]")
                if mode_menu_group[0] is not mode_menu[mode_menu_state]:
                    mode_menu_group[0] = mode_menu[mode_menu_state]
            
            if not current_click and last_click_state:
                if mode_menu_state == 0:
                    display.root_group= colour_group
                    des = 1
                    layer = 2
                    print(f"Directory layer changed to [{layer}]")
                    print(f"Opened colour submenu")
                elif mode_menu_state == 1: #CUSTOM MENU
                    display.root_group = custom_group
                    des = 2
                    layer = 2
                    last_position = encoder.position
                    #print(f"Directory layer changed to [{layer}]")
                    #print(f"Opened custom submenu")
                elif mode_menu_state == 2:
                    print("PERIOD feature coming soon")
                last_click_state = current_click
                if debug == True:
                    debug_print()        
        if dir == 3:
            if delta:
                led_state = (led_state + delta) % 3
                text_area_LED.text = f"TOGGLE <{lSet[led_state]}>"
                #print(f"LED mode changed to [{lSet[led_state]}]")

        if not current_back and last_back_state:
            display.root_group = main_menu_group
            layer = 0
            dir = 0
            #print(f"Directory layer changed to [{layer}]")
            last_position = encoder.position
            if debug == True:
                debug_print()

    if layer == 2:
        if des == 1:
            if delta:
                colour_index = (colour_index + delta) % 9
                colourState = colour_dex[wheel[colour_index]]
                set_pixels(colourState)
                custom_status = "OFF"
                if pixelState == 1:
                    pixels.show()
                text_area_mode_colour.text = f"<{wheel[colour_index].upper()}>"
                #print(f"Colour changed to [{text_area_mode_colour.text}, {colourState}]")
                update_custom_status()
        if des == 2: 
            if delta:
                current_index += delta
                current_index %= 4

                cursor.y = 10 + current_index * 15
                    
        
            if not current_click and last_click_state:
                if cms == "main":
                    if current_index == 0:
                        if custom_status == "OFF" and pixelState == 1:
                            custom_status = "ON"
                            #print("Turned on custom mode with {}")
                        elif custom_status == "ON":
                            custom_status = "OFF"
                            #print("Turned off custom mode.")
                        else:
                            print("To access custom mode, main LED must be ON")
                        update_custom_status()
                        frenzy()
                    elif current_index == 1:
                        cms = "red"
                        layer = 3
                        #print(f"Directory layer changed to [{layer}]")
                        #print("red")
                        lighters(cms)
                        last_position = encoder.position
                    elif current_index == 2:
                        cms = "green"
                        layer = 3
                        #print(f"Directory layer changed to [{layer}]")
                        #print("green")
                        lighters(cms)
                        last_position = encoder.position
                    elif current_index == 3:
                        cms = "blue"
                        layer = 3
                        #print(f"Directory layer changed to [{layer}]")
                        #print("blue")
                        lighters(cms)
                        last_position = encoder.position
                if debug == True:
                    debug_print()
  
        if des == 3:
            """
            This is the period section, WIP.
            """
            pass
        

        if not current_back and last_back_state:
            display.root_group = mode_menu_group
            layer = 1
            dir = 2

            #print(f"Directory layer retreated to [{layer}]")
            last_position = encoder.position

            if debug == True:
                debug_print()

    if layer == 3:
        if delta:
            nozzle(delta)
            lighters(cms)

        if not current_back and last_back_state:
            if cms != "main":
                    extinguishers(cms)
            layer = 2
            last_position = encoder.position
            #print(f"Directory layer retreated to [{layer}]")
            if debug == True:
                debug_print()

    last_click_state = current_click
    last_back_state = current_back
    last_C_state = current_C

    last_position = current_position
    time.sleep(0.01)
    #Experimental functions (not part of real product)
    """
    #cycle = gay_beam(cycle, main_menu_state, layer)
    #gilded_beam()
    """

