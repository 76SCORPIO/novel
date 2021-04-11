import os

# from fake_useragent import UserAgent as ua
# import fake_useragent
# Scrapy settings for novel_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'novel_spider'

SPIDER_MODULES = ['novel_spider.spiders']
NEWSPIDER_MODULE = 'novel_spider.spiders'

# def get_header():
#     location = os.getcwd() + '/fake_useragent.json'
#     ua = fake_useragent.UserAgent(path=location)
#     return ua.random

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = get_header()
# USER_AGENT = ua().random

# Obey robots.txt rules   绕过robots策略
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16) 全局并发数
CONCURRENT_REQUESTS = 40

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay

# See also autothrottle settings and docs   限制爬取速度
# DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)    禁用Cookie
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'novel_spider.middlewares.NovelSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'novel_spider.middlewares.NovelSpiderDownloaderMiddleware': 1,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'novel_spider.pipelines.NovelSpiderPipeline': 1,
   'novel_spider.pipelines.NovelImgPipeline': 2,    #为了开启图片管道

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# LOG_LEVEL = 'INFO'
# LOG_ENABLED = False


# IMAGES_STORE = r'F:\task\task_spider\txt_novel_scrapy\novel_img'   #图片存储路径
IMAGES_STORE = r'/Users/lihongwei/Desktop/py_scrapy_data/my_bixia_novel_site/images'   #图片存储路径


# 图片管道避免下载最近已经下载的图片 使用该参数 设置失效期限
# 90天的图片失效期限
IMAGES_EXPIRES = 90


# 禁止重定向
# REDIRECT_ENABLED = False
# 禁止重试
# RETRY_ENABLED = False
# 减小下载超时
# DOWNLOAD_TIMEOUT = 15







