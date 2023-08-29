#!/usr/bin/env python3

import json
import sys
import os
import random
import argparse
import imghdr


def is_image(file_path):
    image_formats = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'webp']  # Add more formats if needed
    return imghdr.what(file_path) in image_formats

def count_images_in_folder(folder_path):
    image_count = 0
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if is_image(file_path):
                image_count += 1
    return image_count

def clean_filename(filename):
    return filename.split('_')[0]

def get_captions_from_filename(input_directory):
    """
    Get captions from image filenames inside an input directory recursively and put them into a list. 

    Example:

    input/'a man and his dog_01.jpg'
    input/dogs/'a dog having a beer_12.jpg'

    $ get_captions_from_filename('input')
    $ ['a man and his dog', 'a dog having a beer']
    """
    image_formats = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'webp']  # Add more formats if needed
    filename_list = [] 
    for root, _, files in os.walk(input_directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if imghdr.what(file_path) in image_formats:
                filename_list.append(filename)
    caption_list = []
    for file in filename_list:
        caption_list.append(clean_filename(file))
    return caption_list

def get_captions(input_directory):
    """
    Get captions from text files inside an input folder recursively and put them into a list.

    Example:

    input/001.txt # a man climbing a wall
    input/bearded-men/022.txt # a close up photo of a bearded man

    $ get_captions.py('input')
    ['a man climbing a wall', 'a close up photo of a bearded man']
    """
    caption_list = []
    for root, _, files in os.walk(input_directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith('.txt'):
                try:
                    with open(file_path, 'r') as f:
                        caption_list.append(f.readline().strip())
                except Exception as e:
                    print(f"An error occurred: {e}")
    return caption_list

def main(num_prompts, output_file, input_directory, negative_prompt,  seed, z_axis_type, z_axis_values, filename_caption):
    """
    Create a XYZ grid prompt json file from captions inside an input directory. 

    Other prompt parameters can be used and will be applied to all captions:
    - Negative prompt
    - Seed
    - Z axis type
    - Z axis values

    Examples:
    $ python caption2prompt.py -O xyz_prompts_test-caption-in-filename.json -N "(low quality, worst quality), EasyNegativeV2" --z_axis_type "Prompt S/R" --z_axis_values "Joe Smith,man" --seed -1 -n 20 -f
    $ python caption2prompt.py --z_axis_type "Steps" --z_axis_values "20,30" --seed 1234 -d images
    """
    image_count = count_images_in_folder(input_directory)
    print(f'Creating {num_prompts} from {image_count} images files from the `{input_directory}` directory')
    if image_count < num_prompts:
        print(f'ERROR: Not enough images to generate {num_prompts} prompts')
        sys.exit(1)

    # Get captions
    if filename_caption:
        captions = get_captions_from_filename(input_directory)
    else:
        captions = get_captions(input_directory)

    if captions:
        caption_list = random.sample(captions, num_prompts)
        # Prepare data dict with captions as prompts
        data = []
        for prompt in caption_list:
    	    d = {}
    	    d['prompt'] = prompt
    	    d['negative_prompt'] = negative_prompt
    	    d['seed'] = seed
    	    d['z_axis_type'] = z_axis_type
    	    d['z_axis_values'] = z_axis_values
    	    data.append(d)
        # Save prompts to json file
        with open(output_file, 'w') as fp:
            json.dump(data, fp)
    else:
        print('ERROR: Could not get captions')
        return sys.exit(1)

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_prompts', type=int, default=15, help='Number of prompts to generate at random from the files in input directory (default: 15)')
    parser.add_argument('-d', '--input_directory', type=str, default='input', help="The folder where caption filenames are located (default: 'input')")
    parser.add_argument('-O', '--output_file', type=str, default='xyz_prompts.json', help='The name of the JSON file (default: xyz_prompts.json)')
    parser.add_argument('-N', '--negative_prompt', type=str, default='', help="Negative prompt (default: '')")
    parser.add_argument('-s', '--seed', type=int, default=-1, help='Seed value (default: -1)')
    parser.add_argument('-z', '--z_axis_type', type=str, default='Nothing', help="Z axis type. Options: 'Nothing', 'Prompt S/R', 'Steps', 'CFG Scale', 'Sampler', etc. (default: 'Nothing')")
    parser.add_argument('-Z', '--z_axis_values', default='', type=str, help="Z axis values. (default: '')")
    parser.add_argument('-f', '--filename_caption', action='store_true', default=False, help='Get captions from filenames. (default: False)')
    args = parser.parse_args()

    num_prompts = args.num_prompts
    input_directory = args.input_directory
    output_file = args.output_file
    negative_prompt = args.negative_prompt
    seed = args.seed
    z_axis_type = args.z_axis_type
    z_axis_values = args.z_axis_values
    filename_caption = args.filename_caption

    # Run main
    main(num_prompts, output_file, input_directory, negative_prompt,  seed, z_axis_type, z_axis_values, filename_caption)
