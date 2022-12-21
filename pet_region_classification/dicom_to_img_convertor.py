import pydicom as dicom
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os


def convert_all_dicom_to_imgs(img_format = '.jpg') -> None:

    dicom_file_names = os.listdir('dicom_files')

    num_imgs = len(dicom_file_names)

    for i in range(len(dicom_file_names)):

        dicom_file_path = f'dicom_files/{dicom_file_names[i]}'

        ds = dicom.dcmread(dicom_file_path)

        pixel_array = ds.pixel_array

        to_save_image_path = f'image_files/{dicom_file_names[i].replace(".dcm", img_format)}'

        plt.imsave(to_save_image_path, pixel_array, cmap='gray')

        print(f'Saved - {dicom_file_names[i].replace(".dcm", img_format)}')
        print(f'{np.round((i+1) * 100 / num_imgs, 2)} % Complete')
        print()


convert_all_dicom_to_imgs()


