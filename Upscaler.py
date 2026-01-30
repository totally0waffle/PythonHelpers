from PIL import Image

# Load image
image_path = input("enter filename: ")  # Update with your actual path
original_image = Image.open(image_path).convert("RGBA")

# Remove white background
new_data = []
for item in original_image.getdata():
    #if item[0] > 240 and item[1] > 240 and item[2] > 240:
    #    new_data.append((255, 255, 255, 0))  # Make white transparent
    new_data.append(item)

original_image.putdata(new_data)

# Resize to 4K (3840x2160 max) while maintaining aspect ratio
target_width, target_height = 1920, 1920
scale_factor = min(target_width / original_image.width, target_height / original_image.height)
new_size = (int(original_image.width * scale_factor), int(original_image.height * scale_factor))
upscaled_image = original_image.resize(new_size, Image.LANCZOS)

# Save as PNG with transparency
upscaled_image.save((image_path + ".png"), "PNG")
