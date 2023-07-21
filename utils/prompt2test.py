#!/usr/bin/env python3

import os
import json
import argparse


def main(filename, prompt, prompt_sr, seed):
    """
    Create or add Prompt S/R tests to a JSON file.

    Examples:
    $ prompt2test.py -p 'A scene from 10 Cloverfield Lane' -r '10 Cloverfield Lane, nightmare on elm street, matrix, star wars, 20th century women, toy story'
    $ prompt2test.py -p 'A photo of a cartoon character' -r 'cartoon character, monkey, dog, cat, statue, painting, pottery, car, house, city'
    $ prompt2test.py -p 'A photo of Morgan Freeman' -r 'Morgan Freeman, Tom Cruise, Rihanna, Emma Watson, person, man, woman, boy, girl'
    """
    # Open tests file
    try:
        with open (filename, 'r') as f:
            data = json.loads(f.read())
    except Exception:
        data = []
    # Add test to file
    data.extend([{
         'prompt': prompt,
         'prompt_sr': prompt_sr,
         'seed': seed,
         'z_axis_type': "Prompt S/R"
    }])
    # Save prompts to JSON file
    with open(filename, 'w') as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default='prompt_sr_tests.json', help='The name of the tests JSON file')
    parser.add_argument('-p', '--prompt', type=str, help='Prompt')
    parser.add_argument('-r', '--prompt_sr', type=str, help='Prompt S/R')
    parser.add_argument('--seed', type=int, default=555, help='Seed')
    args = parser.parse_args()

    filename = args.filename
    prompt = args.prompt
    prompt_sr = args.prompt_sr
    seed = args.seed

    main(filename, prompt, prompt_sr, seed)

