import getopt, sys
from utils.graphserializer import download_save

def usage():
    print("""
    Usage: graphbuilder.py [OPTIONS] <minlat,minlon,maxlat,maxlon>
    Build and save a routable graph
    OPTIONS:
    \t-o, --output define the output file (graph by default)
    \t-h, --help   show the help
    """)

output = "graph.pkl"

try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output"])
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(1)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ("-o", "--output"):
        output = arg
    else:
        print("ERROR in options")
        sys.exit(1)

if len(args) > 1:
    print("ERROR: too many args")
    usage()
    sys.exit(1)

c = args[0].split(',')
if len(c) != 4:
    print("ERROR: wrong coordinates")
    usage()
    sys.exit(1)

coords = []
for e in c:
    try:
        coords.append(float(e))
    except:
        print(f"ERROR: {e} is not a floating number")
        sys.exit(1)

download_save(coords[0], coords[1], coords[2], coords[3], output)