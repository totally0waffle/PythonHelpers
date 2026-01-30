from PIL import Image

# ================= CONFIG =================
# ADJUST THESE VALUES TO CONFIGURE WHAT VALUE THE BACKGROUND IS, LOWER VALUES ALLOW A GRADIENT
R_VAL = 250
G_VAL = 250
B_VAL = 250

image_path = input("enter filename: ")    # Update with your actual path
original_image = Image.open(image_path).convert("RGBA")
new_data = []
for item in original_image.getdata():
    if item[0] > R_VAL and item[1] > G_VAL and item[2] > B_VAL:
        new_data.append((255, 255, 255, 0))     # Make white transparent
    else:
        new_data.append(item)
original_image.putdata(new_data)

original_image.save((image_path + ".png"), "PNG")    # Save as PNG with transparency
