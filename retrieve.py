#!/usr/bin/env python3

'''Script that goes through a list of collections (NSIDC shortnames) and retrieves 
all the data products of that type, saving them to the mounted data directory under that shortname'''


import os
import time
import random
import json
import earthaccess


def retrieve_data(short_name=None, folder_path=None):
    if short_name == None:
        raise Exception('Must provide short_name for data product')
    
    # 1. Login to NASA Earthdata (creds should be in .netrc)
    earthaccess.login(persist=True)

    # If short_name is a list, recursively call retrieve_data for each item
    if isinstance(short_name, list):
        for sn in short_name:
            retrieve_data(short_name=sn)
        return  # Prevents further execution in the recursive calls
    if folder_path == None:
        folder_path = os.path.join('/data', short_name)

    print(f'querying for {short_name}')
    # 2. Search for product
    results = earthaccess.search_data(
        #provider='NSIDC',
        short_name=short_name,  # dataset
        #bounding_box=(-180, -90, 180, -60),  # Covers all of Antarctica
        #temporal=("2014-01", "2025-01"),  # Adjust temporal range as needed
        count=-1  # Number of results to fetch, -1 means all
    )
    print('found {} results...'.format(len(results)))

    # 3. Download files
    #downloaded_files = earthaccess.download(results, local_path=folder_path, threads=8)
    robust_download(results, folder_path, max_retries=5)

    # Save complete file
    with open(os.path.join(folder_path, 'collection.json'), 'w', encoding='utf-8') as file:
        file.write(json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False))


def robust_download(results, folder_path, max_retries=5):
    """Download files with retry logic in case of failures."""
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} to download...")
            downloaded_files = earthaccess.download(results, local_path=folder_path, threads=4)
            return downloaded_files  # If successful, return results
        except Exception as e:
            print(f"Download failed (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = random.uniform(5, 15)  # Random wait between 5-15 seconds
                print(f"Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Skipping.")
                return None  # Skip if retries fail

if __name__ == '__main__':
    collections = [
    'NSIDC-0478', # MEaSUREs Greenland Ice Sheet Velocity Map from InSAR Data V002
    'NSIDC-0484', # MEaSUREs InSAR-Based Antarctica Ice Velocity Map V002
    'NSIDC-0498', # MEaSUREs Antarctic Grounding Line from Differential Satellite Radar Interferometry V002
    'NSIDC-0525', # MEaSUREs InSAR-Based Ice Velocity Maps of Central Antarctica: 1997 and 2009 V001
    'NSIDC-0545', # MEaSUREs InSAR-Based Ice Velocity of the Amundsen Sea Embayment, Antarctica V001
    'NSIDC-0547', # MEaSUREs MODIS Mosaic of Greenland (MOG) 2005, 2010, and 2015 Image Maps V002
    'NSIDC-0645', # MEaSUREs Greenland Ice Mapping Project (GIMP) Digital Elevation Model V001
    'NSIDC-0670', # MEaSUREs Multi-year Greenland Ice Sheet Velocity Mosaic V001
    'NSIDC-0709', # MEaSUREs Antarctic Boundaries for IPY 2007-2009 from Satellite Radar V002
    'NSIDC-0713', # MEaSUREs Greenland Ice Mapping Project (GIMP) 2000 Image Mosaic V001
    'NSIDC-0714', # MEaSUREs Greenland Ice Mapping Project (GIMP) Land Ice and Ocean Classification Mask V001'
    'NSIDC-0715', # MEaSUREs Greenland Ice Mapping Project (GrIMP) Digital Elevation Model from GeoEye and WorldView Imagery V002
    'NSIDC-0720', # MEaSUREs Annual Antarctic Ice Velocity Maps V001
    'NSIDC-0723', # MEaSUREs Greenland Image Mosaics from Sentinel-1A and -1B V004
    'NSIDC-0725', # MEaSUREs Greenland Annual Ice Sheet Velocity Mosaics from SAR and Landsat V005
    'NSIDC-0727', # MEaSUREs Greenland Quarterly Ice Sheet Velocity Mosaics from SAR and Landsat V005
    'NSIDC-0731', # MEaSUREs Greenland Monthly Ice Sheet Velocity Mosaics from SAR and Landsat V005
    'NSIDC-0754', # MEaSUREs Phase-Based Antarctica Ice Velocity Map V001
    'NSIDC-0756', # MEaSUREs BedMachine Antarctica V003
    'NSIDC-0761', # MEaSUREs Multi-year Reference Velocity Maps of the Antarctic Ice Sheet V001
    'NSIDC-0776', # MEaSUREs ITS_LIVE Regional Glacier and Ice Sheet Surface Velocities, Version 1
    'NSIDC-0778', # MEaSUREs Grounding Zone of the Antarctic Ice Sheet V001
    'NSIDC-0782', # MEaSUREs ITS_LIVE Antarctic Grounded Ice Sheet Elevation Change V001
    'NSIDC-0792', # MEaSUREs ITS_LIVE Antarctic Quarterly 1920 m Ice Shelf Height Change and Basal Melt Rates, 1992-2017 V001'
    'NSIDC-0793', # MEaSUREs ITS_LIVE Greenland Monthly 120 m Ice Sheet Extent Masks, 1972-2022 V001
    'NSIDC-0794', # MEaSUREs ITS_LIVE Antarctic Annual 240 m Ice Sheet Extent Masks, 1997-2021 V001
    'IDBMG4', # IceBridge BedMachine Greenland V005
    'ASO_3M_PCDTM', # ASO L4 Lidar Point Cloud Digital Terrain Model 3m UTM Grid V001
    'ASO_3M_SD', # ASO L4 Lidar Snow Depth 3m UTM Grid V001
    'ASO_50M_SD', # ASO L4 Lidar Snow Depth 50m UTM Grid V001
    ]
    retrieve_data(short_name=collections)
    print('complete.')
