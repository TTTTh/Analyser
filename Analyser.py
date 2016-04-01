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

#从记录中截取保存在本地的文件名
def cut_local_name( resource_record ) :
    i = 0
    while resource_record[ i ] != '.' :
        i = i + 1
    j = i + 1
    while resource_record[ j ] != ' ' :
        j = j + 1
    return resource_record [ 0 : j ] , resource_record[ i + 1 : j ]

#转换各个文件的格式
def convert_page( resources_record , local_file_path  ):
    item_path , suffix = cut_local_name( resources_record )
    local_txt_path = ''
    #print 'item_path =' , item_path , ', suffix =',suffix
    if suffix == 'doc' :
        local_txt_path = Converter.doc_2_txt( local_file_path + item_path )
    elif suffix == 'docx' :
        local_txt_path = Converter.docx_2_txt( local_file_path + item_path )
    elif suffix == 'rtf' :
        local_txt_path = Converter.rtf_2_txt( local_file_path + item_path )
    elif suffix == 'html':
        local_txt_path = Converter.html_2_txt( local_file_path + item_path )
    #elif suffix == 'xls':
    #    local_txt_path = Converter.xls_2_txt( local_file_path + item_path )
    elif suffix == 'pdf':
        #print 'item_path =',item_path
        local_txt_path = Converter.pdf_2_txt( local_file_path + item_path )
    return item_path , local_txt_path

#对得到的页面进行分词
def segment_page( local_txt_path , segmenter ):
    contents = open( local_txt_path )
    return segmenter.seg_words( contents.read() )

#建立正向索引
def Build_Forward_Index( words_in_page ):
    word_dict = {}
    for word in words_in_page:
        #print 'word = ',word
        #word = to_bytestring( word )
        if word_dict.has_key( word ) == False :
            word_dict[ word ] = 1
        else :
            word_dict[ word ] = word_dict[ word ] + 1
    return word_dict

#暂存分词表
def save_words_table( item_path , wordlist ):
    words_table_path = '/volumes/ExtraData/CrawlData/computer_hdu/WordsTable/'
    i = 0
    while item_path[i] != '.':
        i = i + 1
    save_path = words_table_path + item_path[ 0 : i ] + '.txt'
    fp = open( save_path , 'w' )
    for word in wordlist:
        fp.write( word + '\n')
    fp.close()



#保存倒排索引
def save_index( word_dict ):
    global REVERSER_INDEX_PATH
    reverser_fp = open(REVERSER_INDEX_PATH , 'w')
    #写入总共收录词汇
    reverser_fp.write( str(len(word_dict)) + '\n')
    for word ,inf_set in word_dict.items():
        #每个词，写入词本身， 以及出现文章数
        reverser_fp.write(word + ',' + str(len(inf_set)) + '\n')
        for path,cnt in inf_set:
            #这个词出现在具体文章的位置，以及出现次数
            reverser_fp.write(path + ',' + str(cnt) + '\n')

#建立倒排索引
def build_reverser_index(segmenter , word_dict , file_list_path , local_file_path):
    #打开需要被处理的文件的列表
    file_list = open( file_list_path )

    for item in file_list :
        #转换格式
        item_path , local_txt_path = convert_page( item , local_file_path )
        #如果是可以处理的文件，进行分词
        if len( local_txt_path ) != 0:
            print item_path , 'has successfully change to txt'
            #获得短路径（减少记录内的重复内容）
            local_short_path = Converter.realpath_2_short(local_txt_path)
            #分词
            words_in_page = segment_page( local_txt_path , segmenter )
            #建立正排索引，记录词频
            word_dict_in_page = Build_Forward_Index( words_in_page )
            #根据正排索引添加到倒排索引当中
            for word,cnt in word_dict_in_page.items() :
                word = to_bytestring(word)
                #inf = ( local_short_path , cnt )
                if word[0] != ' ' and word[0]!='\n':
                    word_dict.setdefault( word, set() ).add( ( local_short_path , cnt ) )
#读入页面
def load_pages( resources_list_path , url_list_path , local_html_filepath = '' , local_resources_filepath = '' , segmenter = None) :
    word_dict = {}
    #分析资源列表
    build_reverser_index(segmenter,word_dict,resources_list_path , local_resources_filepath)
    build_reverser_index(segmenter , word_dict , url_list_path , local_html_filepath)
    #保存分词结果
    save_index( word_dict )


#初始化
segmenter = init( STOP_WORDS_PATH )
#加载文件
load_pages( RESOURCES_LIST ,URL_LIST, LOCAL_HTML_FILEPATH , LOCAL_RESOURCES_FILEPATH ,segmenter)
