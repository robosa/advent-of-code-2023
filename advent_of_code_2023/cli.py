import importlib
import sys

import click


@click.command()
@click.option("--day", "-d", type=click.IntRange(0, 25), required=True)
@click.option("--hard", "-a", is_flag=True)
def cli(day: int, hard: bool):
    try:
        module = importlib.import_module(f"advent_of_code_2023.day_{day:02}")
    except ModuleNotFoundError:
        print("Solution not available.")
        sys.exit(1)
    print(module.run(filename=f"inputs/day_{day:02}", hard=hard))
