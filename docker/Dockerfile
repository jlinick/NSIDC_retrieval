FROM osgeo/gdal:ubuntu-small-3.6.3
MAINTAINER jlinick@mit.edu

#ENV DEBIAN_FRONTEND=non-interactive

# Set the working directory
ENV CODE=/code
ENV DATA=/data
ENV PRODUCTS=/products
ENV WORKDIR=${CODE}

WORKDIR ${WORKDIR}
ENV HOME=${WORKDIR}

# Set the data directory
ENV DATA=/data

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
     python3-pip coreutils zip unzip git \
     vim imagemagick ffmpeg libgeos-dev wget curl

RUN pip3 install numpy scipy matplotlib h5py pyproj \
    scikit-learn scikit-image tqdm pint pymp-pypi \ 
    pint xarray pylint pandas simplekml pillow geopandas \
    netcdf4 setuptools dask h5netcdf numba bokeh cvxopt rasterio \
    fiona jupyter plotly jupyterlab earthaccess

RUN echo "PS1='🐳 \e[1;32m\]\u@\e[m\]\e[1;31m\]\h\e[m\]:\e[1;34m\]\w\e[m\]\\$ '" >> ~/.bashrc
