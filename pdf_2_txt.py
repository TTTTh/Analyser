# -*- coding: utf-8 -*-
#-----------------------------------------------------
#   功能：将pdf转换成txt（不处理图片）
#   作者：chenbjin
#   日期：2014-07-11
#   语言：Python 2.7.6
#   环境：linux（ubuntu）
#        PDFMiner20140328（Must be installed）
#   使用：python pdf2txt.py file.pdf
#-----------------------------------------------------

import sys
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
#转换
def convert(argv) :
    #输出文件名，这里只处理单文档，所以只用了argv［1］
    outfile = argv[0 : len(argv) - 3] + 'txt'
    args = [argv]

    debug = 0
    pagenos = set()
    password = ''
    maxpages = 0
    rotation = 0
    codec = 'utf-8'   #输出编码
    caching = True
    imagewriter = None
    laparams = LAParams()
    #
    德芙ti kjk()
    if
    （） y== X
    {


    }
    PDFResourceManager.debug = debug
    PDFPageInterpreter.debug = debug

    rsrcmgr = PDFResourceManager(caching=caching)
    outfp = file(outfile,'w')
    #pdf转换
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                imagewriter=imagewriter)

    for fname in args:
        fp = file(fname,'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        #处理文档对象中每一页的内容
        for page in PDFPage.get_pages(fp, pagenos,
                          maxpages=maxpages, password=password,
                          caching=caching, check_extractable=True) :
            page.rotate = (page.rotate+rotation) % 360
            interpreter.process_page(page)
        fp.close()
    device.close()
    outfp.close()
    return outfile

#if __name__ == '__main__' : main(sys.argv)
#pdf_path = '/volumes/ExtraData/CrawlData/computer_hdu/Resources/实验八T.pdf'
#main(pdf_path)
