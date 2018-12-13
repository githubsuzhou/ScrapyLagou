# -*- coding: utf-8 -*-
import scrapy
import scrapy,time,random,json
from lagou.items import LagouItem
class WorkSpider(scrapy.Spider):
    name = 'work'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']
    page = 1
    kds = [u'java',u'python',u'php',u'android','c++',u'vb',u'ios',u'搜索算法',u'爬虫工程师']
    curo=0 #相当于游标吧
    kd=kds[0]
    #语言名称头
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en',
         'Cookie':'user_trace_token=20180913190730-e55b6bbf-bdb3-4f56-9210-d9a3d06c5319; LGUID=20180913190732-361bfeaf-b745-11e8-95ff-525400f775ce;'
                 ' JSESSIONID=ABAAABAAAIAACBIBD05FD4670CFFBA57AAC238C6CFF0D47; TG-TRACK-CODE=search_code; _gid=GA1.2.1738173782.1536836852; '
                 '_ga=GA1.2.1201569471.1536836852; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536836852; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536848719;'
                 ' LGSID=20180913213756-38e5a2b7-b75a-11e8-960c-525400f775ce; LGRID=20180913222519-d789991a-b760-11e8-b815-5254005c3644;'
                 ' SEARCH_ID=611a7601ceec47059ec6b121c636b2a2',
        'Host':'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_java?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': ' XMLHttpRequest',
    }
    # custom_settings = {
    #     "DEFAULT_REQUEST_HEADERS": {
    #         'Accept': 'application/json, text/javascript, */*; q=0.01',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',            'Host': 'www.lagou.com',
    #         'Origin': 'https://www.lagou.com',
    #         'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?px=default&city=%E5%85%A8%E5%9B%BD',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    #         'X-Anit-Forge-Code': '0',
    #         'X-Anit-Forge-Token': 'None',
    #         'X-Requested-With': 'XMLHttpRequest'
    #     },
    #     "ITEM_PIPELINES": {
    #         'lagou.pipelines.LagouPipeline': 300
    #     }
    # }
    url='https://www.lagou.com/jobs/positionAjax.json?'
    #  参数  dont_filter=False  去重
    def start_requests(self):
        yield scrapy.FormRequest(url=self.url, headers=self.header,
                                 formdata={
                                     'px':'default',
                                     'needAddtionalResult': 'false',
                                     'city':'全国',
                                     'first': 'true',
                                     'pn': str(self.page),
                                     'kd': self.kd
                                 }, callback=self.parse,dont_filter=False
                                  )
    def parse(self, response):
        # print(response.text)
        data = json.loads(response.text)
        results = data['content']['positionResult']['result']  # 职位信息
        for m in results:
            item = LagouItem()
            item['Name'] = m['positionName']
            #将薪资核算为平均值
            s= m['salary']
            s=s.split('-')
            #计算出平均值
            if len(s)==1:
                smax=int(s[0][:s[0].find('k')])
            else:
                smax=int(s[1][:s[1].find('k')])
            smin=int(s[0][:s[0].find('k')])
            s_avg=(smin+smax)/2
            # print(type(s_avg))
            # print("薪资%s"%s_avg)
            item['salary'] = s_avg   #将平均值写入
            item['creat_time'] = m['createTime']
            item['working_years'] = m['workYear']
            item['education'] = m['education']
            item['company'] = m['companyFullName']
            # num=m['positionId']  # https://www.lagou.com/jobs/4976033.html 获取到的是4976033
            #item['yaoqiu'] = 'https://www.lagou.com/jobs/%s.html' % m['positionId']  # 获取到的真实网址
            item['city'] = m['city']
            item['welfare'] = m['positionAdvantage']
            print("=========%s"% item['Name'])
            # print("=========%s"% item['creat_time'])
            yield item


        if self.page < 30: #一共30頁
            first= 'true' if self.page == 1 else 'false'
            self.page += 1
            time.sleep(random.randint(1,6))
            print('正在请求第%s页' % self.page)
            if self.page % 5 == 0:
                time.sleep(random.randint(1,5))  # 爬取5页数据之后会被禁止
            yield scrapy.FormRequest(self.url, headers=self.header,
                                     formdata={
                                         'px':'default',
                                         'needAddtionalResult': 'false',
                                         'city':'全国',
                                         'first': 'first',
                                         'pn': str(self.page),
                                         'kd': self.kd,
                                     }, callback=self.parse,dont_filter=False
                                     )
        # elif self.page2<len(self.kds)-1:
        #     self.page=1
        #     self.curo+=1
        #     self.kd=self.kds[self.curo]
        #     yield  scrapy.FormRequest(self.url,formdata={
        #                                  'px':'default',
        #                                  'needAddtionalResult': 'false',
        #                                  'city':'全国',
        #                                  'first': 'true',
        #                                  'pn': str(self.page),
        #                                  'kd': self.kd,
        # },callback=self.parse,dont_filter=False)

