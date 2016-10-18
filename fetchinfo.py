import md5, sys, urllib2
username = sys.argv[1]
pwdmd5 = md5.new(sys.argv[2]).hexdigest().upper()
result = urllib2.urlopen("http://smart2connect.yunext.com/api/device/wifi/list?accessKey=Q763W08JZ07V23FR99410B3PC945LT28&username=%s&password=%s" % (username, pwdmd5)).read()
print result
