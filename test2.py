import  urllib2

def test():
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'cookiename=cookievalue'))
    f = opener.open("http://example.com/")
    print f

if __name__=='__main__':
    test()