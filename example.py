from PIL import Image
import os

for x in os.listdir("pictures"):
    try:
        im1 = Image.open(f'pictures/{x}')
        im1.save(f'{x.replace(".jpg","")}.pdf', "PDF" ,resolution=100.0)
    except Exception as e:
        print(e)
