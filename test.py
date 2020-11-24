from PIL import Image
import os
im_list = [Image.open(f"pictures/{x}") for x in os.listdir('pictures')]
im1 = im_list[0]
im1.save('ex.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=im_list[1:])
