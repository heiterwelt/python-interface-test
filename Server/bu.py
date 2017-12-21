
import requests
import json
import os
from bs4 import BeautifulSoup
import http.cookiejar as cookielib



class pic_spyder(object):
    
    
    def __init__(self,url,header,data,proxies):
        self.url=url
        self.headers=header
        self.data=data
        self.session=requests.session()
        self.proxies=proxies
    
    def connect_get(self):
        self.session.cookies=cookielib.LWPCookieJar(filename='pic_cookies')
        if not os.path.exists('pic_cookies'):
            self.r=self.session.get(self.url,headers=self.header,params=self.data)
            self.session.cookies.save(ignore_discard=True,ignore_expires=True)
        else:
            self.session.cookies.load(ignore_discard=True)
            print('cookies login')
            if(self.data == None):
                self.r=self.session.get(self.url,headers=self.headers)
            else:
                self.r=self.session.get(self.url,headers=self.headers,params=self.data)
            
#    return self.r


def get_data(self,r):
    self.soup=BeautifulSoup(r,'lxml')
    return self.soup


url='https://pixabay.com/zh/photos/?hp=&image_type=&cat=&min_width=&min_height=&q=%E8%87%AA%E7%84%B6%E9%A3%8E%E5%85%89&order=popular'
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}
proxies = {
    "http": "http://121.232.144.186:9000",
    "https": "http://121.232.144.186:9000"
    }
spyder=pic_spyder(url,header,None,proxies)
r=spyder.connect_get()
soup=spyder.get_data(r.text)
list=[d.get('data-lazy') for d in soup.select('img')[6:]]
print(list)
