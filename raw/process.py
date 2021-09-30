import re
import sys


def main(filename: str):
    items = set()
    with open(filename, 'r') as f:
        for line in f:
            for match in re.findall(r'https?://sites\.google\.com/site/([^/\?&#"\s\]\\]+)', line):
                items.add('site:' + match)
            for match in re.findall(r'https?://sites\.google\.com/a/defaultdomain/([^/\?&#"\s\]\\]+)', line):
                print(match)
                items.add('site:' + match)
            for match in re.findall(r'https?://sites\.google\.com/a/([^/]+/[^/\?&#"\s\]\\]+)', line):
                if not match.startswith('defaultdomain/'):
                    items.add('a:' + match)
                else:
                    print(match)
    with open(filename+'.processed', 'w') as f:
        f.write('\n'.join(sorted(items)))

if __name__ == '__main__':
    main(sys.argv[1])

