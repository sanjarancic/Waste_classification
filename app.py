from flask import Flask, request, jsonify
from fastai.tabular import *
import os
from PIL import Image

from torchvision.transforms import transforms

cwd = os.getcwd()
path = cwd + '/resnet_model'

app = Flask(__name__)

model = torch.load('resnet_model.pt', map_location=torch.device('cpu'))

classes = {
    0: 'cardboard',
    1: 'glass',
    2: 'metal',
    3: 'paper',
    4: 'plastic',
    5: 'trash'
}


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        transformed_image = transform_image(img_bytes)
        prob, preds = torch.max(nn.Softmax(dim=1)(model(transformed_image)), dim=1)

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

