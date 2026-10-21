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

D_INTERVAL = 5.0 #used to check/debug print memory usage (every 5 seconds)
last_action_time = time.time() #memory usage time helper

# Initialize the pixel strip
pixels = neopixel.NeoPixel(board.GP18, 8, brightness=0.20, auto_write=False)
last_colour = None #saves last set colour so the program doesn't redundantly set it again if the colour doesn't change

def set_pixels(colour): # sets the colour of the LED
    global last_colour
    if colour != last_colour:
        pixels.fill(colour)
        pixels.show()
        last_colour = colour

print("Initializing...")

colour_dex = { #rgb tuples for preset colours
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

wheel = [ #preset strings that display in COLOUR labels
    'white',
    'red',
    'orange',
    'green',
    'blue',
    'yellow',
    'cyan',
    'purple',
    'magenta']

set_pixels((0,0,0)) 

led = digitalio.DigitalInOut(board.GP10) #analog LED & its properties to debug, turn on, turn off
led.direction = digitalio.Direction.OUTPUT

led.value = False

encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP16, divisor=2) #controls indexed values such as menu selection, numerical values or alphabetical values

last_position = 0 #rotary encoder last position to handle turning

button1 = digitalio.DigitalInOut(board.GP14) #main pushbutton that is usually used to go fowards one layer in the directory or activate certain settings
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button_back = digitalio.DigitalInOut(board.GP13) #goes back one layer in the directory
button_back.direction = digitalio.Direction.INPUT
button_back.pull = digitalio.Pull.UP

buttonC = digitalio.DigitalInOut(board.GP20) #confirm button, which turns the light on and off
buttonC.direction = digitalio.Direction.INPUT
buttonC.pull = digitalio.Pull.UP

last_click_state = True #check for buttons clicks feedback
last_back_state = True
last_C_state = True

jlabel = label.Label 
jload = adafruit_imageload.load

layer = 0 #governs layers of the menu directory
lSet = ["OFF", "DEBUG", "ON"] #states of the analog LED
debug = True #if true, will print out things in the serial monitor
dir = 0 #governs current selected menu label in layer 1
des = 0 #governs menu label selector in layer 2
custom_status = "OFF" #whether custom mode is on or off
briper = round((pixels.brightness * 100)) #controls brightness percentage of the RGB LED 
old_briper = briper #checks if the brightness percentage displayed within the BRIGHTNESS label is the same as the brightness percentage variable
pixelState = 0 #0= off, 1 = on (RGB)
main_menu_state = 0 #index value of the main menu label
mode_menu_state = 0 #index value of the mode menu label
redditing = False #whether or not the user is editing in the rhythm child menu
led_state = 0 #0 = off, 1 = on (analog)
colour_index = 0 #index of preset colour wheel
colourPreset = colour_dex[(wheel[0])] #tuple of RGB values picked from colour_dex type:DICT
#custom<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
font = terminalio.FONT
red_value, blue_value, green_value = 255, 0, 0 #default custom set colour (red)
cms = "main" #checks for custom menu state, including whether a submenu has been entered or 
AMP = 3 #the rate at which the rotary encoder increase/decreases RGB values in CUSTOM feature
custom_status = "OFF" #determines whether the main LED strip displays the custom set colour or a preset colour
custom_menu_labels = [
    label.Label(font, text="Status <OFF>", x=15, y=10),
    label.Label(font, text="RED   <255>", x=15, y=25),
    label.Label(font, text="GREEN <0>", x=15, y=40),
    label.Label(font, text="BLUE  <0>", x=15, y=55),
]
cursor = jlabel(font, text=">", x=0, y=10)
current_index = 0
#period<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
arra = ["<PS>", "<CT>"] #array for determining the order which the rhythm blinks. PS = preset, CT = custom
aradict = {"<PS>": colourPreset, "<CT>": (red_value, green_value, blue_value)}
arravalues = [None, None]

def update_arravalues(): #Period function - updates colour array values 
    arravalues[0] = aradict[arra[0]]
    arravalues[1] = aradict[arra[1]]

rhythdict = { #period function - the rhythm translator for setting up the rhythm
    "A":(1),
    "B":(1/2, 1/2),
    "C":(1/2, 1/4, 1/4),
    "D":(1/4, 1/4, 1/2),
    "E":(1/3, 1/3, 1/3),
    "F":(3/4, 1/4),
    "G":(1/4,1/4,1/4,1/4),
    "H":(-1/2, 1/2),
    "I":(1/2, -1/2),
    "J":(-1),
    "K":(-1/4, 1/4, 1/4, -1/4),
    "L":(-1/4, 1/4, 1/4, 1/4),
    "M":(1/4, 3/4),
    "N": None
}
period = 4.0 # determines the period which the rhythm repeats at
next_beat_time = time.monotonic() #
period_index = 0 #governs period menu selection
timsig = 0 #time signature for period function
current_colour = 0 #corresponds to last_colour to reduce unnecessary pixel updates
pms = "main"
beatlist = [] 

#lists for code letters in the rhythm child menu
k1 = ["N","A","B","C","D","E","F","G","H","I","J","K","L","M"]
k2 = ["N","A","B","C","D","E","F","G","H","I","J","K","L","M"]
k3 = ["N","A","B","C","D","E","F","G","H","I","J","K","L","M"]
k4 = ["N","A","B","C","D","E","F","G","H","I","J","K","L","M"]
k1v, k2v, k3v, k4v = 1,2,3,0
period_status = "SAVE/TURN ON"
period_menu_labels = [
    label.Label(font, text="FIR <PS>", x=15, y=10),
    label.Label(font, text=f"RHY [<{k1[k1v]}><{k2[k2v]}><{k3[k3v]}><{k4[k4v]}>]", x=15, y=25),
    label.Label(font, text=f"PRD <4.0s>", x=15, y=40),
    label.Label(font, text="STS [SAVE/TURN ON]", x=15, y=55),
]
pursor = jlabel(font, text = ">", x = 0 , y= 10) #period "cursor" arrow
purrent_pindex = 0 #controls the indexed menus within the period label
rhurrent_rhindex = 0 #controls the indexed rhythm menu label nestled within the period label
rhythmenu = [
    f" [{k1[k1v]}]<{k2[k2v]}><{k3[k3v]}><{k4[k4v]}> ",
    f" <{k1[k1v]}>[{k2[k2v]}]<{k3[k3v]}><{k4[k4v]}> ",
    f" <{k1[k1v]}><{k2[k2v]}>[{k3[k3v]}]<{k4[k4v]}> ",
    f" <{k1[k1v]}><{k2[k2v]}><{k3[k3v]}>[{k4[k4v]}] "
]
redditing_rhythmenu = [
    f"  {k1[k1v]} <{k2[k2v]}><{k3[k3v]}><{k4[k4v]}> ",
    f" <{k1[k1v]}> {k2[k2v]} <{k3[k3v]}><{k4[k4v]}> ",
    f" <{k1[k1v]}><{k2[k2v]}> {k3[k3v]} <{k4[k4v]}> ",
    f" <{k1[k1v]}><{k2[k2v]}><{k3[k3v]}> {k4[k4v]}  "
]
print(arravalues)

def switcheroo(): #reverses the first colour that displays during the period function
    global colourPreset, red_value, green_value, blue_value
    arra.reverse()
    period_menu_labels[0].text = f"FIR {arra[0]}"
    update_arravalues()

def enter_rhythm_editor(index): #changes the push button to operate within the rhythm directory
    strings = [
            f" [{k1[k1v]}]<{k2[k2v]}><{k3[k3v]}><{k4[k4v]}> ",
            f" <{k1[k1v]}>[{k2[k2v]}]<{k3[k3v]}><{k4[k4v]}> ",
            f" <{k1[k1v]}><{k2[k2v]}>[{k3[k3v]}]<{k4[k4v]}> ",
            f" <{k1[k1v]}><{k2[k2v]}><{k3[k3v]}>[{k4[k4v]}] "
        ]
    if index:
        period_menu_labels[1].text = "RHY " + strings[index]
    else:
        period_menu_labels[1].text = "RHY " + strings[0]

def update_period_status(): #update STS label
    period_menu_labels[3].text = f"STS <{period_status}>"

def periodcfg(): #updates PRD label within period function
    period_menu_labels[2].text = f"PRD  {period}s "


def process_rhythm(): #processes rhythm for the alternating LED colours
    global beatlist, timsig

    beatlist = []
    beatlist.clear()

    update_arravalues() #update arra for good measure

    keys = [k1[k1v], k2[k2v], k3[k3v], k4[k4v]]

    timsig = len([key for key in keys if key != "N"])

    if timsig == 0: #test for null time signature
        return

    for key in (k1[k1v], k2[k2v], k3[k3v], k4[k4v]): #build rhythm
        value = rhythdict[key]

        if value == None:
            continue
        if isinstance(value, tuple):
            beatlist.extend(value)
        else:
            beatlist.append(value)

def output_rhythm(): #handles the execution of LED blinking after processing all period-related variables
    global period_index
    global next_beat_time
    global pixelState
    global current_colour
    global timsig

    if period_status == "SAVE/TURN ON":
        return

    if timsig == 0:
        return

    update_arravalues()

    now = time.monotonic()

    if now < next_beat_time:
        return

    print(period_index)
    print(timsig)
    beat = beatlist[period_index]

    duration = abs(beat) * (period/timsig)

    if beat >= 0: #checks if there are beats left, if not, set LED to (0,0,0) (but not change its 'on' status)
        set_pixels(arravalues[current_colour])
        current_colour ^= 1
    else:
        set_pixels((0,0,0))

    next_beat_time = now + duration

    period_index += 1
    if period_index >= len(beatlist):
        period_index = 0

def start_period(): #prepare broadcasting-related variables before processing LED rhythm data
    global period_status
    global period_index
    global last_period_time
    global coefficient
    global current_colour
    global aradict

    process_rhythm()

    aradict = {"<PS>": colourPreset, "<CT>": (red_value, green_value, blue_value)}
    period_index = 0
    coefficient = 0
    current_colour = 0
    last_period_time = time.monotonic()

def extinguishers_period(really): #returns to the parent menu of the period feature
    global pms
    if pms != "main":
        if really == "RHY":
            period_menu_labels[1].text = f"RHY [<{k1[k1v]}><{k2[k2v]}><{k3[k3v]}><{k4[k4v]}>]"
        if really == "PRD":
            period_menu_labels[2].text = f"PRD <{period}s>"
        pms = "main"
        process_rhythm()

def screw(delta): #controls LED blink period from 0.5 to 10 seconds, wrapping from both ends when required
    global period, pms
    if pms == "PRD":
        period = (period - delta * 0.5) % 10.5

def flyer(eric): #handles primary direction in the rhythm menu, accepts integer
    strings = [
        f"  {k1[k1v]} <{k2[k2v]}><{k3[k3v]}><{k4[k4v]}> ",
        f" <{k1[k1v]}> {k2[k2v]} <{k3[k3v]}><{k4[k4v]}> ",
        f" <{k1[k1v]}><{k2[k2v]}> {k3[k3v]} <{k4[k4v]}> ",
        f" <{k1[k1v]}><{k2[k2v]}><{k3[k3v]}> {k4[k4v]} "
    ]
    period_menu_labels[1].text = "RHY " + strings[eric]
        
def steer(delta): #cycles between rhythm keys that dictate the final rhythm output
    global k1v, k2v, k3v, k4v, rhurrent_rhindex
    if redditing == True:
        if rhurrent_rhindex == 0:
            k1v = (k1v - delta) % 14
        if rhurrent_rhindex == 1:
            k2v = (k2v - delta) % 14
        if rhurrent_rhindex == 2:
            k3v = (k3v - delta) % 14
        if rhurrent_rhindex == 3:
            k4v = (k4v - delta) % 14
        

def lighters(really): #handles entering child menu RGB labels in CUSTOM settings
    global red_value, blue_value, green_value
    if really == "red":
        custom_menu_labels[1].text = f"RED    {red_value}"
    elif really == "green":
        custom_menu_labels[2].text = f"GREEN  {green_value}"
    elif really == "blue":
        custom_menu_labels[3].text = f"BLUE   {blue_value}"

def extinguishers(really): #handles returning to parent menu in CUSTOM settings
    global red_value, blue_value, green_value, cms
    if cms != "main":
        if really == "red":
            custom_menu_labels[1].text = f"RED   <{red_value}>"
        if really == "green":
            custom_menu_labels[2].text = f"GREEN <{green_value}>"
        if really == "blue":
            custom_menu_labels[3].text = f"BLUE  <{blue_value}>"
        cms = "main"

def nozzle(delta): #handles colour values for the custom RGB colour setter
    global red_value, blue_value, green_value
    if cms == "red":
        red_value = (red_value - delta * AMP)
        if red_value < 0:
            red_value = 255
        if red_value > 255:
            red_value = 0

    elif cms == "green":
        green_value = (green_value - delta * AMP)
        if green_value < 0:
            green_value = 255
        if green_value > 255:
            green_value = 0

    elif cms == "blue":
        blue_value = (blue_value - delta * AMP)
        if blue_value < 0:
            blue_value = 255
        if blue_value > 255:
            blue_value = 0

    if custom_status == "ON":
        update_custom_status()
        set_pixels((red_value,green_value,blue_value))
    print(encoder.position, delta)    
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

#imageload---------------------------------------------
imgms2 = "main_menu-s2.bmp" #load image labels
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

imgs3 = "main_menu-s3.bmp" #load image labels
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

imgs1 = "main_menu-s1.bmp" #load image labels
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

migs1 = "mode-menu_s1.bmp" #load image labels
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

migs2 = "mode-menu_s2.bmp" #load image labels
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

migs3 = "mode-menu_s3.bmp" #load image labels
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


text_area_brightness = jlabel( #loaded text labels
        font,
        text= f"BRIGHTNESS [{briper}%]",
        scale = 1,
        anchor_point=(0.5, 0.5),
        anchored_position=(display.width // 2, display.height // 2)
    )
text_area_mode_colour = jlabel( #loaded text labels
        font,
        text= f"<{wheel[0].upper()}>",
        scale = 1,
        anchor_point=(0.5, 0.5),
        anchored_position=(display.width // 2, display.height // 2)
    )
text_area_LED = jlabel( #loaded text labels
        font,
        text= f"TOGGLE <{lSet[0]}>",
        scale = 1,
        anchor_point=(0.5, 0.5),
        anchored_position=(display.width // 2, display.height // 2))
#display constant--------------------------------------
main_menu = [tile_main_s1, tile_main_s2, tile_main_s3]
mode_menu = [tile_mode_s1, tile_mode_s2, tile_mode_s3]


main_menu_group = displayio.Group() #initializing first labels when loaded
main_menu_group.append(tile_main_s1)

mode_menu_group = displayio.Group() #initializing first labels when loaded
mode_menu_group.append(tile_mode_s1)

brightness_group = displayio.Group() #initializing first labels when loaded
brightness_group.append(text_area_brightness)

led_group = displayio.Group() #....
led_group.append(text_area_LED)

colour_group = displayio.Group() #...
colour_group.append(text_area_mode_colour)

custom_group = displayio.Group() #...
for lbl in custom_menu_labels:
    custom_group.append(lbl)
custom_group.append(cursor)

period_group = displayio.Group() #...
for lbl in period_menu_labels:
    period_group.append(lbl)
period_group.append(pursor)

display.root_group = main_menu_group #load main menu
print("Loaded main menu")


def debug_print(): #blinks the analog LED
    led.value = True
    led.value = False

def pixel_switch(on): #turns on and off main LED, as well as checking if custom status is on to dictate whether to turn on custom or preset colour
    global pixelState, period_status
    if on:
        pixelState = 1
        if custom_status == "ON":
            set_pixels((red_value, green_value, blue_value))
        else:
            set_pixels(colourPreset)
        period_status = "SAVE/TURN ON"
        update_period_status()        
        #print("Pixels turned on")
    else:
        set_pixels((0,0,0))
        #print("Pixels turned off")
        period_status = "SAVE/TURN ON"
        update_period_status()
        pixelState = 0

def LED_toggle(lever): 
    global debug
    if debug == False:
        if lever == "off":
            led.value = False
        elif lever == "on":
            led.value = True

def frenzy(): #handles RGB LED updates after status or variable changes
    if pixelState != 1:
        set_pixels((0,0,0))
        return
    if period_status == "SAVE/TURN ON":
        if custom_status == "ON":
            set_pixels((red_value, green_value, blue_value))
        else:
            set_pixels(colourPreset)

def update_custom_status(): #only updates when there is a menu change or itself to reduce clutter
    custom_menu_labels[0].text = f"Status <{custom_status}>"

def update_briper(): #only updates when there is a menu change or itself to reduce clutter
    text_area_brightness.text = f"BRIGHTNESS [{briper}%]"




while True: #actual loop that the program runs on
###debug den#########################################################
    """
    current_time = time.time()
    if current_time - last_action_time >= D_INTERVAL:
        #gc.collect()
        print(gc.mem_free(), gc.mem_alloc(), len(main_menu_group))
        print(encoder.position)
        last_action_time = current_time

"""
    if period_status == "TURN OFF":
        output_rhythm()
#####################################################################
    current_position = encoder.position // 2

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
        if period_status != "SAVE/TURN ON":
            period_status = "SAVE/TURN ON"
        pixel_switch(not pixelState)
        if debug == True:
            debug_print() 
        print(layer, dir, des)

    if layer == 0: #main menu       
        #rotary switch---------------------------------------------
        if delta: #cycles selector
            main_menu_state += delta
            main_menu_state %= 3
            try:
                main_menu_group[0]=main_menu[main_menu_state]
            except ValueError as e:
                print("Display Error: " ,e)
            print(encoder.position)
            #print(f"Current main menu option selected [{main_menu_state + 1}]")
        #rotary switch---------------------------------------------

        if not current_click and last_click_state: #check for button state change
            if main_menu_state == 0: 
                display.root_group = brightness_group
                dir = 1
                print(f"Opened brightness menu")
            elif main_menu_state == 1: 
                display.root_group = mode_menu_group
                dir = 2
                print(f"Opened mode menu")
                last_position = encoder.position // 2
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

    if layer == 1: #mode menu, brightness, analog LED menu
        if dir == 1:
            if delta:
                briper -= delta * 2

                if briper < 0:
                    briper = 0
                elif briper > 100:
                    briper = 100
                #print(encoder.position)
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
                #print(encoder.position)
            
            if not current_click and last_click_state:
                if mode_menu_state == 0:
                    display.root_group= colour_group
                    des = 1
                    print(f"Directory layer changed to [{layer}]")
                    print(f"Opened colour submenu")
                elif mode_menu_state == 1: #CUSTOM MENU
                    display.root_group = custom_group
                    des = 2
                    update_custom_status()
                    last_position = encoder.position // 2
                    #print(f"Directory layer changed to [{layer}]")
                    #print(f"Opened custom submenu")
                elif mode_menu_state == 2:
                    display.root_group = period_group
                    update_period_status()
                    des = 3
                    last_position = encoder.position // 2
                layer = 2
                print(f"Layer = {layer}")
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
            last_position = encoder.position // 2
            if debug == True:
                debug_print()

    if layer == 2:
        if des == 1:
            if delta: #CUSTOM MENU
                colour_index = (colour_index + delta) % 9
                colourPreset = colour_dex[wheel[colour_index]]
                frenzy()
                text_area_mode_colour.text = f"<{wheel[colour_index].upper()}>"
                #print(f"Colour changed to [{text_area_mode_colour.text}, {colourPreset}]")
        if des == 2: 
            if delta:
                current_index += delta
                current_index %= 4

                cursor.y = 10 + current_index * 15
                #print(encoder.position)
        
            if not current_click and last_click_state:
                if cms == "main":
                    if current_index == 0:
                        if custom_status == "OFF":
                            custom_status = "ON"
                            #print("Turned on custom mode with {}")
                        elif custom_status == "ON":
                            custom_status = "OFF"
                            #print("Turned off custom mode.")
                        update_custom_status()
                        frenzy()
                    elif current_index == 1:
                        cms = "red"
                        layer = 3
                        print(f"Layer = {layer}")
                        #print(f"Directory layer changed to [{layer}]")
                        #print("red")
                        lighters(cms)
        
                    elif current_index == 2:
                        cms = "green"
                        layer = 3
                        #print(f"Directory layer changed to [{layer}]")
                        #print("green")
                        lighters(cms)

                    elif current_index == 3:
                        cms = "blue"
                        layer = 3
                        #print(f"Directory layer changed to [{layer}]")
                        #print("blue")
                        lighters(cms)
                    last_position = encoder.position // 2
                if debug == True:
                    debug_print()
  
        if des == 3: #period menu
            if delta: #selector
                purrent_pindex += delta
                purrent_pindex %= 4    
                pursor.y = 10 + purrent_pindex * 15
            if not current_click and last_click_state:
                if purrent_pindex == 0:
                    switcheroo()
                    period_status = "SAVE/TURN ON"
                    update_period_status()
                    frenzy()
                elif purrent_pindex == 1:
                    print("enter_rhythm_editor")
                    enter_rhythm_editor(0)
                    period_status = "SAVE/TURN ON"
                    update_period_status()
                    frenzy()
                    rhurrent_rhindex = 0
                    pms = "RHY"
                    layer = 3
                elif purrent_pindex == 2:
                    periodcfg()
                    period_status = "SAVE/TURN ON"
                    update_period_status()
                    pms = "PRD"
                    layer = 3
                elif purrent_pindex == 3:
                    if period_status == "SAVE/TURN ON":
                        process_rhythm()
                        if timsig != 0:
                            period_status = "TURN OFF"
                            start_period()
                    elif period_status == "TURN OFF":
                        period_status = "SAVE/TURN ON"
                        frenzy()
                    update_period_status()
                last_position = encoder.position // 2
                
        if not current_back and last_back_state: #move up a layer in the directory
            display.root_group = mode_menu_group
            layer = 1
            dir = 2

            #print(f"Directory layer retreated to [{layer}]")
            last_position = encoder.position // 2

            if debug == True:
                debug_print()

    if layer == 3:
        if des == 2:
            if delta:
                nozzle(delta)
                lighters(cms)
            #print(delta)
        
        if des == 3: #in period menu
            if pms == "RHY":
                if delta:
                    rhurrent_rhindex = (rhurrent_rhindex - delta) % 4
                    enter_rhythm_editor(rhurrent_rhindex)
                    #print(f"Mode menu option selected [{mode_menu_state + 1}]")

                if not current_click and last_click_state:
                    redditing = True
                    layer = 4
                    flyer(rhurrent_rhindex)
                
            elif pms == "PRD":
                    screw(delta)
                    periodcfg()


        if not current_back and last_back_state:
            if des == 2:
                extinguishers(cms)
            if des == 3:
                extinguishers_period(pms)
            layer = 2
            last_position = encoder.position // 2
            #print(f"Directory layer retreated to [{layer}]")
            if debug == True:
                debug_print()

    if layer == 4:
        if delta:
            print("hello?")
            steer(delta)
            flyer(rhurrent_rhindex)    
        if not current_back and last_back_state and redditing:
            layer = 3
            redditing = False
            enter_rhythm_editor(rhurrent_rhindex)
            rhythmenu = redditing_rhythmenu
            last_position = encoder.position // 2

    last_click_state = current_click
    last_back_state = current_back
    last_C_state = current_C

    last_position = current_position
    time.sleep(0.01)
