import easyocr
import hanja
import re

img_url = "./img/test/chinese_tra.jpg"

# 어떤 텍스트를 추출할 건지 선언
# https://www.jaided.ai/easyocr/
# 중국어 번체, 영어
reader = None
# cpu 사용 버전
# reader = easyocr.Reader(['ch_sim','en'], gpu=False)
# gpu 사용 버전
reader = easyocr.Reader(['ch_tra', 'en'])

# 이미지 내의 텍스트를 list 형태로 추출
with open("./img/test/chinese_tra.jpg", "rb") as f:
    img = f.read()

# 추출된 정보중에 글자만 한 개의 list 형태로 return
extract = reader.readtext(img, detail = 0, paragraph=True)
print(type(extract)) # 타입 list

result = ''.join(extract) # list를 str 형식으로 변환
print(hanja.translate(result, 'combination-text')) # 번역