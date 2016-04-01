# -*- coding:utf-8 -*-
# 建立正向索引

def Build_Forward_Index( words_in_page ):
    word_dict = {}
    for word in words_in_page:
        if word_dict.has_key( word ) == False :
            word_dict[ word ] = 1
        else :
            word_dict[ word ] = word_dict[ word ] + 1
    return word_dict


