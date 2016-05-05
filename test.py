# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib

class fm_Spider:
    def __init__(self):
        # 登陆url
        self.loginUrl = 'http://dict.hjenglish.com/kr/많이'

        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
        # 初始化cookiejar来处理cookie信息
        self.cookieJar = cookielib.CookieJar()

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))


    def translate_init(self):
        # 初始化连接并且获取cookie
        myRequest = urllib2.Request(url=self.loginUrl)
        # 访问登陆页面，并获取cookie文件
        resultLogin = self.opener.open(myRequest)
        # resultGrade=self.opener.open(self.gradeUrl)

        print resultLogin.read().decode('gbk')

mySpider=fm_Spider()
mySpider.translate_init()