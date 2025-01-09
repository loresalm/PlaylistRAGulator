import time
import ollama  # type: ignore
import json
from PIL import Image  # type: ignore

print("load config")
config_file_path = 'data/user_inputs/config.json'
with open(config_file_path, 'r') as json_file:
    config = json.load(json_file)

# Assign the values to variables
vismodel = config.get("vismodel")
img_path = config.get("img_path")
img_small_path = config.get("img_small_path")
new_width = config.get("img_w")
new_height = config.get("img_h")
img_desc_path = config.get("img_desc_path")

print("config loaded")
######################
#                    #
#    Resize image    #
#                    #
######################

# Open the image file
with Image.open(img_path) as img:
    original_width, original_height = img.size
    if original_width > original_height:
        # Landscape orientation
        new_size = (new_height, new_width)
    else:
        # Portrait or square orientation
        new_size = (new_width, new_height)

    # Resize the image
    resized_img = img.resize(new_size)
    resized_img.save(img_small_path)
    print(f"Resized img saved to {img_small_path}")
######################
#                    #
#   observe image    #
#                    #
######################
img_prompt = """
Describe the image with a list of adjectives.
Focus on the ambient and the vibe of the place rapresented in this image:
"""
llava_start = time.time()
vismodel = "llava:7b"
res = ollama.chat(
    model=vismodel,
    messages=[{'role': 'user',
               'content': img_prompt,
               'images': [img_path]}])
desc7b = res['message']['content']
llava_end = time.time()
print(f"Immage processed in {round((llava_end- llava_start)/60, 2)} min")
with open(img_desc_path, 'w') as txt_file:
    txt_file.write(desc7b)
    print(f"Analysis saved to {img_desc_path}")
