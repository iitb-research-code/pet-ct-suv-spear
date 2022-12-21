# This has code to rename and organize exemplar images
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import pickle
from PIL import Image


def rename_files_in_data() -> None:
    classes = os.listdir('data')
    num_classes = len(classes)

    print(f'Number of classes = {num_classes}')

    os.chdir('data')

    for class_name in classes:
        os.chdir(class_name)

        imgs = os.listdir()

        for j in range(len(imgs)):
            try:
                os.rename(imgs[j], f'{class_name[:2:]}_{j}.{imgs[j].split(".")[1]}')
            except FileExistsError:
                pass

        # print(imgs)

        os.chdir('..')

    os.chdir('..')

    return


def resize_and_create_pkl_file() -> None:
    imgs_dict = {}

    classes = os.listdir('data')
    num_classes = len(classes)

    os.chdir('data')

    for i in range(num_classes):
        imgs_dict[f'{classes[i][3::]}'] = []

        print(f'Images for {classes[i][3::]} - {len(os.listdir(f"{classes[i]}"))}')

        os.chdir(f'{classes[i]}')

        imgs = os.listdir()
        num_images = len(imgs)

        for j in range(num_images):
            # img = Image.open(imgs[j])
            img = plt.imread(imgs[j])

            # print(img.shape)

            img = np.average(img, axis=2)
            img = cv2.resize(img, (32, 32))


            # plt.imshow(img)
            # plt.show()

            img = img / np.max(img)

            # print(np.max(img))
            # print(img.shape)

            imgs_dict[f'{classes[i][3::]}'].append(img)

        os.chdir('..')

    os.chdir('..')

    with open('data.pkl', 'wb') as fp:
        pickle.dump(imgs_dict, fp)
    fp.close()

    print('Pickle file written')

    return


# rename_files_in_data()

resize_and_create_pkl_file()
