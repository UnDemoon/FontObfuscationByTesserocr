# 文字识别
import string
import time
import os
from tesserocr import PyTessBaseAPI, PSM
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

import tools


class OCR(object):
    default_config = {
        # ocr engine
        'data_path': None,
        'lang': 'chi_sim',
        'white_list': None,
        'black_list': None,
        # image
        'font': None,
        'image_size': (60, 60),
        'font_size': 30,
        'text_offset': (15, 15),
    }

    def __init__(self, config={}):
        c = dict(self.default_config)
        c.update(config)
        self.api = PyTessBaseAPI(path=c['data_path'], lang=c['lang'], psm=PSM.SINGLE_CHAR)
        self.img = Image.new('RGB', c['image_size'], color='white')
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype(c['font'], size=c['font_size'])
        self.text_offset = c['text_offset']
        if c['white_list']:
            self.api.SetVariable('tessedit_char_whitelist', c['white_list'])
        if c['black_list']:
            self.api.SetVariable('tessedit_char_blacklist', c['black_list'])
        self.font_tool = TTFont(c['font'])
        self.empty_char = self._predict_empty_char()

    def _predict_empty_char(self):
        self.api.SetImage(self.img)
        return self.api.GetUTF8Text().strip()

    def is_char_in_font(self, char):
        for t in self.font_tool['cmap'].tables:
            if t.isUnicode():
                if ord(char) in t.cmap:
                    return True
        return False

    def predict(self, char):
        ''' 返回转换后的字符，或空串'' '''
        if not self.is_char_in_font(char):
            return char  # 若字体无法渲染该字符，则原样返回。此处可酌情移除。
        self.img.paste('white', (0, 0, self.img.size[0], self.img.size[1]))
        self.draw.text(self.text_offset, char, fill='black', font=self.font)
        self.api.SetImage(self.img)
        c2 = self.api.GetUTF8Text().strip()
        if c2 == self.empty_char:
            return ''  # 某些字符可能渲染成空白，此时返回空串。
        return c2


#   文字识别类
class Decoder(object):
    def __init__(self, data_path, font):
        self.cache = {}  # 缓存已知的映射关系。
        OCR.default_config.update(dict(data_path=data_path, font=font))
        self.ocr_digit = OCR(dict(
            lang='eng',
            white_list=string.digits,
            black_list=string.ascii_letters,
        ))
        self.ocr_letter = OCR(dict(
            lang='eng',
            black_list=string.digits,
            white_list=string.ascii_letters,
        ))
        self.ocr_other = OCR()

    def decode(self, char):
        if char not in self.cache:
            c2 = self._decode_when_cache_miss(char)
            self.cache[char] = c2 or char
        return self.cache[char]

    def _decode_when_cache_miss(self, char):
        ocr = self.ocr_other
        if char in string.digits:
            ocr = self.ocr_digit
        elif char in string.ascii_letters:
            ocr = self.ocr_letter
        return ocr.predict(char)


if __name__ == '__main__':
    # #   示列代码
    org_path = 'data/input/org_2.html'
    #   正式
    html_txt = tools.readHtml(org_path)
    font_file = tools.getFontFile(org_path)
    d = Decoder('tessdata-main/', font_file)
    txt = ''.join(map(d.decode, html_txt))
    name = str(time.time()) + 'txt'
    output_file = os.path.join('data', 'output', name)
    with open(output_file, 'w', encoding='utf-8') as of:
        of.write(txt)
