import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR: {}\n\
os.path.abspath(__file__): {}\n\
os.path.dirname(os.path.abspath(__file__)): {}\
	".format(BASE_DIR, os.path.abspath(__file__),os.path.dirname(os.path.abspath(__file__))))

