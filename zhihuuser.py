import traceback
import pandas as pd
import requests
import itchat
import time
from bs4 import BeautifulSoup
import csv
import json
import urllib2
import gzip
from StringIO import StringIO
import zlib
import sys
from selenium import webdriver

reload(sys) 
sys.setdefaultencoding( "utf-8" ) 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'Accept-Encoding':'gzip'      } 

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'authorization':'Bearer 2|1:0|10:1501462090|4:z_c0|92:Mi4wQUFDQW9mOGpBQUFBWUVKY0xpS3BDeWNBQUFDRUFsVk5TZ3VtV1FCbFR2MEJhZV85NW9HY210b05SQWt1bjJDT0Zn|0d8d053b9cd64acb04a5a5c37da67ab0649d3d172677057cb2fc1422b812c4b9',
    'Accept-Encoding':'gzip'  ,
    'Connection':'keep-alive' ,
    'X-UDID':'AGBCXC4iqQuPTj7aQR5C9CR1laWyFAQZwGk='} 

def getinfobyuserid(userid):
    url="https://www.zhihu.com/api/v4/members/"+userid+"?include=locations,business,voteup_count,thanked_count,follower_count,favorited_count"
    r=requests.get(url,headers=headers)
    r.encoding='gbk'
    json_str = r.json()
    #print json_str
    result=[]
    result.append(json_str['url_token'])
    result.append(json_str['voteup_count'])
    result.append(json_str['thanked_count'])
    result.append(json_str['follower_count'])
    result.append(json_str['favorited_count'])
    if(json_str.has_key("business")):
        result.append(json_str['business']['name'])
    else:
        result.append(0)
    if(json_str.has_key("locations")):
        if(len(json_str['locations'])>0):
            result.append(json_str['locations'][0]['name'])
        else:
            result.append(0)
    else:
        result.append(0)
    return result
def getfollowers(userid,offset):
    url="https://www.zhihu.com/api/v4/members/"+userid+"/followees?offset="+offset+"&limit=20"
    url="https://www.zhihu.com/api/v4/members/"+userid+"/followers?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset="+offset+"&limit=20"
    r=requests.get(url,headers=headers)
    r.encoding='gbk'
    json_str = r.json()
    return json_str

def loadData(userid):
    url="https://www.zhihu.com/api/v4/members/"+userid+"?include=locations,business,voteup_count,thanked_count,follower_count,favorited_count"
    send_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'Accept-Encoding':'gzip'      } 
    request = urllib2.Request(url,headers=send_headers)
    response = urllib2.urlopen(request)
    content = response.read()
    encoding = response.info().get('Content-Encoding')
    if encoding == 'gzip':
        content = gzipp(content)
    elif encoding == 'deflate':
        content = deflate(content)
    return content

def gzipp(data):
    buf = StringIO(data)
    f = gzip.GzipFile(fileobj=buf)
    return f.read()

def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)

def main(userid):
    content = loadData(userid)
    print content
def getuserid(followerlist):
    for follower in followerlist:
        if(follower["follower_count"]>4000):
            yield follower["url_token"]
def usercsv(userid,offset):
    foll=getfollowers(userid,offset)
    folls=foll['data']
    followers=[]
    aaa=getuserid(folls)
    for i in aaa:
        followers.append(i)
    followerinfo=[]    
    for follower in followers:
        followerinfo.append(getinfobyuserid(follower))
        print time.strftime('%H:%M:%S',time.localtime(time.time()))
        time.sleep(2)
    follpd=pd.DataFrame(followerinfo)  
    print len(follpd)
    #follpd.columns=['name',u'获得的赞同',u'获得的感谢',u'关注者',u'回答被收藏',u'从事行业',u'居住地']
    if(len(followerinfo)>0):
        follpd.to_csv("user.csv",mode='a',index=False,header=False)

def usercsv_selenium(userid,offset):
    Chrome_login.get('https://www.zhihu.com/api/v4/members/qing-shi-yong-zhen-shi-xing-ming/followees?offset=0&limit=20')    
    pre=Chrome_login.find_element_by_tag_name("pre")
    prejson=json.loads(pre.text)
    folls=prejson['data']
    followers=[]
    aaa=getuserid(folls)
    for i in aaa:
        followers.append(i)
    followerinfo=[]    
    for follower in followers:
        followerinfo.append(getinfobyuserid(follower))
        print time.strftime('%H:%M:%S',time.localtime(time.time()))
        time.sleep(2)
    follpd=pd.DataFrame(followerinfo)  
    print len(follpd)
    #follpd.columns=['name',u'获得的赞同',u'获得的感谢',u'关注者',u'回答被收藏',u'从事行业',u'居住地']
    if(len(followerinfo)>0):
        follpd.to_csv("user.csv",mode='a',index=False,header=False)
