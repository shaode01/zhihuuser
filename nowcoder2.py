# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 17:00:28 2017

@author: ZJ-ShaoDexin
"""
import traceback
import pandas as pd
import time
from selenium import webdriver
import itchat
keywords=[u'机器学习',u'数据挖掘',u'聚类',u'贝叶斯',u'马尔科夫',u'SVM',
          u'支持向量机',u'关联规则',u'神经网络',u'Hadoop',u'线性回归',u'逻辑斯蒂回归',u'统计回归',
          u'决策树',u'深度学习',u'回归模型',
          u'模式识别',u'预测',u'时间序列',u'图方法',u'协同过滤',u'深度学习',]
notwords=[u'文案撰写',u'图像识别',u'语音识别',u'视频识别',u'文书管理',u'助理',u'记者'
          ,u'教育培训',u'日语岗位',u'行业分析',u'业务拓展',u'主管',u'前台',u'销售',u'给排水',u'媒介策划'
          ,u'网络运营',u'电话访问员',u'中专',u'程序设计师',u'技术支持',u'品控员',u'文员'
          ,u'药物合成',u'专员',u'产品经理',u'顾问',u'软件工程师',u'视频制作',u'渠道拓展']
print "begin"
itchat.auto_login(hotReload=True, statusStorageDir='shao.pkl')
users = itchat.search_friends(name=u'一步')
userName = users[0]['UserName']

def getLink(url,proxy=''):
    start=time.clock()
    Chrome_login.get(url)
    links=[]
    for tag in Chrome_login.find_elements_by_class_name('discuss-main'):
        link=tag.find_element_by_tag_name("a").get_attribute('href')
        if 'discuss' in link:
            links.append(link.split('?')[0])
        else:
            links.append(link)   
    print(u"耗时"+str(time.clock()-start)+u"秒")
    print u"返回links:"+str(len(links))+u"个"
    return links
def getInfo(url):
    start=time.clock()
    Chrome_login.get(url)
    try:
        data=Chrome_login.find_element_by_class_name('post-topic-des').text                                            
    except:
        data=u''
    try:
        title=Chrome_login.find_element_by_class_name('crumbs-end').text
    except:
        title=u''                                                 
    print time.strftime('%H:%M:%S',time.localtime(time.time()))+" url:"+url+" 耗时"+str(time.clock()-start)+"秒"
  

    for word in keywords:
        if(data.find(word)>0):
            for notword in notwords:
                if(data.find(notword)>0):
                    return 0,0
            return word,title
    return 0,0
        
def srchandsend(userName):
    old=pd.read_csv('job.csv',encoding='utf8',header=None)
    url_head='https://www.nowcoder.com/discuss?type=2&order=0&page='
    url_end=''
    for i in xrange(1,100):
        a=[]
        target=[]
        try:
            links=getLink(url_head+str(i)+url_end)
            for link in links:
                errlink=link
                if(len(old[old[0]==link])>0):
                    continue
                a.append(pd.DataFrame([link]))
                try:
                    word,title=getInfo(link)
                    if(word<>0):
                        itchat.send(word+":"+title+"\n"+link,toUserName = userName)  
                        target.append(pd.DataFrame([word,link]))
                        print word
                        print link
                except:
                    print(errlink)
                    pd.DataFrame([[errlink,traceback.format_exc()]]).to_csv('error.csv',mode='a',header=None)
                    print('traceback.format_exc():\n%s' % traceback.format_exc())
                    continue
            if(len(a)>0):
                print(u"新增链接"+str(len(a))+u"个")
                pd.concat(a).to_csv('job.csv',encoding='utf8',header=None,index=None,mode="a") 
            if(len(target)>0):
                print(u"新增目标链接"+str(len(target))+u"个")
                pd.concat(target).to_csv('target.csv',encoding='utf8',header=None,index=None,mode="a") 

        except:
            print(url_head+str(i)+url_end)
            if(len(a)>0):
                print(len(a))
                pd.concat(a).to_csv('job.csv',encoding='utf8',header=None,index=None,mode="a") 

            pd.DataFrame([[url_head+str(i)+url_end,traceback.format_exc()]]).to_csv('error.csv',mode='a',header=None)
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            continue
        print "over"

Chrome_login=webdriver.Chrome()  
srchandsend(userName)
