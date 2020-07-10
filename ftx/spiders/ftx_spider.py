# -*- coding: utf-8 -*-
import scrapy
import re
from ftx.items import NewhouseItem, EsfItem

class FtxSpiderSpider(scrapy.Spider):
    name = 'ftx_spider'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@id='c02']/table//tr")
        province = None
        for tr in trs:
            province_text = tr.xpath(".//td[2]//text()").extract_first()
            province_text = re.sub(r'\s', '', province_text)
            if province_text == '其它':
                continue
            if province_text:
                province = province_text
            city_tds = tr.xpath(".//td[3]/a")
            for city_td in city_tds:
                city = city_td.xpath("./text()").extract_first()
                city_url = city_td.xpath("./@href").extract_first()
                city_py = re.findall(r'.//(.*?)\.', city_url)[0]
                wrong_urls = ['mengcheng', 'leizhou', 'daye', 'anlu', 'sihong', 'hk',
                              'guangde', 'esf', 'sxly'
                              ]
                if city_py not in wrong_urls:
                    newhouse_link = 'https://{}.newhouse.fang.com/house/s/'.format(city_py)
                    esf_link = 'https://{}.esf.fang.com/'.format(city_py)


                    try:

                        yield scrapy.Request(url=newhouse_link, callback=self.parse_newhouse,
                                             meta={'info': (province, city)})
                        yield scrapy.Request(url=esf_link, callback=self.parse_esf,
                                             meta={'info': (province, city)})
                    except:
                        pass

    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        uls = response.xpath("//div[@class='nlc_details']")
        for ul in uls:
            address = ul.xpath(".//div[@class='address']/a/@title").extract_first()
            name = ul.xpath(".//div[@class='nlcd_name']/a//text()").get().strip()
            loupan_url = 'https:' + ul.xpath(".//div[@class='nlcd_name']/a/@href").get()
            type = ''.join(ul.xpath(".//div[@class='house_type clearfix']//text()").getall())
            type = re.sub(r'\s', '', type).split('－')
            try:
                rooms = type[0]
                square = type[1]
            except IndexError:
                pass
            else:
                price = ''.join(ul.xpath(".//div[@class='nhouse_price']//text()").getall())
                price = re.sub(r'\s', '', price)
                sale = ul.xpath(".//span[@class='inSale']/text()").get()
                number = ''.join(ul.xpath(".//div[@class='tel']/p//text()").getall())
                item = NewhouseItem(province=province, city=city, name=name, address=address, rooms=rooms,
                                    square=square, price=price, sale=sale, loupan_url=loupan_url, number=number)
                print(item)
                yield item

        next_page = response.xpath("//li[@class='fr']//a[last()-1]/@href").get()
        if next_page:
            print(response.urljoin(next_page))
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_newhouse,
                                 meta={'info':(province,city)})




    def parse_esf(self, response):
        province, city = response.meta.get('info')
        dds = response.xpath("//div[@class='shop_list shop_list_4']//dl")
        for dd in dds:
            name = dd.xpath(".//p[@class='add_shop']/a/@title").get()
            address = dd.xpath(".//p[@class='add_shop']/span/text()").get()
            info = ''.join(dd.xpath(".//p[@class='tel_shop']//text()").getall())
            info = re.sub(r'\s', '', info).split('|')
            try:
                rooms = info[0]
                area = info[1]
                floor = info[2]
                toward = info[3]
                build = info[4]
            except IndexError:
                pass
            else:
                # print(rooms,area,floor,toward,build)
                price = ''.join(dd.xpath(".//dd[@class='price_right']/span[1]//text()").getall())
                price = re.sub(r'\s', '', price)
                union = dd.xpath(".//dd[@class='price_right']/span[2]/text()").get()
                item = EsfItem(province=province, city=city, name=name, address=address, rooms=rooms, area=area,
                               floor=floor, toward=toward, build=build, price=price, union=union)
                print(item)
                yield item

        next_page = response.xpath("//div[@class='page_al']//p[1]/a/@href").get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_esf,
                                 meta={'info':(province,city)})

