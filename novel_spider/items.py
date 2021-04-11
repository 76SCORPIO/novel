# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NovelSpiderItem(scrapy.Item):
    # 小说名
    txt_name = scrapy.Field()
    #小说类别
    txt_category = scrapy.Field()
    # 作者
    txt_author = scrapy.Field()
    # 小说字数
    txt_words = scrapy.Field()
    # 小说状态
    txt_status = scrapy.Field()
    # 小说章节
    txt_chapter = scrapy.Field()
    # 小说简介
    txt_content = scrapy.Field()
    # 小说url地址
    txt_url = scrapy.Field()
    # 小说下载地址
    txt_download_url = scrapy.Field()
    # 小说更新日期
    txt_date = scrapy.Field()
    # 小说封面地址
    txt_img_url = scrapy.Field()

class NovelCategoryItem(scrapy.Item):

    txt_category = scrapy.Field()

class NovelChapterAndContentItem(scrapy.Item):
    # 小说名
    txt_name = scrapy.Field()
    #  小说作者
    txt_author = scrapy.Field()
    # 小说章节名称
    txt_chapter_name = scrapy.Field()
    # 小说章节内容
    txt_chapter_content = scrapy.Field()


class NovelImgItem(scrapy.Item):
    # 小说名
    txt_name = scrapy.Field()
    # 图片下载地址
    txt_img_url = scrapy.Field()



    
    
    

