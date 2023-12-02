from importlib import import_module
from os.path import exists
from sys import exit

import click


@click.command()
@click.option("--day", "-d", type=click.IntRange(0, 25), required=True)
@click.option("--hard", "-a", is_flag=True)
def cli(day: int, hard: bool):
    try:
        module = import_module(f"advent_of_code_2023.day_{day:02}")
    except ModuleNotFoundError:
        print("Solution not available")
        exit(1)
    filename = f"inputs/day_{day:02}"
    if not exists(filename):
        print(f"Missing {filename}")
        exit(1)
    print(module.run(filename, hard))
