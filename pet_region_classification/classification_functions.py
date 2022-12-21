import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy import spatial
import cv2

# Reading data file (contains preprocessed images from all classes)
with open('data.pkl', 'rb') as fp:
    data = pickle.load(fp)


def img_preprocessing(img):
    # Converting to 1 channel image
    if len(img.shape) == 3:
        img = np.average(img, axis=2)

    # Resizing image to (32, 32)
    img = cv2.resize(img, (32, 32))

    return img


def softmax(vector):
    vector = np.array(vector)
    e = np.exp(vector)
    return list(e / e.sum())


def classify_image(img_path) -> str:
    img = plt.imread(img_path)

    img = img_preprocessing(img)

    img = img.flatten()

    max_similarity = {}
    average_similarity = {}
    for class_name in data.keys():

        imgs = data[class_name]
        num_imgs = len(imgs)

        temp_similarity = []
        for i in range(num_imgs):
            temp_similarity.append(-1 * (spatial.distance.cosine(img, data[class_name][i].flatten()) - 1))

        max_similarity[class_name] = max(temp_similarity)
        average_similarity[class_name] = np.mean(temp_similarity)

    max_similarity_prob = softmax(list(max_similarity.values()))
    average_similarity_prob = softmax(list(average_similarity.values()))

    return list(data.keys())[max_similarity_prob.index(max(max_similarity_prob))]


# print(classify_image('image_files/1-435.jpg'))

def classify_folder(img_folder_path):
    # Deleting existing classification results
    try:
        os.mkdir('classification_results')
    except FileExistsError:
        shutil.rmtree('classification_results')
        os.mkdir('classification_results')

    assert os.path.exists(img_folder_path), "No folder found containing image files"

    imgs = os.listdir(img_folder_path)
    num_imgs = len(imgs)

    # Making sub_folder for each classes
    for class_name in list(data.keys()):
        os.mkdir(f'classification_results/{class_name}')

    for i in range(num_imgs):
        img_path = img_folder_path + '/' + imgs[i]
        max_prob_class = classify_image(img_path)

        print(max_prob_class)
        print(f'{np.round((i + 1) * 100 / num_imgs, 2)} % Complete')
        print()

        shutil.copyfile(img_path, f'classification_results/{max_prob_class}/{imgs[i]}')

    return


classify_folder('image_files')
