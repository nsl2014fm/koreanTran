#-*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
import random
import time
import sys
import re
import json

def loadHtml(url):
    """输入url，载入页面，并写入到txt中"""
    ## 声明一个CookieJar对象实例来保存cookie
    cookie = cookielib.CookieJar()
    ## 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    ## 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    header=[('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1')]
    opener.addheaders=header
    urllib2.install_opener(opener)

    req = urllib2.Request(url)
    ## 此处的open方法同urllib2的urlopen方法，也可以传入request
    ## response = opener.open('http://baidu.com/')
    req.add_header("Referer", url)
    try:
        while True:
            response = urllib2.urlopen(req)
            result = response.read()

            interval = random.uniform(0.001, 20)
            time.sleep(interval)  ##设置定时
            return result
    except urllib2.URLError, e:
        print "====出错原因==="+e.reason+"============"
        return

def regular(html):
    """正则匹配html"""
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_style = re.compile('style="[^"]+"', re.I)  # 去掉style
    re_html = re.compile('<[^>]+>')  # 获取html标签

    html = re_br.sub('', html)
    html = re_style.sub('', html)
    re_kr = re.compile('\<span\s+class="cmd_sent_ee"+\>[^span]+\<\/span\>', re.I)  # 匹配韩文
    re_cn = re.compile('\<div\s+class="cmd_sent_cn clear"\>[^\<]+\<\/div\>', re.I)  # 匹配中文
    re_space = re.compile('\s', re.I)  # 匹配空格

    # html = re_space.sub('',html)
    result_kr = re_kr.findall(html)
    result_cn = re_cn.findall(html)

    result = []
    if ((len(result_kr)) == 0 or len(result_cn) == 0):
        print "====无翻译值===="
        return
    else:
        if (len(result_kr) == len(result_cn)):
            for m in range(len(result_kr)):
                temp_kr = {}
                if (result_kr[m].strip() and result_cn[m].strip()):
                    result_kr[m] = re_html.sub('', result_kr[m])
                    result_kr[m] = re_space.sub('', result_kr[m])

                    result_cn[m] = re_html.sub('', result_cn[m])
                    result_cn[m] = re_space.sub('', result_cn[m])

                    temp_kr["kr"] = result_kr[m].strip()
                    temp_kr["cn"] = result_cn[m].strip()
                    temp_kr = json.dumps(temp_kr, ensure_ascii=False)  # 将ascii码编码false掉
                    result.append(temp_kr)
        result = json.dumps(result, ensure_ascii=False)
        print result
        return result

def urlParse(word):
    url="http://dict.hjenglish.com/kr/"
    word=urllib.quote(word)

    url=url+word
    return url

def loadTxt():
    items=[] ##输出数据，json格式
    word_load = open('kr_words_loaded.txt', 'a')
    words=open("kr_words.txt",'r')
    compare=open('kr_words_loaded.txt','r')

    data= open('kr_data5.txt', 'a')

    lines=words.readlines()
    compare_line=compare.readlines()

    kkk = 0
    countLine = 0
    while True:
        for m in range(len(compare_line),len(lines)):
            countLine = countLine + 1
            line=lines[m].strip()
            if line:  #跟字符串，只要非空，则返回true；若跟数字，只要非零，则返回true
                line = line.strip()  #strip(),删除特定字符函数，没有参数则去掉空格

                print "目前读入单词数" + str(countLine)
                print "当前单词：" + line

                url=urlParse(line) ##拼接链接

                html=loadHtml(url) ##获得页面
                item=regular(html)  ##正则匹配
                word_load.write(line + '\n')  #写入文件
                if (item is not None):

                    items.append(item)
                    data.write(items[kkk] + "\n")  # 对txt进行写入操作
                    kkk = kkk + 1
                    print "目前有效数" + str(kkk)
                else:
                    continue
            else:
                break
    word_load.close()
    words.close()
    compare.close()
    data.close()

    items=json.dumps(items,ensure_ascii=False)

    return items

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    # loadHtml('http://baidu.com/')
    loadTxt()