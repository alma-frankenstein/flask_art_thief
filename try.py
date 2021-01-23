from io import BytesIO
import requests
from PIL import Image
# https://www.artsy.net/artwork/salvador-dali-madonne
# https://d32dm0rphc51dk.cloudfront.net/dAMtqpwtIUgN0zlJpjYrmA/dztiles/10/1_1.jpg
# TODO Automate the url grab
# TODO Automate the tile counts
# TODO Include Metadata (artist, title, etc)

# root_url = "https://d32dm0rphc51dk.cloudfront.net/dAMtqpwtIUgN0zlJpjYrmA/dztiles/12/{}_{}.jpg"   # Dali
root_url = "https://d32dm0rphc51dk.cloudfront.net/z6cZrfbgQXCnoZPztYQTsQ/dztiles/11/{}_{}.jpg"  # Mucha

# Mucha 3x3
# Dali 5x8 (final: Fetching image 4_7.jpg)
TILE_WIDTH_RANGE = 9
TILE_HEIGHT_RANGE = 9
TILE_SIZE = 512

# TODO It should be safe to assume the first tile is enough to determine the maximum TILE_SIZE.
#   If the image creation could be delayed until after the first tile is fetched we wouldn't need TILE_SIZE
new_image = Image.new('RGB', (TILE_SIZE * TILE_WIDTH_RANGE, TILE_SIZE * TILE_HEIGHT_RANGE))

# TODO A smarter algorithm for the actual_width/height would probably be:
#  Watch for smallest width
#  actual_width = (tile_count_width - 1) * TILE_SIZE + SMALLEST_WIDTH
actual_width = 0
actual_height = 0
height_counter = 0
width_counter = 0

# TODO Parallelize the tile fetch

for i in range(TILE_WIDTH_RANGE):
  for j in range(TILE_HEIGHT_RANGE):
    try:
      r = requests.get(root_url.format(i, j))
      im = Image.open(BytesIO(r.content))
      width, height = im.size
      actual_height += height
      actual_width += width
      new_image.paste(im, (TILE_SIZE * i, TILE_SIZE * j))
      print(f"Fetching image {i}_{j}.jpg")
      if r.ok and j == 0:
        height_counter += 1
      if r.ok and i == 0:
        width_counter += 1
    except OSError:
      pass

actual_width /= width_counter
actual_height /=  height_counter

print(f"Image size computed at: {actual_width}x{actual_height} (NOT {new_image.size})")
cropped_image = new_image.crop((0, 0, actual_width, actual_height))
cropped_image.show()

# TODO Turn the whole thing into a flask app and host it on GH?
