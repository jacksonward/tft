import os
import random
from PIL import Image
from shapely.geometry import box
from concurrent.futures import ProcessPoolExecutor

def create_image(char_folder='cutouts', bg_folder='arenas', out_folder='output',
                   instances_per_image=40, max_overlap=0.1, img_counter=0):

    # Load a random background
    bg_file = random.choice(os.listdir(bg_folder))
    bg = Image.open(os.path.join(bg_folder, bg_file))
    # List all the character folders
    characters = os.listdir(char_folder)
    num_instances = random.randint(0, instances_per_image)
    
    yolo_labels = []
    boxes = []
    for _ in range(num_instances):
        # Select a random character and load a random cutout for it
        character = random.choice(characters)
        char_path = os.path.join(char_folder, character)
        char_images = os.listdir(char_path)
        cutout_file = random.choice(char_images)
        cutout = Image.open(os.path.join(char_path, cutout_file))

        # Resize the cutout randomly
        scale = random.uniform(0.3, 0.6)  # scale changed to accommodate more cutouts
        new_size = (int(cutout.width * scale), int(cutout.height * scale))
        cutout = cutout.resize(new_size, Image.LANCZOS)

        # Decide a random position for the cutout and check for overlaps
        for __ in range(50):  # Max 50 attempts to place the cutout
            left = random.randint(0, bg.width - cutout.width)
            top = random.randint(0, bg.height - cutout.height)
            new_box = box(left, top, left + cutout.width, top + cutout.height)

            # Check for overlaps with the existing boxes
            overlaps = [new_box.intersection(b).area / new_box.area > max_overlap for b in boxes]
            if not any(overlaps):
                boxes.append(new_box)
                break
        else:
            continue  # Skip this cutout if we couldn't place it

        # Paste the cutout onto the background
        bg.paste(cutout, (left, top), cutout)

        # Prepare a YOLO label
        x_center = (left + cutout.width / 2) / bg.width
        y_center = (top + cutout.height / 2) / bg.height
        width = cutout.width / bg.width
        height = cutout.height / bg.height
        yolo_labels.append(f"{characters.index(character)} {x_center} {y_center} {width} {height}\n")

    # Save the final image and the YOLO labels
    out_file = os.path.join(out_folder, f"img_{str(random.randint(100000000, 999999999))}.png")
    bg.save(out_file, "PNG")

    with open(out_file.replace('.png', '.txt'), 'w') as f:
        f.writelines(yolo_labels)
        img_counter += 1

    return True

def create_dataset(char_folder='cutouts', bg_folder='arenas', out_folder='output',
                   instances_per_image=40, max_overlap=0.1, num_images=50000):

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    characters = os.listdir(char_folder)
    
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        if __name__ == '__main__':
            futures = {executor.submit(create_image, char_folder, bg_folder, out_folder, instances_per_image, max_overlap, i): i for i in range(num_images)}
            for future in futures:
                print('Completed image:', futures[future])
                if not future.result():
                    print('Failed to create image:', futures[future])

create_dataset()