import sys
import subprocess

command = "grep -m 1 {} ./dict/{}"


def lookup(h):
    result = subprocess.run(command.format(h, h[0]).split(' '), stdout=subprocess.PIPE)
    return result.stdout.decode('UTF-8').split(' ')[0]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)
    print(lookup(sys.argv[1]))