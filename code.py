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
pixels = neopixel.NeoPixel(board.GP18, 8, brightness=0.20, auto_write=False)

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
custom_menu_items = [f"Status <{custom_status}>",f"RED   <{red_value}>",f"GREEN <{green_value}>",f"BLUE  <{blue_value}>"]
menu_labels = []
cursor = jlabel(font, text=">", x=0, y=10)
current_index = 0

def lighters(really):
    global red_value, blue_value, green_value, cms
    if cms != "main":
        if really == "red":
            menu_labels[1].text = f"RED    {red_value}"
        elif really == "green":
            menu_labels[2].text = f"GREEN  {green_value}"
        elif really == "blue":
            menu_labels[3].text = f"BLUE   {blue_value}"
    else:
        pass

def extinguishers(really):
    global red_value, blue_value, green_value, cms, layer
    if cms != "main":
        if really == "red":
            menu_labels[1].text = f"RED   <{red_value}>"
        if really == "green":
            menu_labels[2].text = f"GREEN <{green_value}>"
        if really == "blue":
            menu_labels[3].text = f"BLUE  <{blue_value}>"
    cms = "main"
    layer = 2
    print("main")

def nozzle():
    global red_value, blue_value, green_value, cms, current_position, last_position
    if current_position < last_position:
                if cms == "red":
                    red_value += amp
                    if red_value > 255:
                        red_value = 0
                    if red_value < 0:
                        red_value = 255
                if cms == "green":
                    green_value += amp
                    if green_value > 255:
                        green_value = 0
                    if green_value < 0:
                        green_value = 255
                if cms == "blue":
                    blue_value += amp
                    if blue_value > 255:
                        blue_value = 0
                    if blue_value < 0:
                        blue_value = 255
    else:
                if cms == "red":
                    red_value -= amp
                    if red_value < 0:
                        red_value = 255
                    if red_value > 255:
                        red_value = 0
                if cms == "green":
                    green_value -= amp
                    if green_value < 0:
                        green_value = 255
                    if green_value > 255:
                        green_value = 0
                if cms == "blue":
                    blue_value -= amp
                    if blue_value < 0:
                        blue_value = 255
                    if blue_value > 255:
                        blue_value = 0
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

#display constant--------------------------------------
main_group = displayio.Group()
display.root_group = main_group
main_menu = [tile_main_s1, tile_main_s2, tile_main_s3]
mode_menu = [tile_mode_s1, tile_mode_s2, tile_mode_s3]
main_group.append(main_menu[0])
print("Loaded main menu")


#lovibabeles---------------------------------------------
layer = 0
lSet = ["OFF", "DEBUG", "ON"]
debug = True
dir = 0
des = 0
custom_status = "OFF"
briper = round(int(pixels.brightness * 100))
pixelState = 0
main_menu_state = 0
mode_menu_state = 0
led_state = 0
colourState = colour_dex.get(wheel[0])
pixels.fill(colourState)

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
    time.sleep(0.005)
    led.value = False

def pixel_switch(what):
    global pixelState, custom_status
    if what == "on":
        pixelState = 1

        if custom_status == "ON":
            pixels.fill((red_value, green_value, blue_value))
        else:
            pixels.fill(colourState)
        print("Pixels turned on")
        pixels.show()
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

def frenzy():
    if pixelState != 1:
        return

    if custom_status == "ON":
        pixels.fill((red_value, green_value, blue_value))
    else:
        pixels.fill(colourState)

    pixels.show()

def update_custom_status():
    custom_menu_items[0] = f"Status <{custom_status}>"

    if layer == 2 and des == 2 and len(menu_labels) >= 4:
        menu_labels[0].text = custom_menu_items[0]

text_area_brightness = jlabel( #filler
        font,
        text= f"BRIGHTNESS [{briper}%]",
        scale = 1,
        anchor_point=(0.5, 0.5),
        anchored_position=(display.width // 2, display.height // 2)
    )
text_area_mode = jlabel( #filler
        font,
        text= f"MODE SHOW",
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
text_area_mode_custom = jlabel( #filler
        font,
        text= f"CUSTOM",
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
    text_area_brightness.text = f"BRIGHTNESS [{briper}%]"

    if text_area_LED.text == f"TOGGLE <{lSet[1]}>":
        LED_toggle("off")
        debug = True
    
    elif text_area_LED.text == f"TOGGLE <{lSet[0]}>":
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
        print("Confirm button pressed")
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
            #print(f"Current main menu option selected [{main_menu_state + 1}]")
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
                #print(f"Mode menu option selected [{mode_menu_state + 1}]")
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
            last_click_state = current_click
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
                if pixelState == 1:
                    pixels.show()

                text_area_brightness.text = f"BRIGHTNESS [{briper}%]"
                #print(f"BRIGHTNESS changed to [{briper}%]")
                last_position = current_position
      
        if dir == 2:
            if current_position != last_position:
                mode_menu_state = current_position % 3
                #print(f"Mode menu option selected [{mode_menu_state + 1}]")
                main_group.pop()
                main_group.append(mode_menu[mode_menu_state])
                last_position = current_position
            
            if not current_click and last_click_state:
                if mode_menu_state == 0:
                    main_group.pop()
                    main_group.append(text_area_mode_colour)
                    des = 1
                    layer = 2
                    print(f"Directory layer changed to [{layer}]")
                    print(f"Opened colour submenu")
                if mode_menu_state == 1: #CUSTOM MENU
                    main_group.pop()
                    custom_menu_items = [
                        f"Status <{custom_status}>",
                            f"RED   <{red_value}>",
                    f"GREEN <{green_value}>",
                                f"BLUE  <{blue_value}>"
                                                    ]
                    for index, item_text in enumerate(custom_menu_items):
                        y_pos = 10 + (index * 15)
                        item_label = jlabel(font, text=item_text, x=15, y=y_pos)
                        menu_labels.append(item_label)
                        main_group.append(item_label)
                    main_group.append(cursor)
                    des = 2
                    layer = 2
                    print(f"Directory layer changed to [{layer}]")
                    print(f"Opened custom submenu")
                else:
                    pass
                last_click_state = current_click
                if debug == True:
                    debug_print()
                
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

    if layer == 2:
        if des == 1:
            if current_position != last_position:
                colourState = colour_dex.get(wheel[current_position % 9])
                pixels.fill(colourState)
                if pixelState == 1 and custom_status == "OFF":
                    pixels.show()
                else:
                    pass
                text_area_mode_colour.text = f"<{wheel[current_position % 9].upper()}>"
                #print(f"Colour changed to [{text_area_mode_colour.text}, {colourState}]")
                last_position = current_position
        
        if des == 2: 
            if current_position != last_position:
                if cms == "main" and layer == 2:
                    if current_position > last_position:
                        current_index += 1
                    else:
                        current_index -= 1
                    if current_index < 0:
                        current_index = 3
                    elif current_index > 3:
                        current_index = 0
                    cursor.y = 10 + (current_index * 15)
                    last_position = current_position
                    
        
            if not current_click and last_click_state:
                if cms == "main":
                    if current_index == 0:
                        if custom_status == "OFF" and pixelState == 1:
                            custom_status = "ON"
                            print("Turned on custom mode with {}")
                        elif custom_status == "ON":
                            custom_status = "OFF"
                            print("Turned off custom mode.")
                        else:
                            print("To access custom mode, main LED must be ON")
                        custom_menu_items[0] = f"Status <{custom_status}>"
                        main_group.remove(menu_labels[0])
                        item_label = label.Label(font, text=custom_menu_items[0], x=15, y=10)
                        menu_labels[0] = item_label
                        main_group.append(item_label)
                        frenzy()
                    elif current_index == 1:
                        cms = "red"
                        layer = 3
                        print(f"Directory layer changed to [{layer}]")
                        print("red")
                    elif current_index == 2:
                        cms = "green"
                        layer = 3
                        print(f"Directory layer changed to [{layer}]")
                        print("green")
    
                    elif current_index == 3:
                        cms = "blue"
                        layer = 3
                        print(f"Directory layer changed to [{layer}]")
                        print("blue")
                    lighters(cms)
                if debug == True:
                    debug_print()
  
        if des == 3:
            """
            This is the period section, WIP.
            """
            pass
        

        if not current_back and last_back_state:
            for lbl in menu_labels:
                main_group.remove(lbl)

            menu_labels.clear()

            try:
                main_group.remove(cursor)
            except ValueError:
                pass
            try:
                main_group.remove(text_area_mode_colour)
            except ValueError:
                pass
            main_group.append(mode_menu[mode_menu_state])
            layer = 1
            dir = 2
            encoder.position = mode_menu_state
            print(f"Directory layer retreated to [{layer}]")
            last_position = encoder.position

            if debug == True:
                debug_print()

    if layer == 3:
        if current_position != last_position:
            nozzle()
            lighters(cms)
            last_position = current_position

        if not current_back and last_back_state:
            if cms != "main":
                    extinguishers(cms)
            else:
                pass
            layer = 2
            print(f"Directory layer retreated to [{layer}]")
            if debug == True:
                debug_print()

    last_click_state = current_click
    last_back_state = current_back
    last_C_state = current_C

    #Experimental functions (not part of real product)
    """
    #cycle = gay_beam(cycle, main_menu_state, layer)
    #gilded_beam()
    """
    
