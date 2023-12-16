#!/usr/env/bin python3

import os
import glob
import json
import datetime
import argparse
import re
import webuiapi

def main(filename, output_folder, sampler, steps, seed, cfg_scale, width, height):
    """
    Generate XYZ grids from a XYZ prompt JSON file and save images and texts to the `output` folder.

    Examples:
    $ python generate_xyz_grids.py --input_filename 'xyz_prompt-1.json' --output_folder 'tests'
    $ python3 generate_xyz_grids.py -W 768 -H 768
    """
    # datetime
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Instantiate Webuiapi
    api = webuiapi.WebUIApi(host='127.0.0.1',
                        port=7860,
                        sampler=sampler,
                        steps=steps
                        )
    # Load prompts
    with open (filename, 'r') as j:
        xyz_prompt_list = json.loads(j.read())
        print(f'Loaded {len(xyz_prompt_list)} prompt tests')

    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(f'{output_folder}/{dt}')
    else:
        os.makedirs(f'{output_folder}/{dt}')

    XYZPlotAvailableTxt2ImgScripts = [
    "Nothing",
    "Seed",
    "Var. seed",
    "Var. strength",
    "Steps",
    "Hires steps",
    "CFG Scale",
    "Prompt S/R",
    "Prompt order",
    "Sampler",
    "Checkpoint name",
    "Sigma Churn",
    "Sigma min",
    "Sigma max",
    "Sigma noise",
    "Eta",
    "Clip skip",
    "Denoising",
    "Hires upscaler",
    "VAE",
    "Styles",
    ]

    # Generate grid for each prompt
    counter = 0
    for p in xyz_prompt_list:
        counter += 1
        print(f'Generating xyz grid {counter} out of {len(xyz_prompt_list)} prompt tests')
        prompt = p.get('prompt')
        negative_prompt = p.get('negative_prompt')
        # Prepare prompt
        XAxisType = p.get('x_axis_type')
        XAxisValues = p.get('x_axis_values')
        YAxisType = p.get('y_axis_type')
        YAxisValues = p.get('y_axis_values')
        ZAxisType = p.get('z_axis_type')
        ZAxisValues = p.get('z_axis_values')
        drawLegend = "True"
        includeLoneImages = "False"
        includeSubGrids = "False"
        noFixedSeeds = "False"
        marginSize = 0
        result = api.txt2img(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    seed=int(seed),
                    cfg_scale=cfg_scale,
                    width=width,
                    height=height,
                    script_name="X/Y/Z Plot",
                    denoising_strength=0.7,
                    seed_resize_from_h=0,
                    seed_resize_from_w=0,
                    script_args=[
                        XYZPlotAvailableTxt2ImgScripts.index(XAxisType),
                        XAxisValues,
                        [],
                        XYZPlotAvailableTxt2ImgScripts.index(YAxisType),
                        YAxisValues,
                        [],
                        XYZPlotAvailableTxt2ImgScripts.index(ZAxisType),
                        ZAxisValues,
                        [],
                        drawLegend,
                        includeLoneImages,
                        includeSubGrids,
                        noFixedSeeds,
                        marginSize,                        ]
                    )
        seq = '{0:0>4}'.format(counter)
        truncated_prompt = prompt[:100]
        path_filename = f'{output_folder}/{dt}/xyz_grid-{seq}-{seed}-{width}x{height}-{truncated_prompt}'
        print(f'Saving image as "{path_filename}.png"')
        print('')
        result.image.save(f'{path_filename}.png')
        # Save txt file
        image_info =  f'''
Prompt: {prompt}
Negative prompt: {negative_prompt}

Sampler: {sampler}
Steps: {steps}
Seed: {seed}
CFG scale: {cfg_scale}
Height: {height}
Width: {width}
Script: X/Y/Z plot
X Type: {XAxisType}   
X Values: {XAxisValues}
Y Type: {YAxisType}
Y Values: {YAxisValues}
Z Type: {ZAxisType}
Z Values: {ZAxisValues}
'''
        with open(f"{path_filename}.txt", "w") as f:
            f.write(image_info)


if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_filename', type=str, default='xyz_prompts.json', help="The name of the JSON file (default: 'xyz_prompts.json')")
    parser.add_argument('-O', '--output_folder', type=str, default='output', help='Folder where images and text files will be saved to ( default: output/ )')
    parser.add_argument('-S', '--sampler', type=str, default='Euler a', help='Sampler (default: Euler a)')
    parser.add_argument('-t', '--steps', type=int, default=20, help='Steps value (default: 20)')
    parser.add_argument('-s', '--seed', type=int, default=555, help='Seed value (default: 555)')
    parser.add_argument('-c', '--cfg_scale', type=float, default=7.0, help='CFG value (default: 7.0)')
    parser.add_argument('-W', '--width', type=int, default=512, help='Width value (default: 512)')
    parser.add_argument('-H', '--height', type=int, default=512, help='Height value (default: 512)')
    args = parser.parse_args()

    filename = args.input_filename
    output_folder = args.output_folder
    sampler = args.sampler
    steps = args.steps
    seed = args.seed
    cfg_scale = args.cfg_scale
    width = args.width
    height = args.height

    # Run main
    main(filename, output_folder, sampler, steps, seed, cfg_scale, width, height)
