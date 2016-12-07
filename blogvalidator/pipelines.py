import os
from . import vision
from .settings import IMAGES_STORE


class SafeValidatorPipeline(object):
    def process_item(self, item, spider):
        result_images = []
        for image in item['images']:
            image['safe_result'] = vision.safe_search(os.path.join(IMAGES_STORE, image['path']))
            result_images.append(image)

        item['result_images'] = result_images

        return item
