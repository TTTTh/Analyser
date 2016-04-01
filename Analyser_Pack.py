# -*- coding:utf-8 -*-

import Converter
from Segmenter import Segmenter
#import ForwardIndex

local_html_cnt = 0
local_res_cnt = 0
LOCAL_HTML_FILEPATH = '/volumes/ExtraData/CrawlData/computer_hdu/HtmlSources/'
LOCAL_RESOURCES_FILEPATH = '/volumes/ExtraData/CrawlData/computer_hdu/Resources/'
REVERSER_INDEX_PATH = '/volumes/ExtraData/CrawlData/computer_hdu/reverser_index.txt'
URL_LIST = 'url_list.txt'
RESOURCES_LIST = 'resources_list.txt'
STOP_WORDS_PATH = 'stop_words_list.txt'
Converter.TOP_PATH = '/volumes/ExtraData/CrawlData/computer_hdu'

def to_bytestring(s, enc='utf-8'):
    if s:
        if isinstance(s, str):
            return s
        else :
            return s.encode(enc)

#初始化，生成一个新的分词器
def init( STOP_WORDS_PATH ):
    #打开停用词表
    print 'loading stop using words list'
    stop_words = open( STOP_WORDS_PATH )
    stop_words_list = stop_words.readlines()
    tmp_list = []
    #切割出换行符
    for word in stop_words_list:
        word = ''.join( word.split() )
        print 'word =' , word
        tmp_list.append( word )
    #使用停用词表初始化一个过滤器
    segmenter = Segmenter( tmp_list )
    return segmenter

#初始化
segmenter = init( STOP_WORDS_PATH )
#加载文件
#load_pages( RESOURCES_LIST ,URL_LIST, LOCAL_HTML_FILEPATH , LOCAL_RESOURCES_FILEPATH ,segmenter)
