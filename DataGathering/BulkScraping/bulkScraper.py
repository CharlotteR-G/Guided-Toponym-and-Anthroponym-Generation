import bz2
import ijson
import json
from decimal import Decimal

BATCHSIZE = 1000

# Deal with the Decimals in wikiData
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return super().default(obj)
    
# Extract all humans from WikiData bulk source
def extract_humans(bulkWikidataPath, outputPath="humans.json"):
    count = 0
    firstItem = True

    with open(outputPath, "w") as outfile:
        outfile.write("[")

        with bz2.open(bulkWikidataPath, "rt") as data:
            for item in ijson.items(data, "item"):
                # If type is property, move on
                if item["type"] == "property":
                    continue

                # make sure item has instance of property
                if not item.get("claims", {}).get("P31", []):
                    continue

                # get id and check item is human
                itemInstances = item.get("claims", {}).get("P31", [])
                for instance in itemInstances:
                    # go through all claims and find if any match human
                    if instance.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q5":
                        # if human
                        if not firstItem:
                            outfile.write(",")
                        json.dump(item, outfile, cls=DecimalEncoder, indent=2)

                        firstItem = False

                        count += 1
                        break

                if count % BATCHSIZE == 0:
                    print(count)

                if count == 5000:
                    break

        outfile.write("]")

extract_humans("latest-all.json.bz2")

with open("humans.json", "r") as data:
    for item in ijson.items(data, "item"):
        print(item.get("labels", {}).get("en", {}).get("value"))





# Extracting every human and all relevant information to make
# Scrppaing faster when finding more specific information
# like names
# def extract_humans(bulkWikidataPath, outputPath="humans.json"):
#     humanBatch = []
#     count = 0
#     firstItem = True

#     with open(outputPath, "w") as outfile:

#         with bz2.open(bulkWikidataPath, "rt") as data:
#             for item in ijson.items(data, "item"):

#                 # If type is property, move on
#                 if item["type"] == "property":
#                     continue

#                 # make sure item has instance of property
#                 if not item.get("claims", {}).get("P31", []):
#                     continue

#                 # get id and check item is human
#                 itemInstances = item.get("claims", {}).get("P31", [])
#                 for instance in itemInstances:
#                     # go through all claims and find if any match human
#                     if instance.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q5":
#                         # if human
#                         humanBatch.append(item)
#                         count += 1
#                         break
                
#                 # Every 1000 humans
#                 if len(humanBatch) == BATCHSIZE:
#                     if not firstItem:
#                         outfile.write(",")
#                     json.dump(humanBatch, outfile, cls=DecimalEncoder, indent=2)
#                     firstItem = False
#                     print(count)
#                     humanBatch.clear()
#                     if count >= 50:
#                         break

#             # handle final batch
#             # if humanBatch:
#             #     if not firstItem:
#             #         outfile.write(",")
#             #     json.dump(humanBatch, outfile, cls=DecimalEncoder, indent=2)

#             # instances = claims.get("P31", [])
#             # for instance in instances:
#             #     id = instance.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
#             #     # isHuman = True if id == "Q5" else False # Q5 == human

#             #     if id == "Q5": # if human
#             #         # append relevant data to
#             #         # Convert sex qualifier to human readable
#             #         # print(item.get("labels", {}).get("en", {}).get("value"))

#             #         # Ensure person has a sex listed
#             #         if not item.get("claims", {}).get("P21", []):
#             #             break

#             #         sexID = item.get("claims", {}).get("P21", [])[0].get("mainsnak", {}).get("datavalue", {}).get("value", {}). get("id")
#             #         sex = "male" if sexID == "Q6581097" else "female"

#             #         humanData = {
#             #             "id": item.get("id"),
#             #             "name": item.get("labels", {}).get("en", {}).get("value"),
#             #             "sex": sex
#             #         }

#             #         humans.append(humanData)
#             #         count += 1
#             #         break
#             # if count % 10000 == 0:
#             #     print(count)

#     # with open(outputPath, "w") as outfile:
#     #     json.dump(humans, outfile, indent=2)
#     #     print(count)

        
