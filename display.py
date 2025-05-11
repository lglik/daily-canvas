#!/usr/bin/env python3
"""
display.py  –  Push a bitmap/PNG/JPEG onto a Waveshare 5.65-inch 7-colour e-paper.
Usage:  python3 display.py path/to/picture.png
"""
import os, sys, time
from PIL import Image
import epaper

# Locate driver (only needed if you installed by git instead of PyPI)
# sys.path.append('/usr/local/lib/python3.*/dist-packages')

PALETTE = [
    (0,   0,   0  ),  # black
    (255, 255, 255),  # white
    (0,   255, 0  ),  # green
    (0,   0,   255),  # blue
    (255, 0,   0  ),  # red
    (255, 255, 0  ),  # yellow
    (255, 165, 0  )   # orange
]

def palette_image(img: Image.Image, epd):
    """Quantise any RGB image to the 7-colour palette expected by epd5in65f."""
    pal_img = Image.new("P", (16, 16))
    pal_img.putpalette([c for rgb in PALETTE for c in rgb] + [0]*(256*3 - 7*3))
    return img.convert("RGB").resize((epd.width, epd.height)).quantize(palette=pal_img)

def main(path):
    epd = epaper.epaper('epd5in65f').EPD()
    epd.init()           # power-on & LUT
    epd.Clear()          # white the canvas

    img = palette_image(Image.open(path), epd)
    epd.display(epd.getbuffer(img))  # bulk SPI transfer (~3.4 s)
    time.sleep(2)                    # give the e-ink capsules time to settle
    epd.sleep()                      # deep-sleep: <0.02 mA

if __name__ == "__main__":
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        sys.exit("Usage: python3 display.py ./picture.png")
    main(sys.argv[1])
