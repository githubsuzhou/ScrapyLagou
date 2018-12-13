# -*- coding: utf-8 -*-
import scrapy


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    def parse(self, response):
        #爬取西刺代理
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }

        # 遍历2000页的数据
        for i in range(200):
            response = requests.get('http://www.xicidaili.com/nn/{0}'.format(i), headers=headers)
            # 获取selector用来解析网页内容
            selector = Selector(text=response.text)
            all_trs = selector.css('#ip_list tr')
            ip_list = []
            # all_trs[1:]去除表头
            for tr in all_trs[1:]:
                speed = tr.css('.bar::attr(title)').extract()[0]
                if speed:
                    speed = float(speed.split('秒')[0])

                all_text = tr.css('td::text').extract()

                ip = all_text[0]
                port = all_text[1]
                proxy_type = all_text[5]

                ip_list.append((ip, port, proxy_type, speed))

                print(ip_list)
