import argparse
import multiprocessing
import os

import requests


def queuer(item: str, key: str):
    print('queuing', item)
    response = requests.post(
        'http://blackbird-amqp.meo.ws:23038/{}/'.format(key),
        data=item
    )
    if response.status_code not in (200, 409):
        print('got response', response.status_code)
        raise ValueError('bad response')


def main(filename: str, concurrency: int, key: str):
    print('queuing file', filename)
    with open(filename, 'r') as f:
        items = [line.strip() for line in f]
    with multiprocessing.Pool(concurrency) as p:
        p.starmap(queuer, ((item, key) for item in items))
    os.rename(filename, os.path.join('ADDED', filename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--index', type=int,
                        help='index of the file to queue')
    parser.add_argument('-f', '--filename', type=str,
                        help='filename of the file to queue')
    parser.add_argument('-c', '--concurrency', type=int, default=10,
                        help='concurrency with which to queue items')
    parser.add_argument('-k', '--key', type=str, required=True,
                        help='key to queue to')
    args = parser.parse_args()
    if args.index is None and args.filename is None:
        raise Exception('--index of --filename shoud be given')
    if args.index is not None:
        for filename in os.listdir('.'):
            number = filename.split('_', 1)[0]
            if not number.isdigit():
                continue
            if int(number) == args.index:
                break
        else:
            raise Exception('index not found')
    else:
        filename = args.filename
    main(filename, args.concurrency, args.key)

