import argparse
import functools
import os
import typing

import zstandard


@functools.lru_cache(maxsize=None)
def load_items(filepath: str) -> typing.Set[str]:
    print('loading file', filepath)
    if filepath.endswith('.zst'):
        with open(filepath, 'rb') as f:
            return {
                line.strip()
                for line in str(
                    zstandard.ZstdDecompressor().decompress(f.read()),
                    'utf8'
                ).splitlines()
            }
    with open(filepath, 'r') as f:
        return {line.strip() for line in f}


def get_done() -> typing.Set[str]:
    items = set()
    for filename in os.listdir('ADDED'):
        items |= load_items(os.path.join('ADDED', filename))
    for filename in os.listdir('.'):
        if not filename.endswith('.txt'):
            continue
        items |= load_items(filename)
    print('found total of', len(items), 'processed items')
    return items


def dump_list(items: typing.List[str], index: int) -> int:
    for i in range(0, len(items), 500000):
        filename = '{}_{}.txt'.format(str(index).zfill(3), items[0].split(':')[0])
        if os.path.isfile(filename):
            raise Exception(filename + ' already exixts.')
        with open(filename, 'w') as f:
            print('writing', f.name)
            f.write('\n'.join(items[i:i+500000]))
            index += 1
    return index


def main(filename: str, index: int) -> int:
    new_items = load_items(filename)
    print('found', len(new_items), 'in', filename)
    new_items -= get_done()
    print('found', len(new_items), 'new items in', filename)
    items_site = sorted(s for s in new_items if s.startswith('site:'))
    items_a = sorted(s for s in new_items if s.startswith('a:'))
    index = dump_list(items_site, index)
    return dump_list(items_a, index)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str,
                        help='The (maybe zst) file to process.')
    parser.add_argument('-i', '--index', type=int, required=True,
                        help='The index of the next to list to create.')
    parser.add_argument('-d', '--dir', type=str,
                        help='The directory to process all files from.')
    args = parser.parse_args()
    if (args.dir and args.filename) or (not args.dir and not args.filename):
        print('--filename or --dir should be given')
    if args.dir:
        index = args.index
        for filename in os.listdir(args.dir):
            index = main(os.path.join(args.dir, filename), index)
    else:
        main(args.filename, args.index)

