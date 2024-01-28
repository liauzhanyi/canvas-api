import argparse
from utils import refresh_cache
from api import download_course_files, cache

## define command line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("courses", type=str, nargs="+",
                       help="Course code of the course to be processed")

## read command line arguments
parser = argparser.parse_args()

## start
print("programme started. downloading new files...")

## download files
download_course_files(parser.courses)

## end
print("programme ended successfully")