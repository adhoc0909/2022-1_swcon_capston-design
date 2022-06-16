import cv2
import numpy as np
from PIL import Image
import PIL
import pandas as pd
import os
import warnings
from tqdm import tqdm
warnings.simplefilter(action='ignore', category=FutureWarning)


def Gaussian_blur(image_name):
    img = cv2.imread(image_name)
    blur = cv2.GaussianBlur(img,(5,5),0)
    return blur

def Unsharp_Mask(image_name):
    img = cv2.imread(image_name)
    gaussian_3 = cv2.GaussianBlur(img, (0, 0), 2.0)
    unsharp_image = cv2.addWeighted(img, 2.0, gaussian_3, -1.0, 0)
    return unsharp_image

def Min_filter(image_name):
    im = Image.open(image_name) # Image load
    im_array = np.asarray(im)
    size = (3, 3)
    shape = cv2.MORPH_RECT
    kernel = cv2.getStructuringElement(shape, size)
    min_image = cv2.erode(im_array, kernel)
    return Image.fromarray(min_image)




orig_csv = pd.read_csv("/root/cheXpert/CheXpert-v1.0-small/label_frontal.csv")
target_label = ['Lung Lesion', 'Pleural Other', 'Fracture']
index = orig_csv[(orig_csv[target_label[0]] == 1) | (orig_csv[target_label[1]] == 1) | (orig_csv[target_label[2]] == 1)].index



new_csv = pd.DataFrame(columns = orig_csv.columns)

for add_i, i in tqdm(enumerate(index)): #gaussian blur
    img_name = "images/"+str(i).zfill(6)+".png"
    
    im = Gaussian_blur(img_name)
   
    cv2.imwrite("images_only_augmented/"+str(add_i).zfill(6)+".png", im)
    row = orig_csv.iloc[i].copy()
    row["Path"] = "augmented/Gaussian_blur"
    row["Image_ID"] = add_i
    new_csv = new_csv.append(row, ignore_index=True)


for add_i, i in tqdm(enumerate(index)): #unsharp mask
    img_name = "images/"+str(i).zfill(6)+".png"
    im = Unsharp_Mask(img_name)

    cv2.imwrite("images_only_augmented/"+str(add_i+len(index)).zfill(6)+".png", im)
    row = orig_csv.iloc[i].copy()
    row["Path"] = "augmented/unsharp_mask"
    row["Image_ID"] = add_i + len(index)
    new_csv = new_csv.append(row, ignore_index=True)

for add_i, i in tqdm(enumerate(index)): #minimum filtering
    img_name = "images/"+str(i).zfill(6)+".png"
    im = Min_filter(img_name)
    
    im.save("images_only_augmented/"+str(add_i+len(index)+len(index)).zfill(6)+".png")
    row = orig_csv.iloc[i].copy()
    row["Path"] = "augmented/min_filtering"
    row["Image_ID"] = add_i + len(index) + len(index)
    new_csv = new_csv.append(row, ignore_index=True)

new_csv.to_csv("new_csv_2.csv", index = False)

import imageio

for i in tqdm(range(52248)):
    image_path =  '/root/cheXpert/Thorax_GAN-master/images_256/images_only_augmented_3chan/'+ str(i).zfill(6) + '.png'
    image = imageio.imread(image_path)
    if image.ndim != 2:
        image = image[:,:,0]
    image_name = str(i).zfill(6) + '.png'
    imageio.imwrite(os.path.join('/root/cheXpert/Thorax_GAN-master/images_256/images_only_augmented/', image_name), image)