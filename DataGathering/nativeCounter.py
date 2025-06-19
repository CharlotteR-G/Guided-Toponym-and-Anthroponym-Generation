# simple code to count the number of people in the coarse data that do and do not
# have a native name or native language


import gzip
import json
from datetime import datetime

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("source", help = "Human data (people.json.gz) from wikidata")
args = parser.parse_args()

def data(filename):
	with gzip.open(filename, mode='rt') as f:
		f.read(2) # skip first two bytes: "[\n"
		for line in f:
			try:
				yield json.loads(line.rstrip(',\n'))
			except json.decoder.JSONDecodeError:
				#continue
				if line.strip().startswith(']'):
					continue
				else:
					print('Error processing:')
					print(line)
					continue

native_count = 0
no_native_count = 0
starttime = datetime.now()
for row, record in enumerate(data(args.source)):
	
    # if no native name present or no native language
	if len(record["native_name"]) == 0 and len(record["native_language"]) == 0:
		no_native_count += 1
	else:
		native_count += 1

print(f"Final count: {native_count} people with native names or native language, {no_native_count} people without native names or native language")
