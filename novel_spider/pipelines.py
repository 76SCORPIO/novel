# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from datetime import datetime
import scrapy

from scrapy.exceptions import DropItem

from scrapy.pipelines.images import ImagesPipeline    #scrapy定制图片管道 用于下载项目图片 保存到本地

from .items import NovelSpiderItem,NovelImgItem,NovelCategoryItem,NovelChapterAndContentItem

from .SqlPool import OPMySql


class NovelSpiderPipeline(object):
    def __init__(self):
        # MYSQL#
        # DBhost = '192.168.153.128'
        # DBhost = '127.0.0.1'
        # DBport = 3306
        # DBuser = 'root'
        # DBpasswd = 'lhw100418'
        # DBdb = 'my_bixia_novel'
        # DBdb = 'my_bixia_novel_site'

        self.MYSQL = OPMySql("my_bixia_novel_site")
        self.con,self.cur = self.MYSQL.getConn()

    def process_item(self, item, spider):

        if isinstance(item,NovelSpiderItem):
            ### 写入 小说 全部信息  novel
            sql_query_novel = f"select count(*) from novel where txt_name = '{item['txt_name']}' AND txt_author = '{item['txt_author']}';"

            novel_result,ALL = self.MYSQL.handleSql(self.con,self.cur,sql_query_novel,"SELECT")

            if novel_result[0] == 1:
                print('*****已有数据,不执行插入!')

            elif novel_result[0] == 0:
                sql_insert_novel = f"insert into novel(txt_name,txt_category,txt_author,txt_words,txt_status,txt_chapter,txt_content,txt_url,txt_download_url,txt_date,create_time) values ('{item['txt_name']}','{item['txt_category']}','{item['txt_author']}','{item['txt_words']}','{item['txt_status']}','{item['txt_chapter']}','{item['txt_content']}','{item['txt_url']}','{item['txt_download_url']}','{item['txt_date']}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');"
                self.MYSQL.handleSql(self.con,self.cur,sql_insert_novel,"INSERT")

        if isinstance(item,NovelCategoryItem):

            ### 写入 小说 分类列表 novel_category

            sql_query_novel_category = f"select count(*) from novel_category where txt_category = '{item['txt_category']}';"
            novel_category_result,ALL = self.MYSQL.handleSql(self.con,self.cur,sql_query_novel_category,"SELECT")

            if novel_category_result[0] == 1:
                print('*****分类已有 加1!')
                sql_update_novel_category = f"update novel_category SET txt_num=txt_num+1 where txt_category = '{item['txt_category']}';"
                self.MYSQL.handleSql(self.con,self.cur,sql_update_novel_category,"UPDATE")

            elif novel_category_result[0] == 0:
                sql_insert = f"insert into novel_category(txt_category, txt_num)values ('{item['txt_category']}',1);"
                self.MYSQL.handleSql(self.con,self.cur,sql_insert,"INSERT")

        if isinstance(item,NovelChapterAndContentItem):

            ### 写入小说 章节名称和章节内容  novel_chapter  chapter_content
            try:
                sql_query_novel_id = f"select id from novel where txt_name = '{item['txt_name']}' and txt_author = '{item['txt_author']}';"

                novel_id,ALL = self.MYSQL.handleSql(self.con,self.cur,sql_query_novel_id,"SELECT")

                sql_query_novel_chapter = f"select count(*) from novel_chapter_content where txt_chapter_name = '{item['txt_chapter_name']}' AND txt_novel_id = {novel_id[0]};"

                novel_chapter_result,ALL = self.MYSQL.handleSql(self.con,self.cur,sql_query_novel_chapter,"SELECT")

                if novel_chapter_result[0] == 1:
                    print('*****章节名称 已有数据 不执行插入!')

                elif novel_chapter_result[0] == 0:
                    sql_insert_novel_chapter_content = f"insert into novel_chapter_content(txt_chapter_name, txt_chapter_content,txt_novel_id) values ('{item['txt_chapter_name']}','{item['txt_chapter_content']}',{novel_id[0]});"
                    self.MYSQL.handleSql(self.con,self.cur,sql_insert_novel_chapter_content,"INSERT")

            except Exception as e:
                print('',e)

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.con.close()


# 图片下载管道 继承定制图片管道  ,  重写get_media_requests() 方法
class NovelImgPipeline(ImagesPipeline):
    # 下载图片 如果传过来是一个集合 需要循环下载
    def get_media_requests(self, item, info):
        if isinstance(item,NovelImgItem):

            yield scrapy.Request(item['txt_img_url'],meta={'txt_name':item['txt_name']})

    # 是否下载成功
    def item_completed(self, results, item, info):
        file_paths = [x["path"] for ok, x in results if ok]

        if not file_paths:
            raise DropItem('*****下载失败!')
        return item

    #图片存放
    def file_path(self, request, response=None, info=None):
        img_name = request.meta['txt_name']+'.jpg'
        return img_name





















