import pytesseract

img_path = 'test.png'
lang = 'eng'
text = pytesseract.image_to_string(img_path, lang=lang)

print(text)
