import os
import shutil
import numpy as np
from sklearn.model_selection import train_test_split

# your data folder
data_folder = 'output'
# train, test, val folder
train_folder = 'data\\train'
test_folder = 'data\\test'
val_folder = 'data\\val'

# get all the file names, assuming they are all in the format 'img_<number>.ext'
file_names = [f.split('.')[0] for f in os.listdir(data_folder) if f.endswith('.png')]

# split data into train, test and validation
train_files, test_files = train_test_split(file_names, test_size=0.2, random_state=42)
test_files, val_files = train_test_split(test_files, test_size=0.5, random_state=42)

# helper function to move files
def move_files(file_list, dest_folder):
    for fname in file_list:
        # move image file
        shutil.move(os.path.join(data_folder, fname + '.png'), os.path.join(dest_folder, fname + '.png'))
        # move txt file
        shutil.move(os.path.join(data_folder, fname + '.txt'), os.path.join(dest_folder, fname + '.txt'))

# move files to corresponding folders
move_files(train_files, train_folder)
move_files(test_files, test_folder)
move_files(val_files, val_folder)
