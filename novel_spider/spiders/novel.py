# -*- coding: utf-8 -*-
import copy
import os
import re
import scrapy
from ..items import NovelSpiderItem,NovelImgItem,NovelCategoryItem,NovelChapterAndContentItem

class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['bxwx8.la']
    start_urls = ['http://www.bxwx8.la/btopallvisit/0/1.html']

    def parse(self,response):
        print('*****开始爬取****')
        item = NovelSpiderItem()

        txt_urls = response.xpath("//table[@class='grid']//tr/td[1]/a/@href").getall()
        for txt_url in txt_urls:
            item['txt_url'] = txt_url
            yield scrapy.Request(url=item['txt_url'], callback=self.novel_info,meta={'item': copy.deepcopy(item)})


        next_url = response.xpath("//div[@id='pagelink']/a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=next_url,callback=self.parse)


    def novel_info(self,response):
        item = response.meta['item']

        item_Img = NovelImgItem()
        item_Category = NovelCategoryItem()

        print('*****正在爬取小说详情页*****')

        txt_name = response.xpath("//*[@id='centerm']/table[1]//tr/td/table[2]//tr/td/font/strong/text()").get().split('全集下载')[0]
        txt_category = response.xpath("//div[@id='centerm']/table[1]//tr/td/table[3]//tr/td/table[1]//tr/td[2]/table//tr[1]/td[2]/a/text()").get()
        txt_author = response.xpath("//div[@id='centerm']/table[1]//tr/td/table[3]//tr/td/table[1]//tr/td[2]/table//tr[1]/td[4]/a/text()").get()
        txt_words = response.xpath("//div[@id='centerm']/table[1]//tr/td/table[3]//tr/td/table[1]//tr/td[2]/table//tr[3]/td[4]/text()").get()
        txt_date = response.xpath("//div[@id='centerm']/table[1]//tr/td/table[3]//tr/td/table[1]//tr/td[2]/table//tr[3]/td[6]/text()").get()
        txt_status = response.xpath("//div[@id='centerm']/table[1]//tr/td/table[3]//tr/td/table[1]//tr/td[2]/table//tr[2]/td[6]/text()").get()

        item['txt_name'] = txt_name
        item['txt_category'] = txt_category
        item_Category['txt_category'] = txt_category

        item['txt_author'] = txt_author
        item['txt_words'] = txt_words
        item['txt_date'] = txt_date
        item['txt_status'] = txt_status



        # 爬取每本小说下载链接 存入变量txt_download_url
        txt_download_url = re.findall('mydownurl="(http:.*)"', response.text)[0]

        # 获取每本小说简介
        content = response.xpath("//div[@align='left']/text()").getall()

        txt_content = ''.join(content)[12:-12]

        # 获取每本小说图片链接
        txt_img_url = response.xpath("//img[@class='picborder']/@src").get()


        item_Img['txt_name'] = txt_name
        # item_Img['txt_img_url'] = []
        item_Img['txt_img_url'] = txt_img_url

        # 获取每本小说 阅读链接和封面链接
        item['txt_download_url'] = txt_download_url
        item['txt_content'] = txt_content

        txt_read_button = response.xpath("//div[@id='centerm']/table[1]//tr/td/table[3]//tr/td/table[1]//tr/td[1]/table//tr/td/a/@href").get()

        yield scrapy.Request(url=txt_read_button, callback=self.novel_chapter,meta={'item': copy.deepcopy(item), 'txt_read_button': txt_read_button})
        yield item_Img
        yield item_Category


    def novel_chapter(self,response):
        item = response.meta['item']
        print('*****正在爬取小说章节页*****')

        txt_read_button = response.meta['txt_read_button']

        read_urls = response.xpath("//div[@id='TabCss']/dl/dd/a/@href").getall()

        item['txt_chapter'] = len(read_urls)

        txt_read_url = txt_read_button.split('index')[0]

        for read_url in read_urls:
            chapter_url = txt_read_url + read_url
            yield scrapy.Request(url=chapter_url,callback=self.novel_chapter_content,meta={'txt_name':item['txt_name'],'txt_author':item['txt_author']})

        yield item

    def novel_chapter_content(self,response):
        item_Chapter_Content = NovelChapterAndContentItem()

        txt_name = response.meta['txt_name']
        txt_author = response.meta['txt_author']

        read_title = response.xpath("//div[@id = 'title']/text()").get()
        new_title = read_title.strip()

        item_Chapter_Content['txt_name'] = txt_name
        item_Chapter_Content['txt_author'] = txt_author
        item_Chapter_Content['txt_chapter_name'] = new_title

        txt_content = response.xpath("//div[@id='content']/text()").getall()
        new_content = []
        for str in txt_content:
            new_content.append(str.strip())

        content = ''.join(new_content)
        content = content.replace("'",'"')

        item_Chapter_Content['txt_chapter_content'] = content

        yield item_Chapter_Content




















