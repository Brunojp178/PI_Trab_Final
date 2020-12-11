# Compara imagens de lesões na pele por histogramas para tentar
# uma comparação positiva para imagens semelhantes a lesões de cancer de pele

import numpy as np
import cv2, math, os
from tqdm import tqdm

def main():
    # TODO, load the database images, load the csv file with info on the images
    # filter the images joining using the colums "region"

    # path of the dir where the images're located
    images_path = 'C:/Users/Karen Reis/Desktop/PI_Trab_Final/database/HAM10000_images_part_1'
    csv_path = 'C:/Users/Karen Reis/Desktop/PI_Trab_Final/database/metadata.csv'

    # the images_list will have the same indexs as the distances list
    # 'cause the images're in crescent order

    # load all the images and save in this list, yep, 4 thousand images in one list :D
    images_list = load_database_images(images_path)

    # compare the images
    distances = calculateHist(images_list)

    distance_threshhold = 45.0

    images_2_check = []

    for i in tqdm(range(1, len(distances)), desc='Comparing the distances'):
        if (distances[i] < distance_threshhold):
            images_2_check.append(24306 + i)

# The first image on the list is the image to compare
def calculateHist(imageList):
    image_input = imageList[0]

    histograms = []
    distances = []

    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    # concat lists
    ranges = h_ranges + s_ranges
    # Use the 0-th and 1-st channels
    channels = [0, 1]

    histogram_input = cv2.calcHist([image_input], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(histogram_input, histogram_input, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    # For every image, calculate the histogram and save on the list
    for img in tqdm(imageList, desc='calc. histograms'):
        hist = cv2.calcHist([img], channels, None, histSize, ranges, accumulate=False)
        cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

        histograms.append(hist)

    for histo in tqdm(histograms, desc='comp. histograms'):
        # calculate the histograms distance with the first image on the list
        correlation = cv2.compareHist(histogram_input, histo, 0)
        chiSquare = cv2.compareHist(histogram_input, histo, 1)
        bhatta = cv2.compareHist(histogram_input, histo, 3)

        correlation = pow((1/(correlation + 0.001)), 2)
        chiSquare = pow(chiSquare, 2)
        bhatta = pow(bhatta, 2)

        distance = correlation + chiSquare + bhatta
        # sqrt(Corr^2 + Chi-Sq^2 + Bhatta^2)
        distance = math.sqrt(distance)
        distances.append(distance)

    return distances

def load_database_images(path):
    # Use this to limitate the database :D
    # define max_index with the number of images that you want
    count = 24306
    max_index = 300
    # save a list of file names
    files = os.listdir(path)
    images = []
    max_index += 24306
    for file in tqdm(files, desc='Loading database'):
        name = path + "/"+ file
        img = cv2.imread(name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        images.append(img)
        count += 1
        if(count == max_index): break;

    # return the list of the images in hsv format
    return images

def database_check(metadata_path, images):

    # load the metadata.csv
    metadata = open(metadata_path, "r")

    # to every image, read the file to find the metadata, compare to the first one and see if the dx and bodypart was the same
    for img in images:
        # reads the file:
        current_name = "ISIC_00" + str(img)

        for line in metadata:
            # image_input is the first image of the list (24306)
            # all the test were made with it
            image_input = metadata[0].split(',')

            # Words = an entire line, separated by ","
            # words[0] = lesion_id
            # words[1] = image_id  <--- want that
            # words[2] = dx (diaginostic, lesion type)
            # words[3] = dx_type (how the diaginostic was made, type of exam)
            # words[4] = age (irrelevant right now)
            # words[5] = sex (irrelevant right now)
            # words[6] = localization <----- want this too
            words = line.split(",")

            # compare the image_id of the list with the img of the distance results
            # (aka. is this line the image that is on the first for)
            if (words[1] == current_name):
                # compare if the dx was the same (same desease)
                if(words[2] == image_input[2]):
                    print("Teria acertado um possivel cancer baseado na primeira imagem da base")


main()
