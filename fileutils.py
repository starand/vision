# -*- coding: utf-8 -*-
#

def storeLastUpdateId(filename, id):
    with open(filename, 'w') as f:
        f.write('%d' % id)

def loadLastUpdateId(filename):
    id = 0
    try:
        with open(filename, 'r') as f:
            id = int(f.readline())
    except FileNotFoundError as e:
        print('File %s not found' % filename)
    except ValueError as e:
        print('last_id not found')
    return id