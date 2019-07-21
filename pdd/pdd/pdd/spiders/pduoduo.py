# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import time
import hashlib



class PduoduoSpider(scrapy.Spider):
    name = 'pduoduo'
    allowed_domains = ['pinduoduo.com']
    start_urls = ['http://mobile.yangkeduo.com']
    orderno = "ZF201811120134l65nvw"
    secret = "c15cbd29996f422ea82f43d9bdfe1af5"
    ip_port = 'forward.xdaili.cn:80'

    def start_requests(self):
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        sign = hashlib.md5(string.encode("utf-8")).hexdigest().upper()  # 计算sign
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        proxy = 'http://' + str(self.ip_port)
        headers = {#"Proxy-Authorization": auth,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        cookie = {'cookie':'api_uid=rBUGXl0z5mkC1nbfTyN/Ag==; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20WOW64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F63.0.3239.132%20Safari%2F537.36; _nano_fp=XpdjXqEJn0PylpTonT_qDsBp3Nc~0sNlrdA294s3; webp=1; rec_list_index=rec_list_index_hM04uu; JSESSIONID=1B35A16E51F18F2336C50C89F13B35F3'}
        a = input('输入关键字：')
        url = 'http://mobile.yangkeduo.com/search_result.html?search_key={}&search_src=new&search_met=btn_sort&search_met_track=manual&refer_page_name=search&refer_page_id=10031_1563684436444_D0KaFQBJzY&refer_page_sn=10031'.format(a)
        yield scrapy.Request(url=url, method='POST', headers=headers, cookies=cookie, callback=self.parse, meta={'proxy': proxy})

    def parse(self, response):
        print()
        print(response.url)
        print()
