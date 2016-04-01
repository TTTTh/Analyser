# -*- coding:utf-8 -*-
#转换格式
import os

cmd = 'iconv -c -f windows-1252 -t UTF-8 stop_words_list.txt >> stop_words_list.txt'

os.system(cmd)
