import os
from tqdm import tqdm

def main():
    # Code used to parse the metadata.csv file

    # ISIC_00 + 24306
    images_name = "ISIC_00"
    counter = 24306
    max = 29305

    metadata_csv_old, metadata_csv_new = metadata_load()

    for line in tqdm(metadata_csv_old):
        # Words = an entire line, separated by ","
        # words[0] = lesion_id
        # words[1] = image_id  <--- want that
        # words[2] = dx (diaginostic, lesion type)
        # words[3] = dx_type (how the diaginostic was made, type of exam)
        # words[4] = age (irrelevant right now)
        # words[5] = sex (irrelevant right now)
        # words[6] = localization <----- want this too
        words = line.split(",")

        for i in range(max - counter):
            # in every word checks with every posible name value that we want
            # this will take a while cause the table is not order by the images_id
            name_2_match = images_name + str(counter)

            if (words[1] == name_2_match):
                # the database is not complete, so we need this to filter the images in the metadata file with the images that we have
                metadata_csv_new.write(line)

            counter += 1
            
        #reset the counter
        counter = 24306

    metadata_csv_old.close()
    metadata_csv_new.close()

def metadata_load():
    file_name = "C:/Users/Karen Reis/Desktop/Segurança/PI_Trab_Final/database/HAM10000_metadata.csv"
    metadata_csv = open(file_name, "r")

    file_name2 = "C:/Users/Karen Reis/Desktop/Segurança/PI_Trab_Final/database/metadata.csv"
    new_metadata_csv = open(file_name2, "w")

    return metadata_csv, new_metadata_csv

main()
