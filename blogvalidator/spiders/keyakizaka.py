import scrapy
from blogvalidator.items import BlogArticle


class KeyakizakaSpider(scrapy.Spider):
    name = "keyakizaka"
    allowed_domains = ["keyakizaka46.com"]
    start_urls = [
        'http://www.keyakizaka46.com/mob/news/diarKiji.php?site=k46o&ima=0000&cd=member',
    ]
    LIMIT_PAGES = 500
    page_count = 0
    LIMIT_IMAGES = 2000
    image_count = 0

    def parse(self, response):
        # limit pages
        if self.page_count > self.LIMIT_PAGES:
            return

        for article in response.css('article'):
            article_url = article.css('h3 > a::attr("href")').extract_first()
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article_page)

        next_page_url = response.css('div.pager li:last-child > a::attr("href")').extract_first()
        if next_page_url:
            self.page_count += 1
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_article_page(self, response):
        # limit images
        if self.image_count > self.LIMIT_IMAGES:
            return

        blog_article = BlogArticle()
        blog_article['title'] = response.css('article div.box-ttl > h3 ::text').extract_first().strip()
        blog_article['url'] = response.url
        blog_article['image_urls'] = [response.urljoin(url) for url in response.css('article img::attr("src")').extract()]

        self.image_count += len(blog_article['image_urls'])
        yield blog_article
