"""Sorts duplicate photos/files and places all copies in their own folder."""

import click
import halo

from hashlib import sha256
from pathlib import Path
from shutil import copyfile, move

""" Return the SHA256 sum of the provided file name.

:param file_name - Name of the file to check
:return Hexdigst of SHA sum
"""
def sha256sum(file_name):
    with open(file_name, 'rb') as file_bytes:
        return sha256(file_bytes.read()).hexdigest()
    return ''

@click.command()
@click.argument('directory', type=click.Path(file_okay=False, exists=True))
@click.option('--move/--copy', '-m/-c', default=False)
def main(directory, move):
    dup_dir = Path('{}/duplicate_files'.format(directory))
    # Do stuff
    if not dup_dir.exists():
        dup_dir.mkdir()
    click.echo('This script will iterate through the directory \'{0}\' and move all duplicate files to a subdirectory named \'{1}\'.'.format(directory, dup_dir))
    #click.confirm('Do you wish to continue?', abort=True)
    path = Path(directory)

    hash_dict = dict()
    for file_path in path.iterdir():
        print(file_path)
        if Path(file_path).is_file():
            sha_sum = sha256sum(file_path)
            if sha_sum in hash_dict.keys():
                hash_dict[sha_sum].append(file_path)
            else:
                hash_dict[sha_sum] = [file_path]
    print(hash_dict)

    for sha_sum in list(filter(lambda x: len(hash_dict[x]) > 1, hash_dict.keys())):
        for filepath in hash_dict[sha_sum]:
            if move:
                move(filepath, dup_dir / filepath.parts[-1])
            else:
                copyfile(filepath, dup_dir / filepath.parts[-1])

if __name__ == '__main__':
    main()
