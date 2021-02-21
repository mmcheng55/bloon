import click
import os

create_file = lambda file: open(file, "w+")


@click.command()
@click.option("--dir", default=os.getcwd(), help="Init a Bloon Directory.")
def init(dir):
    for files in ["main.py", "settings.txt"]:
        create_file(dir + "\\" + files)


if __name__ == '__main__':
    init()
