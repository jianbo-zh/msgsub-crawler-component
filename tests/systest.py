import sys

def main():
    print(sys.argv)
    print(sys.argv[0])
    for i in range(1, len(sys.argv)):
        print('arg %s -> %s' % (i, sys.argv[i]))

if __name__ == "__main__":
    main()

