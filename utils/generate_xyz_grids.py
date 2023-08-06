#!/usr/env/bin python3

import os
import glob
import json
import datetime
import argparse
import re
import webuiapi

def main(filename, ckpt_folder, checkpoints, baseline_ckpt, output_folder, sampler, steps, seed, cfg_scale, width, height):
    """
    Generate XYZ grids from a prompt test JSON file and save images and their respective text files to `output` folder.

    Examples:
    $ python3 generate_xyz_grids.py -f 'prompt_sr_tests.json' -C 'models/Stable-diffusion' -o 'output'
    $ python3 generate_xyz_grids.py -f 'xyz_prompt_tests.json'
    $ python3 generate_xyz_grids.py -f 'xyz_prompt_tests.json' -w 1024 -h 512
    $ wget -O - https://raw.githubusercontent.com/roperi/sd-utils/main/generate_xyz_grids.py | python3 - -f 'xyz_prompt_tests.json'
    """
    # datetime
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Instantiate Webuiapi
    api = webuiapi.WebUIApi(host='127.0.0.1',
                        port=7860,
                        sampler=sampler,
                        steps=steps
                        )
    if not checkpoints:
        # Get your checkpoints
        ckpt_list = [os.path.basename(x) for x in glob.glob(f'{ckpt_folder}/*gs*.ckpt')]

        # Sort checkpoints by global step ascending
        substrings = [int(x) for string in ckpt_list for x in re.findall(r'gs(\d+)', string)]
        substrings.sort()
        checkpoint_list = [string for x in substrings for string in ckpt_list if int(re.findall(r'gs(\d+)', string)[0]) == x]

        # Add baseline ckpt
        if baseline_ckpt:
            checkpoint_list.insert(0, baseline_ckpt)

        # Prepare checkpoints str
        checkpoints = ','.join(checkpoint_list)

    # Load prompts
    with open (filename, 'r') as j:
        prompt_tests_list = json.loads(j.read())
        print(f'Loaded {len(prompt_tests_list)} prompt tests')

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

    # Generate grid for each prompt test
    counter = 0
    for p in prompt_tests_list:
        counter += 1
        print(f'Generating xyz grid {counter} out of {len(prompt_tests_list)} prompt tests')
        prompt = p.get('prompt')
        prompt_sr = p.get('prompt_sr')
        seed = str(p.get('seed'))
        z_axis_type = p.get('z_axis_type')
        # Prepare prompt
        XAxisType = "Seed"
        XAxisValues = seed
        YAxisType = "Checkpoint name"
        YAxisValues = checkpoints
        ZAxisType = z_axis_type
        ZAxisValues = prompt_sr
        drawLegend = "True"
        includeLoneImages = "False"
        includeSubGrids = "False"
        noFixedSeeds = "False"
        marginSize = 0
        result = api.txt2img(
                    prompt=prompt,
                    seed=seed,
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
                        XYZPlotAvailableTxt2ImgScripts.index(YAxisType),
                        YAxisValues,
                        XYZPlotAvailableTxt2ImgScripts.index(ZAxisType),
                        ZAxisValues,
                        drawLegend,
                        includeLoneImages,
                        includeSubGrids,
                        noFixedSeeds,
                        marginSize,                        ]
                    )
        seq = '{0:0>4}'.format(counter)
        path_filename = f'{output_folder}/{dt}/xyz_grid-{seq}-{seed}-{width}x{height}-{prompt}'
        print(f'Saving image as {path_filename}.png')
        print('')
        result.image.save(f'{path_filename}.png')
        # Save txt file
        image_info =  f'''
Prompt: {prompt}

Steps: {steps}
Sampler: {sampler}
CFG scale: {cfg_scale}
Script: X/Y/Z plot
X Type: Seed
X Values: {seed}
Fixed X Values: {seed}
Y Type: Checkpoint name
Y Values: {checkpoints}
Z Type: {z_axis_type}
Z Values: "{prompt_sr}"
'''
        with open(f"{path_filename}.txt", "w") as f:
            f.write(image_info)


if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default='prompt_tests.json', help='The name of the tests JSON file (default: prompt_tests.json)')
    parser.add_argument('-F', '--ckpt_folder', type=str, default='models/Stable-diffusion/', help='Folder where checkpoints are located ( default: models/Stable-diffusion )')
    parser.add_argument('-C', '--checkpoints', type=str, default=None, help='Comma-separated list of checkpoint names to be used instead of using those found in the ckpt folder. Eg. "SD-1.5.ckpt,SDv2-768.ckpt" (default=None)')
    parser.add_argument('-b', '--baseline_ckpt', type=str, default='SDv1-5.ckpt', help='Baseline checkpoint used for comparisons (default: SDv1-5.ckpt)')
    parser.add_argument('-o', '--output_folder', type=str, default='output', help='Folder where images and text files will be saved to ( default: output/ )')
    parser.add_argument('-S', '--sampler', type=str, default='Euler a', help='Sampler (default: Euler a)')
    parser.add_argument('-t', '--steps', type=int, default=20, help='Steps value (default: 20)')
    parser.add_argument('-s', '--seed', type=int, default=555, help='Seed value (default: 555)')
    parser.add_argument('-c', '--cfg_scale', type=float, default=7.0, help='CFG value (default: 7.0)')
    parser.add_argument('-W', '--width', type=int, default=512, help='Width value (default: 512)')
    parser.add_argument('-H', '--height', type=int, default=512, help='Height value (default: 512)')
    args = parser.parse_args()

    filename = args.filename
    ckpt_folder = args.ckpt_folder
    checkpoints = args.checkpoints
    baseline_ckpt = args.baseline_ckpt
    output_folder = args.output_folder
    sampler = args.sampler
    steps = args.steps
    seed = args.seed
    cfg_scale = args.cfg_scale
    width = args.width
    height = args.height

    # Run main
    main(filename, ckpt_folder, checkpoints, baseline_ckpt, output_folder, sampler, steps, seed, cfg_scale, width, height)
