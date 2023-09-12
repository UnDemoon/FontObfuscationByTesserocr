'''
Author: your name
Date: 2020-09-28 15:41:31
LastEditTime: 2021-03-22 16:47:45
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /qqSsoGather/pyinstall.py
'''
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts = ['main.py',
            'ui_home.py',
            'Decoder.py',
            'tools.py',
            '-F',
            '-w',
            # '-D',
            '--icon=favicon.ico']
    run(opts)
