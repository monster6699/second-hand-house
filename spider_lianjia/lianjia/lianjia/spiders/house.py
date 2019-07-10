# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import re
import time
import scrapy
from redis import StrictRedis
from scrapy_redis.spiders import RedisSpider
import redis
from datetime import datetime


class HouseSpider(RedisSpider):
    name = 'house'
    # allowed_domains = ['bj.lianjia.com']
    # start_urls = ['https://bj.lianjia.com/ershoufang/']
    redis_key = 'start_url'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(HouseSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        datas = response.xpath('//div[@class="info clear"]')

        for data in datas:
            data_dict={
                'selectData':[],
            }

            data_dict['title'] = data.xpath('./div[@class="title"]/a/text()').extract_first()
            data_dict['url'] = data.xpath('./div[@class="title"]/a/@href').extract_first()
            focus= data.xpath('./div[@class="followInfo"]/text()').extract_first().split('/')[0]
            vide = data.xpath('./div[@class="followInfo"]/text()').extract_first().split('/')[1]
            # area = data.xpath('.//div[@class="houseInfo"]/text()[2]').extract_first()
            houseYear = data.xpath('.//div[@class="positionInfo"]/text()[2]').extract_first()
            data_dict['buil_year']=houseYear

            data_dict['vide']=  int(re.findall(r'\d+',vide)[0])
            data_dict['focus'] = int(re.findall(r'\d+',focus)[0])

            yield scrapy.Request(url=data_dict['url'],callback=self.parse_detail,meta=data_dict)

        con = StrictRedis(host='192.168.177.138',port=6379,db=1)
        page = con.get("page")
        page = int(page.decode())

        if(page<100):
            time.sleep(1)
            next_url="https://zz.lianjia.com/ershoufang/pg{}/".format(page)
            print("++++++++++++++++++++%s+++++++++++++++"%next_url)
            page = page+1
            con.set("page",page)
            yield scrapy.Request(url=next_url,callback=self.parse)
        else:
            con.set("num",1)

    def parse_detail(self,response):
        introductions = response.xpath('//*[@id="introduction"]//div[@class="content"]')
        data_dict=response.meta
        data_list=[]
        basc_attr = introductions[0].xpath('./ul/li')
        house_type = basc_attr[0].xpath('./text()').extract_first()
        floor = basc_attr[1].xpath('./text()').extract_first()
        area = basc_attr[2].xpath('./text()').extract_first()
        structure = basc_attr[3].xpath('./text()').extract_first()
        in_area = basc_attr[4].xpath('./text()').extract_first()
        build_type = basc_attr[5].xpath('./text()').extract_first()
        build_head = basc_attr[6].xpath('./text()').extract_first()
        build_struct = basc_attr[7].xpath('./text()').extract_first()
        decorate = basc_attr[8].xpath('./text()').extract_first()
        ladder_hou_pro = basc_attr[9].xpath('./text()').extract_first()
        heat_method = basc_attr[10].xpath('./text()').extract_first()
        lift = basc_attr[11].xpath('./text()').extract_first()
        period_int = basc_attr[12].xpath('./text()').extract_first()#产权年限
        address_wu = response.xpath('/html//div[@class="communityName"]//a[1]/text()').extract_first()
        address_qu = response.xpath('/html//span[@class="info"]/a[1]/text()').extract_first()
        address_detail = response.xpath('/html//span[@class="info"]/a[2]/text()').extract_first()

        basc_dict={
            "house_type":house_type,
            "floor":floor,
            "area":area,
            "structure":structure,
            "in_area":in_area,
            "build_type":build_type,
            "build_head":build_head,
            "build_struct":build_struct,
            "decorate":decorate,
            "ladder_hou_pro":ladder_hou_pro,
            "heat_method":heat_method,
            "lift":lift,
            "period_int":period_int,
            "address_wu":address_wu,
            "address_qu":address_qu,
            "address_detail":address_detail,


        }
        data_list.append(basc_dict)



        attr = introductions[1].xpath('./ul/li//span[2]')
        # print(len(attr))
        listed_time = attr[0].xpath('./text()').extract_first()
        trade_ownership = attr[1].xpath('./text()').extract_first()
        last_transation_time = attr[2].xpath('./text()').extract_first()
        house_use = attr[3].xpath('./text()').extract_first()
        house_year = attr[4].xpath('./text()').extract_first()
        belong_to = attr[5].xpath('./text()').extract_first()
        mortgage_info = attr[6].xpath('./text()').extract_first()
        room_bak = attr[7].xpath('./text()').extract_first()
        trade_dict={
            "listed_time":listed_time,
            "trade_ownership":trade_ownership,
            "last_transation_time":last_transation_time,
            "house_use":house_use,
            "house_year":house_year,
            "belong_to":belong_to,
            "mortgage_info":mortgage_info.strip(),
            "room_bak":room_bak,
        }
        data_list.append(trade_dict)
        data_dict['base_info'] = data_list

        houses = response.xpath('//div[@class="introContent showbasemore"]//div[@class="content"]')
        # houses = response.xpath('//div[@class="introContent showbasemore"]/div')

        tags= houses[0].xpath('./a/text()')
        tag_list=[]
        charact_dict={}
        for tag in tags:
            tag_list.append(tag.extract())
        houses = response.xpath('//div[@class="introContent showbasemore"]/div[@class="baseattribute clear"]')
        for house in houses:
            name = house.xpath("./div[@class='name']/text()").extract_first()
            content = house.xpath("./div[@class='content']/text()").extract_first()
            name = name.strip()
            content = content.strip()
            charact_dict[name]=content

        data_dict['tag']=tag_list


        data_dict['house_charact'] =charact_dict

        images = response.xpath('/html/body//div[@class="container"]/div[@class="list"]//img')
        image_dict = {}
        if images:
            for image in images:
                image_url = image.xpath('./@src').extract_first()
                image_alt = image.xpath('./@alt').extract_first()
                image_dict[image_alt]=image_url
        else:
            image_dict['照片正在拍摄中'] ='https://s1.ljcdn.com/feroot/pc/asset/img/blank.gif?_v=20190418174907'
        data_dict['images']=image_dict


        data_dict['price'] = int(response.xpath('/html/body//span[@class="total"]/text()').extract_first())
        data_dict['unit_price'] = response.xpath('/html/body//span[@class="unitPriceValue"]/text()').extract_first()
        data_dict['source'] = "链家"


        price = int(data_dict['price'])
        print("===========================================")
        print(price)
        price_in = '暂无数据'
        if price <200:
            price_in='200万以下'
            print("=================200万以下==========================")
        elif price>=200 and price<250:
            price_in='200-250万'
            print("=================200-250==========================")
        elif price >= 250 and price < 300:
            price_in = '250-300万'
            print("=================250-300万==========================")
        elif price >= 300 and price < 400:
            price_in = '300-400万'
            print("=================300-400==========================")
        elif price >= 400 and price < 500:
            price_in = '400-500万'
            print("=================400-500万==========================")
        elif price >= 500 and price < 800:
            price_in = '500-800万'
            print("=================500-800万==========================")


        # print(area.replace('平方',''))
        area = int(int(re.findall(r'\d+',area)[0]))
        data_dict['area']=area
        if area <50:
            area_in='50平以下'
        elif area>=50 and area<70:
            area_in='50-70平'
        elif area >= 70 and area < 90:
            area_in = '70-90平'
        elif area >= 90 and area < 110:
            area_in = '90-110平'
        elif area >= 110 and area < 130:
            area_in = '110-130平'
        else:
            area_in = '130-150平'
        buildYear=data_dict['buil_year']
        print("---------------------------------------------------------------")
        if buildYear:
            buildYear = int(re.findall(r'\d+',buildYear)[0])
            date_now = datetime.now()
            buildYear = date_now.year-buildYear
            if buildYear < 5:
                buildYear = '5年以下'
            elif buildYear >= 5  and  buildYear < 10:
                buildYear = '10年以内'
            elif buildYear >= 10  and  buildYear < 15:
                buildYear = '15年以内'
            elif buildYear >= 15  and  buildYear < 20:
                buildYear = '20年以内'
            else:
                buildYear = '20年以上'
        else:
            buildYear='暂无数据'
        house_type = house_type[:4]
        vide = data_dict['vide']
        data_dict['selectData']=[address_wu,address_qu,address_detail,vide,price,house_type,area,tag_list,build_head,floor,buildYear,decorate,house_use,lift,heat_method,trade_ownership,build_type]
        print(data_dict['selectData'])
        data_dict['conData']=address_wu+address_qu+address_detail+price_in+house_type+area_in+str(tag_list)+build_head+floor+buildYear+decorate+house_use+lift+heat_method+trade_ownership+build_type
        yield data_dict
