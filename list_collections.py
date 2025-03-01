#!/usr/bin/env python3

'''Prints the NSIDC data collections, along with associated shortnames and data
products'''

from earthaccess import DataCollections

def test():
    # We only need to specify the DAAC and if we're looking for cloud hosted data
    query = DataCollections().daac("NSIDC").cloud_hosted(False)
    # we use hits to get a count for the collections that match our query
    query.hits()
    # Now we get the collections' metadata
    collections = query.get()

    for col in collections:
        shortname = col["umm"]["ShortName"]
        longname = col["umm"]["EntryTitle"]
        summary = col["umm"]["Abstract"] 
        #print(shortname, ':', longname)
        print(f"{shortname:<{12}} : {longname}")

if __name__ == '__main__':
    test()
