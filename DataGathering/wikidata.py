import os
import bz2, gzip
import json
from datetime import datetime
import usefulQualifiers as IDS # holds all important IDs from Wikidata

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("source", help="BZ2 Wikidata dump file.")
parser.add_argument("output", help="Output directory")
args = parser.parse_args()

# make output directory
os.makedirs(args.output, exist_ok=True)

tags = set()

def wikidata(filename):
	with bz2.open(filename, mode="rt") as f:
		f.read(2) # skip first two bytes: "[\n"
		for line in f:
			try:
				yield json.loads(line.rstrip(",\n"))
			except json.decoder.JSONDecodeError:
				#continue
				if line.strip().startswith("]"):
					continue
				else:
					print("Error processing:")
					print(line)
					continue

# Taken from Tom"s code
class DataFile:
	def __init__(self, filename):
		self._f = gzip.open(os.path.join(args.output,filename+".json.gz"), mode="wt", compresslevel=6)
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
people = DataFile("people")
mythological = DataFile("mythological")
names = DataFile("names")
countries = DataFile("countries")
places = DataFile("places")
languages = DataFile("languages")
occupations = DataFile("occupations")
fictional = DataFile("fictional") # check if has an instance with fictional in label

starttime = datetime.now()
for row, record in enumerate(wikidata(args.source)):
	
    # check if record has "instance of" property, if not continue to next record
	if "P31" in record["claims"]:
		instance_of = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P31"] if i["mainsnak"]["snaktype"] == "value"]

		# form collection of people
		if any((i in IDS.human_ids) for i in instance_of):

			# English label if there is one
			label = record["labels"]["en"] if "en" in record["labels"] else next(iter(record["labels"].values()), None)
			# Any English aliases
			aliases = record["aliases"]["en"] if "en" in record["aliases"] else next(iter(record["aliases"].values()), [])
			# Which categories of human the entity belongs to
			categories = [i for i in instance_of if i in IDS.human_ids]
			# list of sex/genders the person belongs to
			sex = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P21"] if i["mainsnak"]["snaktype"] == "value"] if "P21" in record["claims"] else []
			citizenship = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P27"] if i["mainsnak"]["snaktype"] == "value"] if "P27" in record["claims"] else []
			ethnicity = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P172"] if i["mainsnak"]["snaktype"] == "value"] if "P172" in record["claims"] else []
			birthplace = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P19"] if i["mainsnak"]["snaktype"] == "value"] if "P19" in record["claims"] else []

			native_language = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P103"] if i["mainsnak"]["snaktype"] == "value"] if "P103" in record["claims"] else []
			languages_spoken = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P1412"] if i["mainsnak"]["snaktype"] == "value"] if "P1412" in record["claims"] else []
			writing_languages = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P6886"] if i["mainsnak"]["snaktype"] == "value"] if "P6886" in record["claims"] else []

			native_name = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1559"] if i["mainsnak"]["snaktype"] == "value"] if "P1559" in record["claims"] else []

			# if native_name missing, use native language and tags to find native_name

			# if not native_name and len(native_language) != 0:
			# 	if native_language[0] in IDS.IETF_lookup:
			# 		tag = IDS.IETF_lookup[native_language[0]]
			# 		name = record["labels"][tag] if tag in record["labels"] else next(iter(record["labels"].values()), None)
			# 		native_name = [{"text": name["value"], "language": name["language"]}]
			# 		print("\nchange", native_name, "\n", tag)
			# 	else:
			# 		print("no translation")
			# else:
			# 	if native_name:
			# 		print("no change", native_name)
			
			# for each native language
			#	find the equivalent IETF tag

			# 	language_name = ""
			# 	for i in IDS.specific_language_ids:
			# 		if list(i.keys())[0] == native_language[0]:
			# 			language_name = i[native_language[0]]
			# 			for i in IDS.IETF_translation:
			# 				if language_name in i["English"]:
			# 					native_language_tag = i["alpha2"]
			# 					# start work on autoencoder whilst this runs
			# 					name = record["labels"][native_language_tag] if native_language_tag in record["labels"] else next(iter(record["labels"].values()), None)
			# 					native_name = [{"text": name["value"], "language": name["language"]}]
			# 					# print("\n", native_name, "\n")
			# 					break
			# 			break
			# else:
			# 	if native_name:
			# 		print(native_name)


			birth_name = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1477"] if i["mainsnak"]["snaktype"] == "value"] if "P1477" in record["claims"] else []

			given_names = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P735"] if i["mainsnak"]["snaktype"] == "value"] if "P735" in record["claims"] else []
			family_name = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P734"] if i["mainsnak"]["snaktype"] == "value"] if "P734" in record["claims"] else []

			pseudonyms = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P742"] if i["mainsnak"]["snaktype"] == "value"] if "P742" in record["claims"] else []

			professions = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P106"] if i["mainsnak"]["snaktype"] == "value"] if "P106" in record["claims"] else []

			people.write({
				"id": record["id"],
				"label": label,
				"aliases": aliases,
				"categories": categories,
				"sex": sex,
				"citizenship": citizenship,
				"ethnicity": ethnicity,
				"birthplace": birthplace,
				"native_language": native_language,
				"languages_spoken": languages_spoken,
				"writing_languages": writing_languages,
				"native_name": native_name,
				"birth_name": birth_name,
				"given_names": given_names,
				"family_name": family_name,
				"pseudonyms": pseudonyms,
				"occupations": professions,
			})

		# form collection of names

		elif any((i in IDS.given_name_ids) for i in instance_of):

			label = record["labels"]["en"] if "en" in record["labels"] else next(iter(record["labels"].values()),None)
			aliases = record["aliases"]["en"] if "en" in record["aliases"] else next(iter(record["aliases"].values()), [])
			categories = [i for i in instance_of if i in IDS.given_name_ids]

			language_usage = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P407"] if i["mainsnak"]["snaktype"] == "value"] if "P407" in record["claims"] else []
			native_label = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1705"] if i["mainsnak"]["snaktype"] == "value"] if "P1705" in record["claims"] else []
			writing_system = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P282"] if i["mainsnak"]["snaktype"] == "value"] if "P282" in record["claims"] else []
			pronounced_languages = [
					j["datavalue"]["value"]["id"]
					for i in record["claims"]["P443"]
					for j in i.get("qualifiers",{}).get("P407",[])
					if i["mainsnak"]["snaktype"] == "value" and j["snaktype"] == "value"] if "P443" in record["claims"] else []

			other_forms = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P460"] if i["mainsnak"]["snaktype"] == "value"] if "P460" in record["claims"] else []
			other_gender = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P1560"] if i["mainsnak"]["snaktype"] == "value"] if "P1560" in record["claims"] else []

			# ALREADY COMMENTED ---------------------------------
			#nickname_ids = [
			#		j["datavalue"]["value"]["id"]
			#		for i in record["claims"]["P1449"]
			#		for j in i.get("qualifiers",{}).get("P805",[])
			#		if i["mainsnak"]["snaktype"] == "value" and j["snaktype"] == "value"] if "P1449" in record["claims"] else []
			#nickname_text = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1449"] if i["mainsnak"]["snaktype"] == "value"] if "P1449" in record["claims"] else []

			# ------------------------------------------------------------

			nicknames = [
					(
						i["mainsnak"]["datavalue"]["value"],
						[j["datavalue"]["value"]["id"] for j in i.get("qualifiers",{}).get("P805",[]) if j["snaktype"] == "value"]
						)
					for i in record["claims"]["P1449"]
					if i["mainsnak"]["snaktype"] == "value"] if "P1449" in record["claims"] else []

			names.write({
				"id": record["id"],
				"label": label,
				"aliases": aliases,
				"categories": categories,
				"language_usage": language_usage,
				"native_label": native_label,
				"writing_system": writing_system,
				"pronounced_languages": pronounced_languages,
				"other_forms": other_forms,
				"nicknames": nicknames,
				"other_gender": other_gender
			})

		elif any((i in IDS.language_ids) for i in instance_of):

			label = record["labels"]["en"] if "en" in record["labels"] else next(iter(record["labels"].values()),None)
			categories = [i for i in instance_of if i in IDS.language_ids]

			subclass_of = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P279"] if i["mainsnak"]["snaktype"] == "value"] if "P279" in record["claims"] else []
			native_label = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1705"] if i["mainsnak"]["snaktype"] == "value"] if "P1705" in record["claims"] else []

			writing_system = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P282"] if i["mainsnak"]["snaktype"] == "value"] if "P282" in record["claims"] else []
			influenced_by = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P737"] if i["mainsnak"]["snaktype"] == "value"] if "P737" in record["claims"] else []

			iso_639_2 = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P219"] if i["mainsnak"]["snaktype"] == "value"] if "P219" in record["claims"] else []
			iso_639_3 = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P220"] if i["mainsnak"]["snaktype"] == "value"] if "P220" in record["claims"] else []
			iso_639_6 = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P221"] if i["mainsnak"]["snaktype"] == "value"] if "P221" in record["claims"] else []
			ietf = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P305"] if i["mainsnak"]["snaktype"] == "value"] if "P305" in record["claims"] else []

			languages.write({
				"id": record["id"],
				"label": label,
				"categories": categories,
				"subclass_of": subclass_of,
				"native_label": native_label,
				"writing_system": writing_system,
				"influenced_by": influenced_by,
				"iso_639_2": iso_639_2,
				"iso_639_3": iso_639_3,
				"iso_639_6": iso_639_6,
				"ietf": ietf,
			})

		elif any((i in IDS.country_ids) for i in instance_of):

			label = record["labels"]["en"] if "en" in record["labels"] else next(iter(record["labels"].values()),None)
			categories = [i for i in instance_of if i in IDS.country_ids]

			official_name = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1448"] if i["mainsnak"]["snaktype"] == "value"] if "P1448" in record["claims"] else []
			native_label = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1705"] if i["mainsnak"]["snaktype"] == "value"] if "P1705" in record["claims"] else []

			official_language = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P37"] if i["mainsnak"]["snaktype"] == "value"] if "P37" in record["claims"] else []
			languages_used = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P2936"] if i["mainsnak"]["snaktype"] == "value"] if "P2936" in record["claims"] else []

			countries.write({
				"id": record["id"],
				"label": label,
				"categories": categories,
				"official_name": official_name,
				"native_label": native_label,
				"official_language": official_language,
				"languages_used": languages_used,
			})

		elif "P17" in record["claims"] and "P625" in record["claims"]: # Must have a listed country and geographic coordinate

			label = record["labels"]["en"] if "en" in record["labels"] else next(iter(record["labels"].values()),None)

			native_label = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1705"] if i["mainsnak"]["snaktype"] == "value"] if "P1705" in record["claims"] else []

			country = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P17"] if i["mainsnak"]["snaktype"] == "value"]

			places.write({
				"id": record["id"],
				"label": label,
				"instance_of": instance_of,
				"country": country,
				"native_label": native_label
			})

		elif "P1049" in record["claims"]: # Has a "worshipped by" claim

			label = record["labels"]["en"] if "en" in record["labels"] else next(iter(record["labels"].values()), None)
			aliases = record["aliases"]["en"] if "en" in record["aliases"] else next(iter(record["aliases"].values()), [])

			worshipped_by = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P1049"] if i["mainsnak"]["snaktype"] == "value"] if "P1049" in record["claims"] else []

			gender = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P21"] if i["mainsnak"]["snaktype"] == "value"] if "P21" in record["claims"] else []

			native_name = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1559"] if i["mainsnak"]["snaktype"] == "value"] if "P1559" in record["claims"] else []
			birth_name = [i["mainsnak"]["datavalue"]["value"] for i in record["claims"]["P1477"] if i["mainsnak"]["snaktype"] == "value"] if "P1477" in record["claims"] else []

			given_names = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P735"] if i["mainsnak"]["snaktype"] == "value"] if "P735" in record["claims"] else []
			family_name = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P734"] if i["mainsnak"]["snaktype"] == "value"] if "P734" in record["claims"] else []

			mythological.write({
				"id": record["id"],
				"label": label,
				"aliases": aliases,
				"instance_of": instance_of,
				"worshipped_by": worshipped_by,
				"gender": gender,
				"native_name": native_name,
				"birth_name": birth_name,
				"given_names": given_names,
				"family_name": family_name
			})

		# form collection of occupations
		elif any((i in IDS.occupation_ids) for i in instance_of):

			label = record["labels"]["en"] if "en" in record["labels"] else next(iter(record["labels"].values()), None)

			categories = [i for i in instance_of if i in IDS.country_ids]

			subclass_of = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P279"] if i["mainsnak"]["snaktype"] == "value"] if "P279" in record["claims"] else []

			occupation_field = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P425"] if i["mainsnak"]["snaktype"] == "value"] if "P425" in record["claims"] else []

			occupations.write({
				"id": record["id"],
				"label": label,
				"categories": categories,
				"instance_of": instance_of,
				"subclass_of": subclass_of,
				"occupation_field": occupation_field,
			})


		# form collection of fictional people and places
		elif "P1441" in record["claims"]: # has a "present in work" property
			# English label
			label = record["labels"]["en"] if "en" in record["labels"] else next(iter(record["labels"].values()), None)
			# Any English aliases
			aliases = record["aliases"]["en"] if "en" in record["aliases"] else next(iter(record["aliases"].values()), [])

			sex = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P21"] if i["mainsnak"]["snaktype"] == "value"] if "P21" in record["claims"] else []
			
			given_names = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P735"] if i["mainsnak"]["snaktype"] == "value"] if "P735" in record["claims"] else []

			professions = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P106"] if i["mainsnak"]["snaktype"] == "value"] if "P106" in record["claims"] else []

			native_language = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P103"] if i["mainsnak"]["snaktype"] == "value"] if "P103" in record["claims"] else []

			creator = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P170"] if i["mainsnak"]["snaktype"] == "value"] if "P170" in record["claims"] else []

			character_type = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P9071"] if i["mainsnak"]["snaktype"] == "value"] if "P9071" in record["claims"] else []

			fictional_universe = [i["mainsnak"]["datavalue"]["value"]["id"] for i in record["claims"]["P1080"] if i["mainsnak"]["snaktype"] == "value"] if "P1080" in record["claims"] else []


			fictional.write({
				"id": record["id"],
				"label": label,
				"aliases": aliases,
				"instance_of": instance_of,
				"sex": sex,
				"given_names": given_names,
				"occupations": professions,
				"native_language": native_language,
				"character_type": character_type,
				"creator": creator,
				"fictional_universe": fictional_universe,
			})
	
	if (row+1) % 100000 == 0:
		print(f"{datetime.now().strftime("%H:%M:%S")} row {row+1:12} ({people.count} people, {mythological.count} mythological, {names.count} names, {countries.count} countries, {places.count} places, {languages.count} languages, {occupations.count} occupations, {fictional.count} fictional)"  )
		
for f in [people, mythological, names, countries, places, languages, occupations]:
	f.close()

print("Finished.")
print("Time taken:",datetime.now()-starttime)
print(f"Final count: {people.count} people, {mythological.count} mythological, {names.count} names, {countries.count} countries, {places.count} places, {languages.count} languages, {occupations.count} occupations, {fictional.count} fictional")




