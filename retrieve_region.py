#!/usr/bin/env python3

'''Same as retrieve.py script only it uses a shapefile to constrain the results'''

import os
import json
import geopandas as gpd
import earthaccess
import shapely
from shapely.geometry import mapping, Polygon, MultiPolygon

def save_polygon(gdf, output_path):
    gdf.to_file(output_path, driver="ESRI Shapefile")
    print(f"saved to {output_path}")

def get_geometry_wkt(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.to_crs(epsg=3031)  # Convert to WGS 84 for compatibility

    # Fix invalid geometries
    gdf["geometry"] = gdf["geometry"].buffer(0)

    # Merge all polygons into a single geometry
    merged_geom = shapely.ops.unary_union(gdf.geometry)
    merged_gdf = gpd.GeoDataFrame(geometry=[merged_geom], crs="EPSG:3031")
    save_polygon(merged_gdf, 'shapefiles/test.shp')
    return merged_gdf.unary_union.wkt

def round_sig(value, sig=6):
    return round(value, sig - len(str(int(abs(value))))) if value != 0 else 0

def extract_polygon_coordinates(shapefile_path):
    # Load the shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Ensure the geometries are in WGS84 (EPSG:4326) for lat/lon
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    
    polygon_list = []
    
    for geometry in gdf.geometry:
        if geometry.geom_type == 'MultiPolygon':
            for polygon in geometry.geoms:
                coords = list(polygon.exterior.coords)
                polygon_list.append([(round_sig(lon, 6), round_sig(lat, 6)) for lon, lat in coords])
        elif geometry.geom_type == 'Polygon':
            coords = list(geometry.exterior.coords)
            polygon_list.append([(round_sig(lon,6), round_sig(lat,6)) for lon, lat in coords])
    return polygon_list

def retrieve_data(short_name=None, folder_path=None, shapefile_path=None):
    if short_name is None:
        raise Exception('Must provide short_name for data product')

    # If short_name is a list, recursively call retrieve_data for each item
    if isinstance(short_name, list):
        for sn in short_name:
            retrieve_data(short_name=sn, folder_path=folder_path, shapefile_path=shapefile_path)
        return  # Prevents further execution in the recursive calls
    
    if folder_path is None:
        folder_path = os.path.join('/data', short_name)

    # 1. Login to NASA Earthdata (creds should be in .netrc)
    earthaccess.login(persist=True)

    print('querying for product: {}'.format(short_name))
    # 2. Get geometry from the shapefile
    spatial_filter = None
    if shapefile_path:
        coords = extract_polygon_coordinates(shapefile_path)
    print('found {} polygons in the shapefile... conducting queries...'.format(len(coords)))
    
    print(coords)
    # 3. Search for product using the polygon geometry
    results = earthaccess.search_data(
        short_name=short_name,  
        polygon=coords[0],  # Pass actual polygon instead of bounding box
        count=-1  # Fetch all results
    )
    print('found {} products... downloading files'.format(len(results)))

    # 4. Download files
    downloaded_files = earthaccess.download(results, local_path=folder_path, threads=8)

    # Save metadata as JSON
    with open(os.path.join(folder_path, 'collection.json'), 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4, sort_keys=True, ensure_ascii=False)

if __name__ == '__main__':
    collections = ['ATL14']#['ATL06'] 
    shapefile_path = "shapefiles/icesat_ross.shp"  # Path to your shapefile
    retrieve_data(collections, shapefile_path=shapefile_path)

