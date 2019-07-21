# -*- coding: utf-8 -*-
import scrapy
import queue
from lxml import etree
import json
import hashlib
import time


def pd_file(num):
    with open('pd.txt', 'w') as f:
        f.write(num)


class YmxSpider(scrapy.Spider):
    name = 'ymx'
    allowed_domains = ['amazon.com/dp']
    start_urls = ['http://amazon.com/dp']
    # 使用代理，由于不能解决503问题，因此没有使用代理
    # orderno = "ZF201811120134l65nvw"
    # secret = "c15cbd29996f422ea82f43d9bdfe1af5"
    # ip_port = 'forward.xdaili.cn:80'

    def start_requests(self):
        # timestamp = str(int(time.time()))  # 计算时间戳
        # string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        # sign = hashlib.md5(string.encode("utf-8")).hexdigest().upper()  # 计算sign
        # auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        # proxy = 'http://' + str(self.ip_port)
        # headers = {"Proxy-Authorization": auth,
        #            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        cookies = {
            'cookie': 'session-id=130-2997722-7948128; session-id-time=2082787201l; i18n-prefs=USD; lc-main=en_US; sp-cdn="L5Z9:CN"; ubid-main=130-8666230-2258832; x-wl-uid=1j1rz7TyMT2curgMLhcBvKTMvctUEyIqUIj2ZMoSK+qUx0f7RruU1q3h80fexiY8cy2IhyB5EI+8=; session-token=snS3S2F13F1Kb0K94UnbnxFMVgzRU4WpjkehX/ueDOGD6R/MZd8ujDBdisIn3utnT+yvgpsiwSCy2mAEAn56VWg3iLHp/bR1wRr+JBmomEJDg/PypaTRSIroGgutnC3WHVQGXLb2aYqmZafZFM2elnAEW2o9pQvAvBYTW/v7AuH89alU9D88JyccTsO4fWmH; csm-hit=tb:5K87E6A67VHKAV70XK5P+s-5K87E6A67VHKAV70XK5P|1563259023909&t:1563259023909&adb:adblk_no'
        }
        # 读取文档信息，存为队列中
        lines = queue.Queue()
        f = open('asins.txt')
        # 中断恢复判断，当存在编号时，读取该编号
        with open('pd.txt', 'r') as q:
            pd = q.readline()
        # 判断编号为空时，则从头开始，若不为空，则读到与原文档的编号相同时停止
        while True:
            if pd == '':
                break
            line = f.readline()
            if pd == line.split('\n')[0]:
                break
        # 读取原文档编号，并存到队列中
        while True:
            line = f.readline()
            lines.put(line)
            if len(line) == 0:
                break
        # 判断队列不为空时，一直访问url，并保存目前到的编号的信息
        while not lines.empty():
            a = lines.get()
            a = a.split('\n')[0]
            pd_file(a)
            yield scrapy.Request(url='http://amazon.com/dp/{}'.format(a), method='POST', cookies=cookies, callback=self.parse, meta={'asin': a, })

    def parse(self, response):
        html = etree.HTML(response.text)
        a = response.meta.get('asin')
        temp = html.xpath('//title/text()')
        # 保存json文件
        if temp:
            dict_temp = {'asin': a, 'title': temp[0]}
            with open('js.json', 'a') as f:
                f.write(json.dumps(dict_temp))
                f.write('\n')
        else:
            pass
