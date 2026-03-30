import board
import busio
import time
import displayio
import i2cdisplaybus
from adafruit_displayio_ssd1306 import SSD1306
import adafruit_imageload

displayio.release_displays()

i2c = busio.I2C(scl=board.GP27, sda=board.GP26)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = SSD1306(display_bus, width=128, height=64)

bitmap, palette = adafruit_imageload.load(
    "/OLED.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()
group.append(tile_grid)

display.root_group = group

while True:
    time.sleep(1)