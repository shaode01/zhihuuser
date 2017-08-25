import traceback
import pandas as pd
import time
import json
from selenium import webdriver
import random


def getfollowersbyurl(url):
    followers=[]
    is_end=False
    try:
        Chrome_login.get(url)
        pre=Chrome_login.find_element_by_tag_name("pre")
        json_str = json.loads(pre.text)
        if(json_str.has_key('error')):
            return "error","error"
        folls=json_str['data']
        fpage=json_str['paging']
        is_end=fpage['is_end']
 
        aaa=getuserid(folls)
        for i in aaa:
            followers.append(i)
        follpd=pd.DataFrame(followers) 
        follpd.to_csv("sgai.csv",mode='a',index=False,header=False)
    except Exception :
        print traceback.format_exc()
        pass
    return followers,is_end

def getfollowersbyuserid(userid,offset,sleepsecs):
    is_end=False
    followers=[]
    while(is_end==False):
        time.sleep(random.uniform(sleepsecs, 0))
        url="https://www.zhihu.com/api/v4/members/"+userid+"/followers?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset="+offset+"&limit=20"
        flist,is_end= getfollowersbyurl(url)
        if(flist=="error"):
            return "error"
        offset=str(int(offset)+20)
        followers +=flist
    return followers

#获取关注人列表中的全部关注者，每次最多显示20个
def getuserid(followerlist):
    for follower in followerlist:
        yield [follower['url_token'],follower['answer_count'],follower['articles_count'],follower['follower_count']]
#获取关注人列表中关注大于4000的关注者
def getuserid4000(followerlist):
    for follower in followerlist:
        if(follower["follower_count"]>4000):
            yield follower["url_token"]

#获取某个用户的全部follower
#开启一个chrome浏览器
Chrome_login=webdriver.Chrome()    
#然后手动登录一下知乎
##############################    
#获取某人的关注者，从offset开始，以random（2,0）间隔刷新 
getfollowersbyuserid(user_token,'32300',2)       
