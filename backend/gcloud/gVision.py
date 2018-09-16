import io
import os
from google.cloud import vision
from google.cloud.vision import types

def gcloudLabels(imagePath):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    file_name = os.path.join(
        os.path.dirname(__file__), imagePath)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # print('Labels:')
    # for label in labels:
    #     print(label.description)
    return labels
    

def gcloudFaces(imagePath):
        # Instantiates a client
    client = vision.ImageAnnotatorClient()

    file_name = os.path.join(
        os.path.dirname(__file__), imagePath)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Perform face detecion
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    # likelihood_name[0] == 'UNKNOWN'
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

    group = False
    if len(faces) > 1:
        group = True
    
    return group

    # print('Face(s):')
    # for face in faces:
    #     print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
    #     print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
    #     print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
    #     print(face.anger_likelihood)

# def gcloudLandmarks():
    #todo

gcloudLabels(image)
gcloudFaces(image)