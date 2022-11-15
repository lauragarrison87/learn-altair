from PIL import Image

image_1 = Image.open(r'C:\Users\laura\Downloads\laura-garrison.jpg')
im_1 = image_1.convert('RGB')
im_1.save(r'C:\Users\laura\Downloads\laura-garrison.pdf')