from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS  # add this
from transformers import GLPNFeatureExtractor, GLPNForDepthEstimation
from PIL import Image
import torch
import numpy as np
import requests

app = Flask(__name__)
CORS(app)  # enable CORS on all routes
api = Api(app)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan",
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

feature_extractor = GLPNFeatureExtractor.from_pretrained("vinvino02/glpn-nyu")
model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")

class Predict(Resource):
    @auth.login_required
    def post(self):
        inputs = request.get_json(force=True)
        url = inputs['image_url']
        image = Image.open(requests.get(url, stream=True).raw)

        # prepare image for the model
        inputs = feature_extractor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            predicted_depth = outputs.predicted_depth

        # interpolate to original size
        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        )

        # visualize the prediction
        output = prediction.squeeze().cpu().numpy()
        formatted = (output * 255 / np.max(output)).astype("uint8")

        return jsonify(formatted.tolist())  # return as JSON

api.add_resource(Predict, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
