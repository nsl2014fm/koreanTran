#coding=utf-8
import re
import json
import urllib

def selectHtml():
    html=r"""<div class="cmd_sent">
                                <div class="cmd_sent_en">
                                    <span class="cmd_sent_ee">
                                        심산이라 야생화가 <b>많이</b> 피었다.

                                    </span>
                                </div>
                                <div class="cmd_sent_cn clear">
                                    深山里野花盛开。
                                </div>
                            </div>

                            <div class="cmd_sent">
                                <div class="cmd_sent_en">
                                    <span class="cmd_sent_ee">
                                        궁전 건축은 나무토막을 <b>많이</b> 쓴다.

                                    </span>
                                </div>
                                <div class="cmd_sent_cn clear">
                                    宫殿建筑多用木砖。
                                </div>
                            </div>

                            <div class="cmd_sent">
                                <div class="cmd_sent_en">
                                    <span class="cmd_sent_ee">
                                        자기 몫보다 더 <b>많이</b> 차지하다

                                    </span>
                                </div>
                                <div class="cmd_sent_cn clear">
                                    实际占据量比自己应得的那份还要多
                                </div>
                            </div>"""
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
    re_space=re.compile('\s+',re.I) #匹配空格

    #result_kr = re_cmd_sent.findall(html)
    result_kr=re_kr.findall(html)
    result_cn=re_cn.findall(html)

    result=[]
    if (len(result_kr)==len(result_cn)):
        for m in range(len(result_kr)):
            temp_kr = {}
            result_kr[m]=re_html.sub('',result_kr[m])
            result_kr[m]=re_space.sub('',result_kr[m])

            result_cn[m] = re_html.sub('', result_cn[m])
            result_cn[m] = re_space.sub('', result_cn[m])

            temp_kr["A"]=result_kr[m]
            temp_kr["cn"]=result_cn[m]

            result.append(temp_kr)

    result = json.dumps(result)

    print result


if __name__ == '__main__':
    selectHtml()

