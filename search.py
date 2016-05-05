#coding=utf-8
import urllib
import urllib2
import cookielib
import re  #正则
import json
import sys
import random
from threading import Timer
import time
import logging

# import format
#from format import save_json_text, load_json_text

def translate(word):
    #========请求页面============================
    #quote对单个字符进行转换
    word=urllib.quote(word) #将url数据获取之后，并将其编码，从而适用与URL字符串中，使其能被打印和被web服务器接受。
    url = 'http://dict.hjenglish.com/kr/'
    #newword=urllib.urlencode(word)
    targetUrl = url+word

    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookielib.CookieJar()
    # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    #opener = urllib2.build_opener()

    myHeaders={}
    myHeaders['1']=[("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.360")]
    myHeaders['2']=[('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1')]
    myHeaders['3']=[('User-agent','Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1')]
    myHeaders['4']=[('User-agent','Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 4.1')]
    myHeaders['0']=[('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 4.1')]

    m=random.randint(11,22)
    m=m%5
    opener.addheaders=myHeaders[str(m)]
    urllib2.install_opener(opener)

    req=urllib2.Request(targetUrl)
    # 此处的open方法同urllib2的urlopen方法，也可以传入request
    # response = opener.open('http://baidu.com/')
    req.add_header("Referer",targetUrl)

    try:
        while True:
            response = urllib2.urlopen(req)
            interval=random.uniform(0.001,20)
            result = response.read()
            print interval

            time.sleep(interval)  ##设置定时
            return result


    except urllib2.URLError, e:
        print e.reason
        return
    #=========筛选字符=============================

def selectHtml(html):
    re_h = re.compile('<[^>]+>') #取html标签
    kr='(?<=\<div\>)[^<,^>](?=\</div\>)'
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    blank_line = re.compile('\n')
    re_style = re.compile('style="[^"]+"', re.I)  # 去掉style
    re_html=re.compile('<[^>]+>') #获取html标签

    html=re_br.sub('',html)
    #html=blank_line.sub('',html)
    html=re_style.sub('',html)

    #re_cmd_sent=re.compile('\<div\s+class="cmd_sent"+\>[^span]+\<\/div\>',re.I)
    re_kr=re.compile('\<span\s+class="cmd_sent_ee"+\>[^span]+\<\/span\>',re.I) #匹配韩文
    re_cn = re.compile('\<div\s+class="cmd_sent_cn clear"\>[^\<]+\<\/div\>', re.I) #匹配中文
    re_space=re.compile('\s',re.I) #匹配空格

    #html = re_space.sub('',html)
    result_kr=re_kr.findall(html)
    result_cn=re_cn.findall(html)

    result=[]
    if ((len(result_kr))==0 or len(result_cn)==0):
        return
    else:
        if (len(result_kr)==len(result_cn)):
            for m in range(len(result_kr)):
                temp_kr = {}
                if (result_kr[m].strip() and result_cn[m].strip()):
                    result_kr[m]=re_html.sub('',result_kr[m])
                    result_kr[m]=re_space.sub('',result_kr[m])

                    result_cn[m] = re_html.sub('', result_cn[m])
                    result_cn[m] = re_space.sub('', result_cn[m])

                    #print re_html.sub('', result_kr[m])
                    temp_kr["kr"]=result_kr[m].strip()
                    temp_kr["cn"]=result_cn[m].strip()

                    #print temp_kr["A"]
                    temp_kr=json.dumps(temp_kr,ensure_ascii=False) #将ascii码编码false掉
                    #print temp_kr
                    result.append(temp_kr)
                    #print result[m]
        result = json.dumps(result,ensure_ascii=False)
        print result
        return result

def loadTxt():
    word = open("kr_words.txt", "r")
    result=[]
    data= open('kr_data4.txt', 'a')
    m = 0
    countLine = 0
    while True:
        line = word.readline() #读取txt中的行数据

        if line:  #跟字符串，只要非空，则返回true；若跟数字，只要非零，则返回true
            line = line.strip()  #strip(),删除特定字符函数，没有参数则去掉空格
            p = line.rfind('.')  #rfind() 返回字符串最后一次出现的位置，如果没有匹配项则返回-1
            filename = line[0:p]

            print "目前读入单词数" + str(countLine)
            print "当前单词："+line
            countLine = countLine + 1

            #print line.encode("utf-8")
            # sleepTime=random.randint(6,25) ##设置随机沉睡时间
            # for sleep in range(sleepTime+1):
            # if(sleep>=sleepTime):
            html=translate(line)
            selectItem=selectHtml(html)
            # (selectItem)
            if (selectItem is not None):
                print "目前有效数"+str(m)
                result.append(selectItem)
                data.write(result[m] + "\n") #对txt进行写入操作
                m = m+1
            else:
                continue
        else:
            break
    word.close()
    data.close()

    result=json.dumps(result,ensure_ascii=False)
    return result

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    temp=loadTxt()
    #print temp