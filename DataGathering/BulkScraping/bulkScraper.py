import bz2
import ijson
import json

# Extracting every human and all relevant information to make
# Scrppaing faster when finding more specific information
# like names
def extract_humans(bulkWikidataPath, outputPath="humans.json"):
    humans = []
    count = 0

    with bz2.open(bulkWikidataPath, "rt") as data:
        for item in ijson.items(data, "item"):
            claims = item.get("claims", {})
            instances = claims.get("P31", [])
            for instance in instances:
                id = instance.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
                # isHuman = True if id == "Q5" else False # Q5 == human

                if id == "Q5": # if human
                    # append relevant data to

                    # Convert sex qualifier to human readable
                    print(item.get("labels", {}).get("en", {}).get("value"))

                    # Ensure person has a sex listed
                    if not item.get("claims", {}).get("P21", []):
                        break

                    sexID = item.get("claims", {}).get("P21", [])[0].get("mainsnak", {}).get("datavalue", {}).get("value", {}). get("id")
                    sex = "male" if sexID == "Q6581097" else "female"

                    humanData = {
                        "id": item.get("id"),
                        "name": item.get("labels", {}).get("en", {}).get("value"),
                        "sex": sex
                    }

                    humans.append(humanData)
                    count += 1
                    break
            # if count == 5:
            #     break

    with open(outputPath, "w") as outfile:
        json.dump(humans, outfile, indent=2)
        print(count)

            

extract_humans("latest-all.json.bz2")
