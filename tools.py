import os
import re
import json
import base64
import hashlib
import time
from io import BytesIO
from bs4 import BeautifulSoup
from functools import reduce
from fontTools.ttLib import TTFont


#   解析html文件
def readHtml(path=''):
    with open(path, 'r', encoding='utf-8') as f:
        html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        data_jstr = soup.find(id='resolved') if soup.find(id='resolved') else soup.find('textarea')
        data_jstr = data_jstr.text if data_jstr else '{}'
        data_json = json.loads(data_jstr)
        chapter_list = get_value_dict(data_json, ['appContext', '__connectedAutoFetch', 'manuscript', 'data', 'manuscriptData', 'pTagList'])
        chapter_list = chapter_list if chapter_list else get_value_dict(data_json, ['appContext', '__connectedAutoFetch', 'manuscript', 'data', 'manuscriptData', 'manuscript'])
        chapter_doc = "\n".join(chapter_list)
        chapter_soup = BeautifulSoup(chapter_doc, 'html.parser')
        chapter_line = [line.text for line in chapter_soup.find_all('p') if not is_number(line.text) and '备案号:' not in line.text]
        chapter = "\n".join(chapter_line)
        return chapter


def getFontFile(path=''):
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        style = soup.select_one('style[data-react-helmet]')
        font_list = re.findall(r'\(.*?\)', style.text)
        name_list = re.findall(r'\'zh_.*?\'', style.text)
        tf_path = ''
        for i, bd in enumerate(font_list):
            bd = bd.replace('(data:font/ttf;charset=utf-8;base64,', '').replace(')', '')
            name = name_list[i].replace('\'', '')
            tf_path = fontBase64Save(bd, name)
        return tf_path


#   字典多层取值
def get_value_dict(d: dict, keys_chain: list):
    return reduce(lambda x, y: x.get(y, {}), keys_chain, d)


#   base64字体文件存储
def fontBase64Save(font_data, name=''):
    name = name if name else time.time()
    fname = str(name) + '.ttf'
    file_path = os.path.join('data', 'font', fname)
    if not os.path.exists('data/font'):
        os.makedirs('data/font')
    font = TTFont(BytesIO(base64.decodebytes(font_data.encode())))
    font.save(file_path)
    return file_path


#   正则判断是否为数字
def is_number(s):
    return re.match(r'^-?\d+(\.\d+)?$', s) is not None
