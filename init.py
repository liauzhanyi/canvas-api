import os
import argparse
from dotenv import load_dotenv

load_dotenv()

## define command line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("courses", type=str, nargs="+",
                       help="Course code of the course to be processed")
argparser.add_argument("-p", "--path", type=str, required=False,
                       default=os.getenv("HOME"),
                       help="""
                       Absolute or relative path to initialise folders. 
                       Defaults to HOME directory.
                       """)

## read command line arguments
parser = argparser.parse_args()

confirm = input(
    "This will overwrite existing folders with the folowing names:\n" +
    "\n".join(parser.courses).upper() + "\n" +
    "Continue? (y/n) "
    ).lower()

## make directories
for course in parser.courses:
    os.makedirs(os.path.join(parser.path, course.upper()), exist_ok=True)
    os.makedirs(os.path.join(parser.path, os.getenv("NEW_FILES_FOLDER")), exist_ok=True)