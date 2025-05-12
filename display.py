#!/usr/bin/env python3
"""
display.py – Fetch a PNG from the web and push it onto a Waveshare 5.65-inch
7-colour e-paper display.

Default source:
    https://lglik.github.io/83afab3c39/83afab3c39.png

Usage
-----
python3 display.py                  # uses the default URL above
python3 display.py https://...png   # display a different URL
"""
import sys, time, requests
from io import BytesIO
from PIL import Image
import epaper                       # pip install waveshare-epaper (or your fork)

# 7-colour palette for the epd5in65f panel
PALETTE = [
    (0,   0,   0  ),  # black
    (255, 255, 255),  # white
    (0,   255, 0  ),  # green
    (0,   0,   255),  # blue
    (255, 0,   0  ),  # red
    (255, 255, 0  ),  # yellow
    (255, 165, 0  )   # orange
]

DEFAULT_URL = "https://lglik.github.io/83afab3c39/83afab3c39.png"

def fetch_image(url: str) -> Image.Image:
    """Download *url* and return it as a PIL image."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return Image.open(BytesIO(r.content))

def palette_image(img: Image.Image, epd):
    """Quantise any RGB image to the 7-colour palette required by epd5in65f."""
    pal = Image.new("P", (16, 16))
    pal.putpalette([c for rgb in PALETTE for c in rgb] + [0]*(256*3 - 7*3))
    return img.convert("RGB").resize((epd.width, epd.height)).quantize(palette=pal)

def main(url: str):
    epd = epaper.epaper('epd5in65f').EPD()
    epd.init()            # power-on & load LUT
    epd.Clear()           # clear to white

    img = palette_image(fetch_image(url), epd)
    epd.display(epd.getbuffer(img))  # ~3.4 s SPI transfer
    time.sleep(2)                    # allow capsules to settle
    epd.sleep()                      # deep-sleep (<0.02 mA)

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    main(url)
