from api_client import ApiClient
from predictor_chata import ChataDemo
import sys
import numpy as np
import urllib
import cv2

def main():
    if len(sys.argv) < 2:
        print('Path to model config should be provided as command line argument')
    model = ChataDemo(sys.argv[1])
    client = ApiClient()
    client.login()
    latest_id = client.get_latest()
    pages = client.get_pages(latest_id)
    for id, url in pages:
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        predictions = model.get_predictions(image)
        objects = []
        for label, xmin, ymin, xmax, ymax in predictions:
            data = {
                'type':label,
                'x1':xmin,
                'y1':ymin,
                'x2':xmax,
                'y2':ymax,
                'text':'',
                'subRegions':[]
            }
            objects.append(data)
        client.add_annotation(id, objects)


if __name__ == "__main__":
    main()
