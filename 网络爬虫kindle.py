#coding:utf=8
import urllib2
import re
# 1. 获取应用商店的网址
url1 = 'https://www.amazon.cn' #定义字符串url
response1 = urllib2.urlopen(url1) #打开网站首页 获取源代码
KindlePattern1 = re.compile('Kindle 商店.*?url1":"(.*?)"', re.S) # re.compile(string, flags)创建模式，pattern一般用re.S(多行选择)
KindleURL1 = url1 + re.search(KindlePattern1, response1.read()).group(1) # 根据正则表达式模式匹配到应用商店的网址
print ('应用商店的网址：\n %s' % KindleURL1)  #将匹配好的数据打印出来

#2.通过应用商店获取到今日特价书
url2 = KindleURL1
response2 = urllib2.urlopen(url2)
discountPattern  =  re.compile('什么值得读.*?href="(.*?)">今日特价书', re.S)
bookURL = url1 + re.search(discountPattern, response2.read()).group(1)
print ('今日特价的网址：\n %s' % bookURL)

#3.分析今日特价书的页面，获取书的详细信息
response3 = urllib2.urlopen(bookURL) #获取今日特价网站的源代码
infoPattern = re.compile('productImage">.*?href="(.*?)".*?src="(.*?)".*?productTitle">.*?>(.*?)<.*?productByLine">(.*?)<.*?a-color-price">(.*?)<',re.S)
infos = re.findall(infoPattern, response3.read())
for info in infos:
    print ('链接：' + url1 + info[0].strip('\n'))
    print ('图片地址：' + info[1].strip('\n'))
    print ('书名：' + info[2].strip('\n'))
    print ('作者：' + info[3].strip('\n'))
    print ('价格: ' + info[4].strip('\n'))

    imgURL = info[1].strip('\n') # 获得图片链接

imgNamePattern = re.compile('/I/(.*?)jpg',re.S) # 用正则表达式提取图片名称
imgName = re.search(imgNamePattern, imgURL) # 提取图片名称
response = urllib2.urlopen(imgURL) # 打开图片链接

with open(imgName.group(1)+'jpg', 'wb') as file: # 以二进制写方式打开
    file.write(response.read()) # 写入文件