import argparse
from apps.cml import items

# 1. Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Парсинг и печать локального xml-файла.')

# 2. Add arguments to the parser
parser.add_argument('filename', help='The file to process.')
# parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output.')
# parser.add_argument('--count', type=int, default=1, help='Number of times to perform an action.')

# 3. Parse the arguments from the command line
args = parser.parse_args()

# 4. Access the parsed arguments
file_name = "унф/import.xml"  # args.filename

print(f"Читаем из файла: {file_name}")

pack = items.Packet.parse(file_name)

assert pack.version == '2.08'
#assert pack.create_date.strftime("%Y-%m-%dT%H:%M:%S") == '2025-10-20T12:28:35'

print(pack.classifier)
print("*** Groups ***")
for _ in pack.classifier.groups:
    print(_)
    if len(_.groups) > 0:
        for __ in _.groups:
            print("--", __)

print("")
print("*** Properties ***")
for _ in pack.classifier.props:
    print(_)

print("")
print("*** Categories ***")
for _ in pack.classifier.categories:
    print(_)

print("")
print(pack.catalogue)
print("")
for i in range(5):
    print(pack.catalogue.products[i])

