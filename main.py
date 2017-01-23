# Increment dirs in path
import sys,os
sys.path.append(os.path.realpath('.')+"/lib")

from lib import parse,mw_error


if __name__ == "__main__":
    course_data = parse.GenerateData(6360)
    course_data.output_data()

