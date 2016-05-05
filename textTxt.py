#coding=utf-8
import re
import json
import urllib

def writeTxt():

    # list = [[1111, 2, 3], [4, 5, 6], [7, 8, 9]]
    # f = open('kr_data.txt', 'w')
    # for i in list:
    #     k = ' '.join([str(j) for j in i])
    #     f.write(k + "\n")
    # f.close()
    data={}
    m="[]"
    data['n']="我"
    data=json.dumps(data,ensure_ascii=False)
    if (m!=u"[]"):
        print "haha"
    else:
        print "你好"
    #print data

if __name__ == '__main__':
    writeTxt()

