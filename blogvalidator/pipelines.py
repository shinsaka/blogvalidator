import os
import datetime
from dotenv import load_dotenv, find_dotenv
import dj_database_url
import psycopg2
from . import vision
from .settings import IMAGES_STORE


load_dotenv(find_dotenv())

class SafeValidatorPipeline(object):
    spider_name = ''

    def process_item(self, item, spider):
        result_images = []
        for image in item['images']:
            image['safe_result'] = vision.safe_search(os.path.join(IMAGES_STORE, image['path']))
            result_images.append(image)
            self.insert_item(item, image)

        item['result_images'] = result_images

        return item

    def open_spider(self, spider):
        self.spider_name = spider.name
        p = dj_database_url.config()
        self.connection = psycopg2.connect(
            host=p['HOST'],
            port=p['PORT'],
            dbname=p['NAME'],
            user=p['USER'],
            password=p['PASSWORD'])
        self.connection.set_session(autocommit=True)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()

    def insert_item(self, item, image):
        """
        insert table from image hash
        """

        sql = """
            INSERT INTO crawl_item
                (name, url, violence, adult, spoof, medical, site_name, page_title, page_url, created_at)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        self.cursor.execute(sql, (
            image['path'],
            image['url'],
            image['safe_result']['safeSearchAnnotation']['violence'],
            image['safe_result']['safeSearchAnnotation']['adult'],
            image['safe_result']['safeSearchAnnotation']['spoof'],
            image['safe_result']['safeSearchAnnotation']['medical'],
            self.spider_name,
            item['title'],
            item['url'],
            datetime.datetime.now(),
        ))
