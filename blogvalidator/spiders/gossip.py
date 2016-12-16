import scrapy
from blogvalidator.items import BlogArticle


class GossipSpider(scrapy.Spider):
    name = "gossip"
    allowed_domains = ["gossip1.net"]
    start_urls = [
        'http://gossip1.net/',
    ]
    LIMIT_PAGES = 10
    page_count = 0
    LIMIT_IMAGES = 200
    image_count = 0

    def parse(self, response):
        # limit pages
        if self.page_count > self.LIMIT_PAGES:
            return

        for article in response.css('article'):
            article_url = article.css('p.article-title > a::attr("href")').extract_first()
            yield scrapy.Request(article_url, callback=self.parse_article_page)


        next_page_url = response.css('li.paging-next a::attr("href")').extract_first()
        if next_page_url:
            self.page_count += 1
            yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_article_page(self, response):
        # limit images
        if self.image_count > self.LIMIT_IMAGES:
            return

        blog_article = BlogArticle()
        blog_article['title'] = response.css('article p.article-title ::text').extract_first()
        blog_article['url'] = response.url
        #blog_article['image_urls'] = [url for url in response.css('article img::attr("src")').extract() if url[-3:] == 'jpg']
        blog_article['image_urls'] = [url for url in response.css('article img::attr("src")').extract()]

        self.image_count += len(blog_article['image_urls'])
        yield blog_article
