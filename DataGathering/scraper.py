import requests
import csv

GENDERS = {
    "Female": "Q11879590",
    "Male": "Q12308941"
}

CULTURES = {
    "English": "Q1860",
    "German": "Q1860",
    "Spanish": "Q1321",
    "French": "Q150"
}

with open("names.csv", "w", newline="") as csvfile:
    fieldnames = ["given name", "gender", "culture"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through cultures and genders
    for cultureKey, cultureValue in CULTURES.items():
        for genderKey, genderValue in GENDERS.items():
            response = requests.get(f"https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query=SELECT%20DISTINCT%20%3FitemLabel%0AWHERE%20%7B%0A%20%20%20%20%3Fitem%20wdt%3AP31%20wd%3A{genderValue}%3B%20%23%20Any%20instance%20of%20{genderKey}%0A%20%20%20%20%20%20%20%20%20%20wdt%3AP282%20wd%3AQ8229%3B%20%23%20latin%20writing%20script%0A%20%20%20%20%20%20%20%20%20%20wdt%3AP407%20wd%3A{cultureValue}%3B%20%23%20With%20the%20property%20of%20english%20origin%0A%20%20%20%20%20%20%20%20%20%20wikibase%3Asitelinks%20%3Fsitelinks.%0A%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cmul%2Cen%22%20%7D%0A%7D%0AORDER%20BY%20DESC%28%3Fsitelinks%29")
            
            if response.status_code == 200:
                response = response.json() # data returned is a list of ‘repository’ entities
                length = len(response["results"]["bindings"])

                for i in range(length):
                    writer.writerow({"given name": response["results"]["bindings"][i]["itemLabel"]["value"],
                                    "gender": genderKey,
                                    "culture": cultureKey})

