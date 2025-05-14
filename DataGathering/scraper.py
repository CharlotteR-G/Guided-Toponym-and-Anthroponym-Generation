import requests
import csv

# GENDERS = ["female given name", "male given name"]

GENDERS = {
    "female given name": "Q11879590",
    "male given name": "Q12308941"
}

# cultureQualifiers = {
#     "english": "Q1860"
# }

# URL = f"https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query=SELECT%20DISTINCT%20%3FitemLabel%0AWHERE%20%7B%0A%20%20%20%20%3Fitem%20wdt%3AP31%20wd%3AQ11879590%3B%20%23%20Any%20instance%20of%20{GENDER}%0A%20%20%20%20%20%20%20%20%20%20wdt%3AP282%20wd%3AQ8229%3B%20%23%20latin%20writing%20script%0A%20%20%20%20%20%20%20%20%20%20wdt%3AP407%20wd%3AQ1860%3B%20%23%20With%20the%20property%20of%20english%20origin%0A%20%20%20%20%20%20%20%20%20%20wikibase%3Asitelinks%20%3Fsitelinks.%0A%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cmul%2Cen%22%20%7D%0A%7D%0AORDER%20BY%20DESC%28%3Fsitelinks%29"

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['given name', 'gender']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for key, value in GENDERS.items():
        response = requests.get(f"https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query=SELECT%20DISTINCT%20%3FitemLabel%0AWHERE%20%7B%0A%20%20%20%20%3Fitem%20wdt%3AP31%20wd%3A{value}%3B%20%23%20Any%20instance%20of%20{key}%0A%20%20%20%20%20%20%20%20%20%20wdt%3AP282%20wd%3AQ8229%3B%20%23%20latin%20writing%20script%0A%20%20%20%20%20%20%20%20%20%20wdt%3AP407%20wd%3AQ1860%3B%20%23%20With%20the%20property%20of%20english%20origin%0A%20%20%20%20%20%20%20%20%20%20wikibase%3Asitelinks%20%3Fsitelinks.%0A%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cmul%2Cen%22%20%7D%0A%7D%0AORDER%20BY%20DESC%28%3Fsitelinks%29")
        if response.status_code == 200:
            response = response.json() # data returned is a list of ‘repository’ entities
            length = len(response["results"]["bindings"])
            for i in range(length):
                writer.writerow({"given name": response["results"]["bindings"][i]["itemLabel"]["value"],
                                "gender": key})

