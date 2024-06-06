# 출처
# https://velog.io/@bokyungkim/EasyOCR%EC%9D%84-%EC%82%AC%EC%9A%A9%ED%95%B4-%ED%8B%B0%EC%BC%93-%EC%86%8D-%EB%AC%B8%EC%9E%90%EB%A5%BC-%ED%85%8D%EC%8A%A4%ED%8A%B8%ED%99%94-%ED%95%B4%EB%B3%B4%EC%9E%90
import easyocr
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image

img_url = "./img/test/ko_en.png"

reader = easyocr.Reader(['ko', 'en'], gpu = True)
result = reader.readtext(img_url)
img    = cv2.imread(img_url)
img = Image.fromarray(img)
font = ImageFont.load_default(10)
draw = ImageDraw.Draw(img)
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")
for i in result :
    x = i[0][0][0] 
    y = i[0][0][1] 
    w = i[0][1][0] - i[0][0][0] 
    h = i[0][2][1] - i[0][1][1]

    color_idx = random.randint(0,255) 
    color = [int(c) for c in COLORS[color_idx]]

    draw.rectangle(((x, y), (x+w, y+h)), outline=tuple(color), width=2)
    draw.text((int((x + x + w) / 2) , y-2),str(i[1]), font=font, fill=tuple(color),)

plt.figure(figsize=(50,50))
plt.imshow(img)
plt.show()