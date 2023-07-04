import os
import random
from PIL import Image

# Constants
x = 0
y = 10
WIDTH = 1920
HEIGHT = 1080
MAX_OVERLAP = 0.2
MAX_TRIES = 50

def place_cutouts_on_background(background, cutouts, min_cutouts, max_cutouts):
    cutouts_on_bg = background.copy()
    all_boxes = []

    # Randomly place each cutout onto the background
    for class_id, cutout_list in enumerate(cutouts):
        num_cutouts = random.randint(min_cutouts, max_cutouts)
        
        for _ in range(num_cutouts):
            for _ in range(MAX_TRIES):
                cutout = random.choice(cutout_list)
                left = random.randint(0, WIDTH - cutout.width)
                top = random.randint(0, HEIGHT - cutout.height)
                new_box = (left, top, left + cutout.width, top + cutout.height)

                # Check overlap with existing boxes
                if not any(iou(new_box, box[1]) > MAX_OVERLAP for box in all_boxes):
                    cutouts_on_bg.paste(cutout, (left, top), cutout)
                    all_boxes.append((class_id, new_box))
                    break
    return cutouts_on_bg, all_boxes

def iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    interArea = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    box1Area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2Area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    iou = interArea / float(box1Area + box2Area - interArea)
    return iou

def yolo_format_bbox(box, class_id, img_width, img_height):
    # Convert from (left, top, right, bottom) to (x_center, y_center, width, height) and normalize
    x_center = (box[0] + box[2]) / 2 / img_width
    y_center = (box[1] + box[3]) / 2 / img_height
    width = (box[2] - box[0]) / img_width
    height = (box[3] - box[1]) / img_height

    return f"{class_id} {x_center} {y_center} {width} {height}"

def main():
    # Load background and cutouts
    arenas_path = "arenas"
    cutouts_path = "cutouts"
    output_path = "output"

    backgrounds = [Image.open(os.path.join(arenas_path, bg)).convert("RGBA") for bg in os.listdir(arenas_path)]
    cutouts = [[Image.open(os.path.join(cutouts_path, class_folder, cutout)).convert("RGBA") 
                for cutout in os.listdir(os.path.join(cutouts_path, class_folder))] 
               for class_folder in os.listdir(cutouts_path)]

    # Generate images
    for i, background in enumerate(backgrounds):
        img, boxes = place_cutouts_on_background(background, cutouts, x, y)
        img.save(os.path.join(output_path, f"{i}.png"))
        
        # Save labels in YOLO format
        with open(os.path.join(output_path, f"{i}.txt"), 'w') as f:
            for class_id, box in boxes:
                f.write(yolo_format_bbox(box, class_id, WIDTH, HEIGHT) + "\n")

if __name__ == "__main__":
    main()
