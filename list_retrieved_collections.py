#!/usr/bin/env python3

import os
from earthaccess import DataCollections

def test():
    query = DataCollections().daac("NSIDC").cloud_hosted(False)
    query.hits()
    collections = query.get()
    
    retrieved_collections = []
    with open("/data/retrieved_collections.txt", "w") as f:

        for col in collections:
            shortname = col["umm"]["ShortName"]
            longname = col["umm"]["EntryTitle"]
            summary = col["umm"]["Abstract"]
            
            # Check if the directory exists
            if os.path.exists(f"/data/{shortname}"):
                print(f"{shortname:<12} : {longname}")
                f.write(f"{shortname} : {longname}\n")
                with open(f"/data/{shortname}/info.txt", "w") as f2:
                    f2.write(f"{shortname} : {longname}\n\n{summary}")

if __name__ == '__main__':
    test()

