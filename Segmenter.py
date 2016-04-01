# -*- coding:utf-8 -*-

'''
这是分词部分，使用的是结巴分词，同时包含一个停用词表
'''
import jieba
#import Converter


def to_bytestring(s, enc='utf-8'):
    if s:
        if isinstance(s, str):
            return s
        else :
            return s.encode(enc)

class Segmenter:
    def __init__(self, stop_words):
        self.stop_words = [stop_words,'\n','\r','\r\n']

    def seg_words( self, contents):
        seg_list = jieba.cut_for_search(contents)
        result_list = []
        for word in seg_list:
            #print 'word =',word
            word = to_bytestring(word)
            if word not in self.stop_words :
                result_list.append(word)
        #print 'len( result_list ) =' , len(result_list)
        return result_list


