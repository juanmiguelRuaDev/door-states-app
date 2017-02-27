import os
import sys
sys.path.insert(0, '..')

BASE_DIR = os.path.dirname(os.path.realpath(__name__))

if __name__ == "__main__":
    print(BASE_DIR + os.path.sep + "resources" + os.path.sep + "config.ini")
