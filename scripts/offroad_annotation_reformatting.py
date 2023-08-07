import os
import cv2
from tqdm import tqdm
import numpy as np

class_mapping = {
    'sky': 'sky',
    'tree': 'tree',
    'forest': 'tree',
    'high_vegetation': 'tree',
    'grass': 'grass',
    'traversable_grass': 'grass',
    'vehicle': 'vehicle',
    'car': 'vehicle',
    'truck': 'vehicle',
    'bicycle': 'vehicle',
    'animal': 'animal', 
    'cow': 'animal',
    'horse': 'animal',
    'dog': 'animal',
    'sunbeam': 'sunbeam',  
    'crop': 'crop', 
    'crops': 'crop',
    'bush': 'vegetation',
    'non_traversable_low_vegetation': 'vegetation',
    'small-vegetation': 'vegetation',
    'vegetation': 'vegetation',
    'road': 'road',
    'smooth-trail': 'road', 
    'rough-trail': 'road', 
    'smooth_trail': 'road',
    'rough_trail': 'road',
    'asphalt': 'road',
    'concrete': 'road',
    'rubble': 'road', 
    'gravel': 'road',
    'dirt': 'road',
    'drivable_pavement': 'road',
    'drivable_dirt': 'road',
    'person': 'person',
    'obstacles': 'construction',
    'container': 'construction',
    'fence': 'construction',
    'picnic-table': 'construction',
    'bridge': 'construction',
    'sign': 'construction',
    'pole': 'construction',
    'object': 'construction',
    'building': 'construction',
    'wall': 'construction',
    'excavator': 'construction',
    'camper': 'construction',
    'obstacle': 'construction',
    'guard_rail': 'construction',
    'barrier': 'construction',
    'water': 'water',
    'pond': 'water', 
    'puddle': 'water',
    'background': 'other', 
    'mud': 'other', 
    'rubble': 'other',
    'rock-bed': 'other',
    'rock': 'other', 
    'log': 'other', 
    'held_object': 'other',
    'nondrivable_pavement': 'other', 
    'nondrivable_dirt': 'other',
    'void': 'other',
    'sand': 'other',
    'mulch': 'other'
}


def find_key(x, class_mapping):
   
    result_key = None
    for key, values in class_mapping.items():
        if x in values:
            result_key = key
            break
    return result_key


def read_colors_file(filename):
    color_dict = {}

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            
            if len(parts) >= 5:
                label = parts[1]
                rgb = tuple(map(int, parts[2:5]))
                color_dict[rgb] = label

    return color_dict


def get_rgb_by_label(colors_dict, label): 
    for rgb, lbl in colors_dict.items():
        if lbl == label:
            return np.array([rgb[2], rgb[1], rgb[0]], dtype=np.uint8)
        
    return np.array([0, 0, 0], dtype=np.uint8)

def get_last_number_in_dir(output_folder):
    numbers = [int(filename.split('.')[0]) for filename in os.listdir(output_folder) if filename.split('.')[0].isdigit()]
    return max(numbers, default=0)

def change_filename(last_number):
    new_number = last_number + 1
    new_filename = str(new_number).zfill(6) + '.png'
    return new_filename


def change_annotation_colors(image_path, class_mapping, terra_annotation_file, old_annotation_file, output_path):

    old_colors_dict = read_colors_file(old_annotation_file)
    terra_colors_dict = read_colors_file(terra_annotation_file)

    img = cv2.imread(image_path)
    new_img = np.zeros_like(img, dtype=np.uint8)

    for rgb, old_label in old_colors_dict.items():
        
        label = class_mapping[old_label]  
       
        if label:
            new_rgb = get_rgb_by_label(terra_colors_dict, label)
            mask = np.all(img == np.array([rgb[2], rgb[1], rgb[0]], dtype=np.uint8), axis=-1)
            new_img[mask] = new_rgb

    cv2.imwrite(output_path, new_img)



def main(input_folder, output_folder, old_annotation_file, terra_annotation_file):

    image_extensions = ['.png']

    last_number = get_last_number_in_dir(output_folder)

    sorted_filenames = sorted(os.listdir(input_folder))

    for filename in tqdm(sorted_filenames):

        if any(filename.lower().endswith(ext) for ext in image_extensions):
            image_path = os.path.join(input_folder, filename)

            new_filename = change_filename(last_number)

            output_path = f"{output_folder}/{new_filename}"

            change_annotation_colors(image_path, class_mapping,  terra_annotation_file, old_annotation_file, output_path)

            last_number += 1



if __name__ == "__main__":


    input_folder  = '/home/yohan-sl-intern/Documents/off_road_dataset/terra/annotations/rugd'

    output_folder = '/home/yohan-sl-intern/Documents/off_road_dataset/terra/annotations/terra'

    old_annotation_file = '/home/yohan-sl-intern/Documents/off_road_dataset/terra/RUGD_annotation-colormap.txt' 

    terra_annotation_file = '/home/yohan-sl-intern/Documents/off_road_dataset/terra/terra_annotations-colormap.txt' 

    main(input_folder, output_folder, old_annotation_file, terra_annotation_file)
