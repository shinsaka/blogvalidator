import scrapy
from blogvalidator.items import BlogArticle


class GossipSpider(scrapy.Spider):
    name = "movieblog"
    allowed_domains = ["kagehinata-movie.com"]
    start_urls = [
        'https://kagehinata-movie.com/',
        'https://kagehinata-movie.com/page/2',
        'https://kagehinata-movie.com/page/3',
        'https://kagehinata-movie.com/page/4',
        'https://kagehinata-movie.com/page/5',
    ]
    LIMIT_PAGES = 10
    page_count = 0
    LIMIT_IMAGES = 200
    image_count = 0

    def parse(self, response):
        # limit pages
        if self.page_count > self.LIMIT_PAGES:
            return

        for article in response.css('div.report-list article'):
            article_url = article.css('article.report-card a::attr("href")').extract_first()
            yield scrapy.Request(article_url, callback=self.parse_article_page)


    def parse_article_page(self, response):
        # limit images
        if self.image_count > self.LIMIT_IMAGES:
            return

        blog_article = BlogArticle()
        blog_article['title'] = response.css('h1 ::text').extract_first()
        blog_article['url'] = response.url
        blog_article['image_urls'] = [url for url in response.css('section.main-text img::attr("src")').extract()]

        self.image_count += len(blog_article['image_urls'])
        yield blog_article
