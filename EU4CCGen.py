from PIL import Image
import itertools

bmp_file = input("Enter BMP file path: ")
output_html = "unused_colors.html"
max_unused_colors = 10000   # prevent huge output

print("Loading image...")
img = Image.open(bmp_file).convert("RGB")

used_colors = set(img.getdata())

print(f"Unique colors used in BMP: {len(used_colors)}")

print("Scanning RGB space for unused colors...")

unused_colors = []

for r, g, b in itertools.product(range(256), repeat=3):
    if (r, g, b) not in used_colors:
        unused_colors.append((r, g, b))
    if len(unused_colors) >= max_unused_colors:
        break

print(f"Collected {len(unused_colors)} unused RGB codes.")
print("Generating HTML checklist...")

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Unused RGB Codes</title>
<style>
body { font-family: Arial; }
.color-row {
    display: flex;
    align-items: center;
    margin: 4px 0;
}
.swatch {
    width: 30px;
    height: 20px;
    border: 1px solid black;
    margin-right: 10px;
}
.code {
    font-family: monospace;
    margin-left: 10px;
}
</style>
</head>
<body>

<h2>Unused RGB Codes</h2>
<p>Checkbox to track which colors you've used.</p>
<hr>
"""

for r, g, b in unused_colors:
    rgb_text = f"{r},{g},{b}"
    html += f"""
<div class="color-row">
<input type="checkbox">
<div class="swatch" style="background-color: rgb({r},{g},{b});"></div>
<span class="code">{rgb_text}</span>
</div>
"""

html += """
</body>
</html>
"""

with open(output_html, "w") as f:
    f.write(html)

print(f"Done! HTML file saved as: {output_html}")
