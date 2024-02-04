import argparse
from api import download_course_files
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

LOG_FILE = os.path.join(os.getenv("ROOT"), "logs.txt")
f = open(LOG_FILE, "w")

## define command line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("courses", type=str, nargs="+",
                       help="Course code of the course to be processed")

## read command line arguments
parser = argparser.parse_args()

## start
print("programme started. downloading new files...", file=f)

## FIXME: last_updated will cause new course files to not be fully downloaded
## download files
download_course_files(parser.courses)

## end
print("programme ended successfully", file=f)
print(f"time {datetime.now()}", file=f)

f.close()