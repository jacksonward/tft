import cv2
import numpy as np
from PIL import Image

from concurrent.futures import ProcessPoolExecutor
import os

def makeCutouts(mkvPath):

    # Get filename, without extension
    filename = mkvPath.split('\\')[-1].split('.')[0]

    print(filename)
    # Step 1
    cap = cv2.VideoCapture(mkvPath)

    # Set the frame number to skip. If you want every frame, set this to 1
    frame_skip = 10

    frame_count = 0

    # define the RGB tuple for our color to be replaced
    target_color = (0, 0, 0)  # black
    tolerance = 50  # define your tolerance level

    def color_within_tolerance(color_a, color_b, tolerance):
        return sum((a - b) ** 2 for a, b in zip(color_a, color_b)) <= tolerance ** 2

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        # Step 3
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))

        # Step 4
        datas = image.getdata()

        new_data = []
        for item in datas:
            if color_within_tolerance(item[:3], target_color, tolerance):
                new_data.append((item[0], item[1], item[2], 0))  # Make transparent
            else:
                new_data.append(item)
        image.putdata(new_data)

        # Step 5
        bbox = image.getbbox()
        if bbox:
            image = image.crop(bbox)

        # Step 6
        image.save(f'cutouts/{filename}/{filename}_{frame_count//frame_skip}.png')

    cap.release()


directory = 'model_recordings'
video_files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
with ProcessPoolExecutor() as executor:
        print(video_files)
        if __name__ == '__main__':
            executor.map(makeCutouts, video_files)
