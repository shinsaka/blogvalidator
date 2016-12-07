import base64
import httplib2
import json
from .settings import VISION_API_KEY


def safe_search(image_filepath):
    """
    return: dict or None
    """

    if not VISION_API_KEY:
        print('not found google vision api key')
        return None

    with open(image_filepath, 'rb') as image:
        http = httplib2.Http()

        req_json = json.dumps({
            'requests': [{
                'image': {
                    "content": base64.b64encode(image.read()).decode('ascii')
                },
                'features': [{'type': 'SAFE_SEARCH_DETECTION'}],
            }]
        })
        response, content = http.request(
            'https://vision.googleapis.com/v1/images:annotate?key={0}'.format(VISION_API_KEY),
            'POST',
            headers={'Content-Type': 'application/json'},
            body=req_json,
        )

        if response.status != 200:
            print('http error({0})'.format(response.status))
            return None

        try:
            response = json.loads(content.decode('utf-8'))
            return response['responses'][0]
        except:
            return None
