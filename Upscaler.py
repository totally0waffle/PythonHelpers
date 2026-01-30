from PIL import Image

# Load image
image_path = input("enter filename: ")  # Update with your actual path
original_image = Image.open(image_path)

target_width, target_height = 1920, 1920
scale_factor = min(target_width / original_image.width, target_height / original_image.height)
new_size = (int(original_image.width * scale_factor), int(original_image.height * scale_factor))
upscaled_image = original_image.resize(new_size, Image.LANCZOS)

upscaled_image.save(("new" + image_path), "jpeg", quality=95)
