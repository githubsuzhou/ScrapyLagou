# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  pymysql,json
from scrapy.conf import settings

class LagouPipeline(object):
    def process_item(self, item, spider):
        char=settings['CHARSET']
        host = settings['MYSQL_HOST']
        psd = settings['MYSQL_PASSWD']
        db = settings['MYSQL_DBNAME']
        user= settings['MYSQL_USER']
        port=settings['MYSQL_PORT']
        #数据库连接
        con=pymysql.connect(host=host,user=user,passwd=psd,db=db,charset=char,port=port)
        #数据库游标
        cue=con.cursor()
        print("mysql connect succes")#测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        try:
            # cue.execute("insert into jobs (name,working_years,salary,education,company,city,welfare,create_time)values(%s,%s,%s,%s,%s,%s,%s,%s)",[ item['name'],item['working_years'],
            #               item['salary'],item['education'],item['company'] ,item['city'],item['welfare'],item['create_time']])
            cue.execute("insert into jobs (Name,working_years,salary,education,company,city,welfare,creat_time)values(%s,%s,%s,%s,%s,%s,%s,%s)",[ item['Name'],item['working_years'],
                         item['salary'],item['education'],item['company'] ,item['city'],item['welfare'],item['creat_time'] ])
            print("insert success")#测试语句
        except Exception as e:
                print('Insert error:',e)
                con.rollback()
        else:
                con.commit()
                con.close()
                return  item