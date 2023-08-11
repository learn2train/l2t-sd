#!/usr/bin/env python3

import os
import json
import argparse


def main(output_file, prompt, negative_prompt, seed, z_axis_type, z_axis_values):
    """
    Create or add prompts to a XYZ grid prompt json file.

    Examples:
    $ prompt2test.py -i prompts.txt -O xyz_prompts_test.json -z "CFG Scale" -Z "4,7,11" 
    $ prompt2test.py -p 'A photo of a cartoon' --seed 1234 --z_axis_type "Prompt S/R" --z_axis_values="cartoon, monkey, dog, cat, statue, painting, pottery, car, house, city"
    $ prompt2test.py -p 'A portrait of Morgan Freeman' -N "cartoon, 3D"
    """
    # Open json file (if exists)
    try:
        with open (output_file, 'r') as f:
            data = json.loads(f.read())
    except Exception:
        data = []
    # Add prompt to json file
    data.extend([{
         'prompt': prompt,
         'negative_prompt': negative_prompt,
         'seed': seed,
         'z_axis_type': z_axis_type,
         'z_axis_values': z_axis_values

    }])
    # Save prompts to JSON file
    with open(output_file, 'w') as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-O', '--output_file', type=str, default='xyz_prompts.json', help='The name of the JSON file (default: xyz_prompts.json)')
    parser.add_argument('-p', '--prompt', type=str, help='Prompt')
    parser.add_argument('-N', '--negative_prompt', type=str, default='', help="Negative prompt (default: '(low quality, worst quality)')")
    parser.add_argument('-s', '--seed', type=int, default=-1, help='Seed value (default: -1)')
    parser.add_argument('-z', '--z_axis_type', type=str, default='Nothing', help="Z axis type. Options: 'Nothing', 'Prompt S/R', 'Steps', 'CFG Scale', 'Sampler', etc. (default: 'Nothing')")
    parser.add_argument('-Z', '--z_axis_values', default='', type=str, help="Z axis values. (default: '')")
    args = parser.parse_args()

    output_file = args.output_file
    prompt = args.prompt
    negative_prompt = args.negative_prompt
    seed = args.seed
    z_axis_type = args.z_axis_type
    z_axis_values = args.z_axis_values

    main(output_file, prompt, negative_prompt, seed, z_axis_type, z_axis_values)

