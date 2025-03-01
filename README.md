
# NSIDC_retrieval

Lightweight scripts to enable bulk retrieval of various data products from the NSIDC


## Setup

Make the directory to house your data, either `"/home/${USERNAME}/data/nsidc"` (Linux) or `"/Users/${USERNAME}/data/${REPO}"` (Mac), or update `LOCAL_DATA_DIR` in `run_container.sh` to the path you want to save the products.

You will need an [Earthdata](https://search.earthdata.nasa.gov/search) username and password. I suggest adding them to your .netrc (which is imported into the Docker container) but the script will prompt you for it if it doesn't find the credentials. This would be
```bash
machine urs.earthdata.nasa.gov
username <your_username>
password <your_password>
```
## Running the Script
To start, run the command
```bash
./run_container.sh
```
This uses [Docker](https://www.docker.com) to build the `nsidc:0.0.1` image and will then jump you into a running container.

## Usage

```bash
./retrieve.py
```
Will retrieve the NSIDC shortname products listed at the bottom of the script.

```bash
./retrieve_region.py
```
Will retrieve NSIDC shortname products listed at the bottom of the script, using a input shapefile to constrain the results.

```bash
./list_collections.py
```
Will return all the available collections on the NSIDC by shortname.

```bash
./list_retrieved_collections.py
```
Will compile a list of the collections that have been retrieved, full or in-part, and save the shortname summaries in their respective collections subfolder.

