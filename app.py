import numpy as np
from flask import Flask, request, render_template, jsonify
import pickle
from fastai.tabular import *
import os
from PIL import Image

from torchvision.transforms import transforms

cwd = os.getcwd()
path = cwd + '/model'

app = Flask(__name__)

model = load_learner(path, 'model.pkl')

classes = {
    1: 'cardboard',
    2: 'glass',
    3: 'metal',
    4: 'paper',
    5: 'plastic',
    6: 'trash'
}

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        transformed_image = transform_image(img_bytes)
        prob, preds = torch.max(model(transformed_image), dim=1)
        return jsonify({'probability': prob[0].item(), 'class': classes[preds[0].item()]})


def transform_image(img_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(img_bytes))
    return my_transforms(image).unsqueeze(0)


if __name__ == '__main__':
    app.run()

