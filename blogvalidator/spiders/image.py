import scrapy
from blogvalidator.items import BlogArticle


class ImageSpider(scrapy.Spider):
    name = "image"
    allowed_domains = ["serverworks.co.jp"]
    start_urls = [
        'http://blog.serverworks.co.jp/tech/category/techical/',
    ]
    MAX_CRAWL_PAGE_COUNT = 5
    crawld_page_count = 0

    def parse(self, response):
        for article in response.css('article'):
            article_url = article.css('h1 > a::attr("href")').extract_first()
            yield scrapy.Request(article_url, callback=self.parse_article_page)

        next_page_url = response.css('div.nav_to_paged > a::attr("href")').extract_first()
        if next_page_url and self.crawld_page_count < self.MAX_CRAWL_PAGE_COUNT:
            self.crawld_page_count += 1
            yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_article_page(self, response):
        blog_article = BlogArticle()
        blog_article['title'] = response.css('article h1.single-title ::text').extract_first()
        blog_article['url'] = response.url
        blog_article['image_urls'] = [url for url in response.css('article img::attr("src")').extract()]

        yield blog_article
