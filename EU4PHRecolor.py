from PIL import Image
import itertools
import json

eu4_map = input("Path to original EU4 provinces.bmp: ")
custom_map = input("Path to your custom province map: ")

output_map = "recolored_provinces.bmp"
mapping_file = "province_color_mapping.json"

OCEAN_COLOR = (0, 255, 0)
print("Loading images...")

eu4_img = Image.open(eu4_map).convert("RGB")
custom_img = Image.open(custom_map).convert("RGB")

eu4_pixels = list(eu4_img.getdata())
custom_pixels = list(custom_img.getdata())
print("Scanning EU4 map for used RGB codes...")

used_colors = set(eu4_pixels)

print("Used colors detected:", len(used_colors))
print("Generating unused RGB codes...")

unused_colors = []

for r, g, b in itertools.product(range(256), repeat=3):

    color = (r, g, b)

    if color in used_colors:
        continue

    if color == OCEAN_COLOR:
        continue

    unused_colors.append(color)

print("Available unused colors:", len(unused_colors))

custom_colors = set(custom_pixels)

if OCEAN_COLOR in custom_colors:
    custom_colors.remove(OCEAN_COLOR)

print("Custom provinces detected:", len(custom_colors))

if len(custom_colors) > len(unused_colors):
    raise Exception("Not enough unused RGB codes available!")
color_map = {}

for i, color in enumerate(custom_colors):
    color_map[color] = unused_colors[i]

print("Color mapping created.")
print("Recoloring provinces...")

new_pixels = []

for p in custom_pixels:

    if p == OCEAN_COLOR:
        new_pixels.append(p)
    else:
        new_pixels.append(color_map[p])

new_img = Image.new("RGB", custom_img.size)
new_img.putdata(new_pixels)

new_img.save(output_map)

print("Saved recolored map:", output_map)

mapping_readable = {
    f"{k[0]},{k[1]},{k[2]}": f"{v[0]},{v[1]},{v[2]}"
    for k, v in color_map.items()
}

with open(mapping_file, "w") as f:
    json.dump(mapping_readable, f, indent=4)

print("Saved province mapping:", mapping_file)
print("Done!")
