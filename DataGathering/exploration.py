# code used to explore the wikidata structure and contents

import json
import gzip, bz2
import usefulQualifiers as IDS

def data(filename):
	with bz2.open(filename, mode='rt') as f:
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

class DataFile:
	def __init__(self, filename):
		self._f = open((filename+".json"), mode="wt")
		self._f.write("[\n")

		self.count = 0

	def close(self):
		self._f.write("\n]")
		self._f.close()

	def write(self, data):
		if self.count>0: self._f.write(",\n")
		self._f.write(json.dumps(data))
		self.count += 1

# open 6 different 
languages = DataFile("languages")

for row, record in enumerate(data("latest-all.json.bz2")):

# check if record has "instance of" property, if not continue to next record
	if "P31" in record["claims"]:
		instance_of = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P31"] if i["mainsnak"]["snaktype"] == "value"]

		if any((i in IDS.human_ids) for i in instance_of):
			birthplace = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P19"] if i["mainsnak"]["snaktype"] == "value"] if "P19" in record["claims"] else []
			print(birthplace)

        #     iso_639_2 = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P219"] if i["mainsnak"]["snaktype"] == "value"] if "P219" in record["claims"] else []
        #     iso_639_3 = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P220"] if i["mainsnak"]["snaktype"] == "value"] if "P220" in record["claims"] else []
        #     iso_639_6 = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P221"] if i["mainsnak"]["snaktype"] == "value"] if "P221" in record["claims"] else []
        #     ietf = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P305"] if i["mainsnak"]["snaktype"] == "value"] if "P305" in record["claims"] else []

        #     print(iso_639_2, iso_639_3, iso_639_6, ietf)


