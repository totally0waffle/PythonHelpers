from PIL import Image
import numpy as np
from collections import defaultdict

province_file = "provinces.bmp"
heightmap_file = "heightmap.bmp"
output_file = "generated_heightmap.bmp"

print("Loading images...")

prov_img = Image.open(province_file).convert("RGB")
height_img = Image.open(heightmap_file).convert("L")

if prov_img.size != height_img.size:
    raise ValueError("Province map and heightmap must be the same resolution!")

prov_pixels = np.array(prov_img)
height_pixels = np.array(height_img)

height, width, _ = prov_pixels.shape

print(f"Resolution: {width}x{height}")

province_heights = defaultdict(list)

print("Scanning pixels...")

for y in range(height):
    for x in range(width):

        color = tuple(prov_pixels[y, x])

        if color == (0, 0, 0):
            continue

        province_heights[color].append(height_pixels[y, x])
print(f"Detected {len(province_heights)} provinces")
province_avg = {}
for color, values in province_heights.items():
    province_avg[color] = int(np.mean(values))
print("Computed province elevation averages")
new_height = np.zeros((height, width), dtype=np.uint8)
print("Painting provinces...")

for y in range(height):
    for x in range(width):
        color = tuple(prov_pixels[y, x])
        if color in province_avg:
            new_height[y, x] = province_avg[color]

output = Image.fromarray(new_height, mode="L")
output.save(output_file)

print("Heightmap generated:", output_file)
