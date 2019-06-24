from api_client import ApiClient
from predictor_chata import ChataDemo
import sys
import numpy as np
import urllib
import cv2
from maskrcnn_benchmark.config import cfg

def main():
    if len(sys.argv) < 3:
        print('Usage: Path to model config path to model last_checkpoint model type')
    output_dir = sys.argv[2]
    model_type = sys.argv[3]
    cfg.merge_from_file(sys.argv[1])
    cfg.merge_from_list(["OUTPUT_DIR", output_dir])
    model = ChataDemo(cfg, model_type)
    
    client = ApiClient()
    client.login()
    #latest_id = client.get_latest()
    newest_ids = client.get_new_publications()
    for pub_id in newest_ids:
        pages = client.get_pages(pub_id)
        print(pub_id)
        for id, url in pages:
            print(id)
            print(url)
            resp = urllib.request.urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            predictions = model.get_predictions(image)
            annotations = annotate(predictions)
            print(annotations)
            if annotations:
                print('writing annotation...')
                for annotation in annotations:
                    client.add_annotation(id, annotation)

def annotate(predictions):
    objects = []
    for label, xmin, ymin, xmax, ymax in predictions:
        if label in ["chart", "table"]:
            data = {
                'type':label,
                'x1':xmin[0],
                'y1':ymin[0],
                'x2':xmax[0],
                'y2':ymax[0],
                'text':'',
                'subRegions':[]
                }
            objects.append(data)
    return objects
   
if __name__ == "__main__":
    main()
