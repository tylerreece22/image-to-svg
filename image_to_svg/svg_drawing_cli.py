import svgwrite
from PIL import Image
import sys

if len(sys.argv) != 3:
    print("Requires two arguments, source and destination file names")
    sys.exit(1)

source = sys.argv[1]
destination = sys.argv[2]

image = Image.open(source, "r")
width, height = image.size

pixel_values = list(image.getdata())

svg_drawing = svgwrite.Drawing(
    filename=destination, size=(width, height), profile="tiny"
)

for y in range(height):
    for x in range(width):
        pixel = pixel_values[x + y * width]

        if pixel[3] == 0:
            continue
        svg_drawing.add(
            svg_drawing.rect((x, y), (1, 1), fill="rgb(%d,%d,%d)" % pixel[:3])
        )

svg_drawing.save()
