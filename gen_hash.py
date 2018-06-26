import time
from hashlib import md5
import string
from itertools import product
import os


def gen_hash():
    start_time = time.time()

    if not os.path.exists('dict'):
        os.mkdir('dict')

    chars = string.digits + string.ascii_uppercase
    files = []
    for filename in (string.digits + string.ascii_lowercase[:6]):
        f = open('dict/' + filename, 'w')
        files.append(f)
    for i in product(chars, repeat=6):
        msg = ''.join(i)
        h = md5(msg.encode('UTF-8')).hexdigest()
        files[int(h[:1], 16)].write('%s %s\n' % (msg, h))

    print('Time Consumed: %f' % (time.time() - start_time))


if __name__ == '__main__':
    gen_hash()
