# -*- coding:utf-8 -*-
'''
这是转换器，已经实现了doc,rtf,docx到txt的转换
待实现pdf,html,xml格式到txt的转换
'''
import os
from bs4 import BeautifulSoup
import re
import xlrd
import pdf_2_txt_pack

def to_bytestring(s, enc='utf-8'):
    if s:
        if isinstance(s, str):
            return s
        else :
            return s.encode(enc)

TOP_PATH = '/volumes/ExtraData/CrawlData/computer_hdu'
def  doc_2_txt(doc_path):

    cmd = "textutil -convert txt " + doc_path

    os.system(cmd)

    result_path = doc_path[ 0: len(doc_path) - 3] + 'txt'

    return result_path

def  docx_2_txt(docx_path):

    cmd = "textutil -convert txt " + docx_path

    os.system(cmd)

    result_path = docx_path[ 0: len(docx_path) - 4] + 'txt'

    return result_path

def rtf_2_txt(rtf_path):

    cmd = "textutil -convert txt " + rtf_path

    os.system(cmd)

    result_path = rtf_path[ 0: len(rtf_path) - 3] + 'txt'

    return result_path

#将xls转换为txt
def xls_2_txt(xls_path):
    print 'begin change xls', xls_path
    book = xlrd.open_workbook(xls_path)
    result_path = xls_path[0 : len(xls_path) - 3] + 'txt'
    result_fp = open(result_path , 'w')
    #print xls_path,'open success'
    for sheet_name in book.sheet_names():
        sheet = book.sheet_by_name(sheet_name)
        for row_no in range(0,sheet.nrows):
            for col_no in range(0,sheet.ncols):
                cell_value = sheet.cell_value(row_no ,col_no)

                if isinstance(cell_value , str) == False and isinstance(cell_value , unicode) == False:
                    cell_value = str(cell_value)
                cell_value = to_bytestring(cell_value)
                if cell_value == None:
                    continue
                result_fp.write(cell_value + '\n')

    result_fp.close()
    return result_path

#将pdf格式转换为txt
def pdf_2_txt(pdf_path):
    return pdf_2_txt_pack.convert(pdf_path)


#读取html源码并保存为txt格式
def html_2_txt(html_path):
    #打开文件
    sources = open(html_path)

    #清洗html源码
    #解析
    htmlsoup = BeautifulSoup(sources,'html.parser')
    #清除qstyle和script
    [script.extract() for script in htmlsoup.findAll('script')]
    [style.extract() for style in htmlsoup.findAll('style')]
    #通过正则表达式清除html标签
    reg1 = re.compile("<[^>]*>")
    content = reg1.sub('',htmlsoup.prettify())

    #保存得到的内容
    result_path = html_path[0 : len(html_path) - 4] + 'txt'
    txt_fp = open(result_path , 'w')
    txt_fp.write( to_bytestring(content) )

    return result_path

def realpath_2_short(real_path):
    global TOP_PATH
    length = len(TOP_PATH)
    if real_path[0 : length] == TOP_PATH:
        return real_path[length : len(real_path)]

def shortpath_2_real(short_path):
    global TOP_PATH
    return TOP_PATH + short_path


