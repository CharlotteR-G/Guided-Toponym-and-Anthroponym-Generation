import bz2
import gzip
import ijson
import json
from decimal import Decimal

BATCHSIZE = 10000

# Deal with the Decimals in wikiData
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return super().default(obj)
    
# Extract all humans from WikiData bulk source
def extract_humans(bulkWikidataPath, outputPath="humans.json.gz"):
    count = 0
    firstItem = True

    with gzip.open(outputPath, "wt") as outfile:
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

                        # Tracker to check code still running
                        if count % BATCHSIZE == 0:
                            print(count)
                        
                        break

        outfile.write("]")

#extract_humans("latest-all.json.bz2")

with gzip.open("humans.json.gz", "rt") as data:
    for item in ijson.items(data, "item"):
        print(item.get("labels", {}).get("en", {}).get("value"))

