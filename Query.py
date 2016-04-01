# -*- coding: utf-8 -*-
#查询器

#import chardet
#import easygui
import Analyser_Pack

TOP_PATH = '/volumes/ExtraData/CrawlData/computer_hdu'
REVERSER_INDEX_PATH = '/volumes/ExtraData/CrawlData/computer_hdu/reverser_index.txt'
'''
高分,3
/Resources/55.txt,5
/Resources/上机实验报告示例_数据库.txt,2
/Resources/57.txt,6
'''

def cut_record(record):
    i = 1
    while record[i] != ',':
        i = i + 1
    return record[0 : i],int(record[i + 1 : len(record) ])

def Init(words_path , words_dict):
    record_fp = open(words_path)
    n = int(record_fp.readline())

    while n > 0:
        n = n - 1
        word , page_num = cut_record(record_fp.readline())
        #print 'word =' , word , ', page_num =' , page_num
        while page_num > 0:
            page_num = page_num - 1
            path , time = cut_record(record_fp.readline())
            words_dict.setdefault( word , list() ).append( (path , time) )
    seg = Analyser_Pack.init(Analyser_Pack.STOP_WORDS_PATH)
    return seg

#剪切出某个页面内某一行，关键词附近的结果
def get_result_in_line(line , query_word):
    result_line = ''
    line = line.decode('utf-8')
    query_word = query_word.decode('utf-8')
    #如果这一行太长 ，切出一部分
    if len(line) > 40 :
        col_index = line.find(query_word)
        left_p = col_index - 10
        #防越界操作
        if left_p < 0 :
            left_p = 0
        right_p =col_index + 20
        if right_p > len(line):
            right_p = len(line)
        #切割字符串
        result_line = line[left_p : right_p]
    else:
        result_line = line
    result_line = result_line.encode('utf-8')
    return ''.join( result_line.split() )

#输出某一个搜索出来的文件地址 ，对应的文件的相关结果
def show_one_result(result , query_word):
    #打开文件
    content = open(TOP_PATH + result[0]).readlines()
    #扫描每一行
    for line in content :
        #如果被查询的词在这一行里
        if query_word in line:
            print get_result_in_line(line , query_word)

#输出某个词的查询结果
def show_query_result(query_result , query_word):
    #按照词频排序
    query_result.sort(lambda x,y : cmp(x[1],y[1]) ,reverse = True)
    #输出某个词单独的结果
    for result in query_result:
        print result[0] , result[1]
        show_one_result(result , query_word)


#查询某个词
def Query(query_word , words_dict):
    if words_dict.has_key(query_word):
        query_result = words_dict[query_word]
        show_query_result(query_result , query_word)
    else :
        print '找不到这个词啦'

def main(words_dict , seg):
    while True :
        query_words = raw_input()
        if query_words == 'exit':
            break
        else :
            query_words = seg.seg_words(query_words)
            for query_word in query_words :
                print Analyser_Pack.to_bytestring(query_word)
                Query(query_word , words_dict)
                print ''

words_dict = {}
seg = Init(REVERSER_INDEX_PATH , words_dict)
main(words_dict , seg)
