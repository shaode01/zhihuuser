# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 08:46:12 2017

@author: 
"""

import traceback
import pandas as pd
import requests
import itchat
import time
from bs4 import BeautifulSoup
import csv
keywords=[u'机器学习',u'数据挖掘',u'聚类',u'贝叶斯',u'马尔科夫',u'SVM',
          u'支持向量机',u'关联规则',u'神经网络',u'Hadoop',u'线性回归',u'逻辑斯蒂回归',u'统计回归',
          u'决策树',u'深度学习',u'回归模型',
          u'模式识别',u'预测',u'时间序列',u'图方法',u'协同过滤',u'深度学习',]
notwords=[u'文案撰写',u'图像识别',u'语音识别',u'视频识别',u'文书管理',u'助理',u'记者'
          ,u'教育培训',u'日语岗位',u'行业分析',u'业务拓展',u'主管',u'前台',u'销售',u'给排水',u'媒介策划'
          ,u'网络运营',u'电话访问员',u'中专',u'程序设计师',u'技术支持',u'品控员',u'文员'
          ,u'药物合成',u'专员',u'产品经理',u'顾问',u'软件工程师',u'视频制作',u'渠道拓展']
def getLink(url,proxy=''):
    time.sleep(3)
    start=time.clock()
    response=requests.get(url,proxies=proxy,headers={'Connection':'close'},timeout=10)
    print(time.clock()-start)
    s = requests.session()
    s.keep_alive = False
    response.encoding='utf8'
    bs=BeautifulSoup(response.text, "lxml")
    print(time.clock()-start)
    res=bs.find_all("div",{"class":"discuss-main clearfix"})
    print(time.clock()-start)
    links=[]
    print "res:"+str(len(res))
    for item in res:
        if 'discuss' in item.find('a').attrs['href']:
            links.append('https://www.nowcoder.com'+item.find('a').attrs['href'])
        else:
            links.append(item.find('a').attrs['href'])
    print "links:"+str(len(links))
    return links
def getInfo(url):
    #print url
    time.sleep(3)
    #request = urllib2.Request(url)
    response=requests.get(url,headers={'Connection':'close'},timeout=10)
    print "response=requests.get"
    s = requests.session()
    s.keep_alive = False
    response.encoding='utf8'
    bs=BeautifulSoup(response.text,"lxml")
    res=bs.find_all("div",{"class":"post-topic-main"})
    if(len(res)>0):
        res=bs.find_all("div",{"class":"post-topic-des"})
        data=u''
        for section in res:
            data=data+section.get_text()
    else:
        data=response.text
    #data = urllib2.urlopen(request).read()
    #data = request.urlopen(url).read()
    #data = data.decode('gbk')
    for word in keywords:
        if(data.find(word)>0):
            for notword in notwords:
                if(data.find(notword)>0):
                    return 0,0
            return word,bs.title.text
    return 0,0
        

errlink=""    
while(1): 
    itchat.auto_login(hotReload=True)
    users = itchat.search_friends(name=u'shao')
    userName = users[0]['UserName']
    #itchat.send('hello',toUserName = userName)
    old=pd.read_csv('job.csv',encoding='utf8',header=None)

    
    url_head='https://www.nowcoder.com/discuss?type=2&order=0&page='
    url_end=''
    for i in xrange(1,100):
        a=[]
        time.sleep(1)
        try:
            #print url
            links=getLink(url_head+str(i)+url_end)
            for link in links:
                errlink=link
                #print link
                if(len(old[old[0]==link])>0):
                    continue
                a.append(pd.DataFrame([link]))
                try:
                    word,title=getInfo(link)
                    if(word<>0):
                        itchat.send(word+":"+title+"\n"+link,toUserName = userName)  
                        print word
                        print link
                except:
                    print(errlink)
                    pd.DataFrame([[errlink,traceback.format_exc()]]).to_csv('error.csv',mode='a',header=None)
                    print('traceback.format_exc():\n%s' % traceback.format_exc())
                    continue
            if(len(a)>0):
                print(len(a))
                pd.concat(a).to_csv('job.csv',encoding='utf8',header=None,index=None,mode="a") 

        except:
            print(url_head+str(i)+url_end)
            if(len(a)>0):
                print(len(a))
                pd.concat(a).to_csv('job.csv',encoding='utf8',header=None,index=None,mode="a") 

            pd.DataFrame([[url_head+str(i)+url_end,traceback.format_exc()]]).to_csv('error.csv',mode='a',header=None)
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            continue
        print "over"
    time.sleep(60*60)
