from logging import INFO, StreamHandler, getLogger
from sys import stdout
import cv2
from numpy import np
import os
import traceback
import inference

IMAGE_DIR = f'{os.getcwd()}/images'
print('IMAGE_DIR:', IMAGE_DIR)

def load_image(image_path):
    # Case insenstive check of the image type.
    img_lower = image_path.lower()
    if (
        img_lower.endswith(
            ".jpg",
            -4,
        )
        or img_lower.endswith(
            ".png",
            -4,
        )
        or img_lower.endswith(
            ".jpeg",
            -5,
        )
    ):
        try:
            image_data = cv2.imread(image_path)
        except Exception as e:
            print("Unable to read the image: ", e)
            exit(1)
    elif img_lower.endswith(
        ".npy",
        -4,
    ):
        image_data = np.load(image_path)
    else:
        print("Images of format jpg,jpeg,png and npy are only supported.")
        exit(1)
    return image_data


def handler(fname):
    image_data = load_image(os.path.join(IMAGE_DIR, fname))
    
    event = {
        'body': image_data
    }

    print('image_data: ', image_data)

    try:
        result = inference.handler(event,"")          
        return result['body'][0]['Label']
    except:
        traceback.print_exc()
        
def run(event, context):
    print('event: ', event)

    data = event['body-json']

    # convert string of image data to uint8
    nparr = np.fromstring(data, np.uint8)

    # decode image
    img = cv2.imdecode(nparr, cv2.imread.IMREAD_COLOR)

    print('img: ', img)

    fname = 'cat.jpeg'
    label = handler(fname)
    print(fname + " -> "+ label)
    
    return {
        'statusCode': 200,
        'label': label
    }  