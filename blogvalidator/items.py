import scrapy


class BlogArticle(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
