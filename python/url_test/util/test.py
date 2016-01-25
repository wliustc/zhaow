#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf_8 -*-

try:
    import pytesseract
    from PIL import Image, ImageFilter, ImageEnhance
except ImportError:
    print '模块导入错误,请使用pip安装,pytesseract依赖以下库：'
    print 'http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil'
    print 'http://code.google.com/p/tesseract-ocr/'
    raise SystemExit

image = Image.open('../config/vcode.png')
image = image.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2)
image = image.convert('1')
print image.show()
# vcode = pytesseract.image_to_string(image)
# print vcode
