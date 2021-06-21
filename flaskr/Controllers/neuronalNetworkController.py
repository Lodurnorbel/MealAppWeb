import cv2
import matplotlib.image as mpimg
import numpy as np
from flask import (
    Blueprint, request, jsonify
)

from flaskr.Models.Services import neuronalNetworkService

bp = Blueprint('neuronalNetwork', __name__, url_prefix='/neuronalNetwork')


@bp.route('/upload', methods=['POST'])
def upload_base64_file():
    data = request.files

    if data is None:
        print("No valid request body, json missing!")
        return jsonify({'error': 'No valid request body, json missing!'})
    else:
        file = data['img']
        filestr = file.read()
        npimg = np.fromstring(filestr, np.uint8)
        aux_img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        img = mpimg.imread(file)
        #plt.imshow(img)
        #plt.show()

        detections = neuronalNetworkService.analyzeImage(img)
        final_image, mealList = neuronalNetworkService.drawBoxes(aux_img, detections)
        price, namesList = neuronalNetworkService.calculatePrice(mealList)

        return jsonify({'img': final_image,
                        'price': price,
                        'mealList': namesList})
