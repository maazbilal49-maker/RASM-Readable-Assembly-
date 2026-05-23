from parser import parse_file
import sys

for arg in sys.argv[1:]:
    parse_file(arg)