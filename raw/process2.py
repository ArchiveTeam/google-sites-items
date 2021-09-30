import sys


def main(filename: str):
    items = set()
    with open(filename, 'r') as f:
        for line in f:
            if line.count('|') == 1:
                line = line.replace('|', '/')
            elif line.count('|') > 1:
                print(line)
                raise
            line = line.strip().rstrip('/')
            if line.startswith('/a/defaultdomain/'):
                items.add('site:'+line.split('/', 3)[-1])
                print(line)
            elif line.startswith('/a/'):
                items.add('a:'+line.split('/', 2)[-1])
            elif line.startswith('/site/'):
                items.add('site:'+line.split('/', 2)[-1])
            elif line.startswith('/'):
                print(line)
                raise
            elif not '/' in line:
                items.add('site:'+line)
            elif line.count('/') == 1:
                if line.startswith('defaultdomain/'):
                    items.add('site:'+line.split('/', 1)[1])
                    print(line)
                else:
                    items.add('a:'+line)
            else:
                print(line)
                raise
    with open(filename+'.processed', 'w') as f:
        f.write('\n'.join(sorted(items)))

if __name__ == '__main__':
    main(sys.argv[1])

