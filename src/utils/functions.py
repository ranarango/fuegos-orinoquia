# -----------------------------------------------------------------------
# Author: Marcelo Villa-Piñeros
#
# Purpose: Contains functions used by different scripts in the project.
# -----------------------------------------------------------------------
import cgi
import os
import zipfile
from typing import Union

import numpy as np
import requests
from osgeo import gdal


def array_to_geotiff(
    arr: np.ndarray,
    fn: str,
    sr: str,
    gt: Union[list, tuple],
    gdtype: int,
    nd_val: float = None,
    options: list = [],
) -> None:
    """
    Writes a 2D or 3D NumPy array to a GeoTIFF file in disk.

    Parameters
    ----------
    arr:     d2D or 3D array.
    fn:      output GeoTIFF's file name.
    sr:      output GeoTIFF's spatial reference in a WKT string.
    gt:      output GeoTIFF's geotransform.
    gdtype:  GDAL data type.
    nd_val:  output GeoTIFF's NoData value.
    options: GDAL creation options.

    Returns
    -------
    None
    """
    assert 2 <= len(arr.shape) <= 3, "arr must have either 2 or 3 dimensions"

    # Get array dimensions to define number of bands, columns and rows
    # of output GeoTIFF file.
    bands = arr.shape[0] if len(arr.shape) == 3 else 1
    cols = arr.shape[-1]
    rows = arr.shape[-2]

    # Create empty GeoTIFF.
    driver = gdal.GetDriverByName("GTiff")
    out_tif = driver.Create(fn, cols, rows, bands, gdtype, options)

    # Set projection and geotransform.
    out_tif.SetProjection(sr)
    out_tif.SetGeoTransform(gt)

    # set NoData value and write data.
    band = out_tif.GetRasterBand(1)
    if nd_val:
        band.SetNoDataValue(nd_val)
    band.WriteArray(arr)

    # Save file.
    band.FlushCache()
    del band, out_tif


def download_http_file(url: str, save_to: str = None) -> str:
    """
    Downloads a file using the HTTP(S) protocol.

    Parameters
    ----------
    url:     HTTP(S) URL with the downloadable file.
    save_to: optional path to folder (e.g. /home/foo) or file
             (e.g. /home/foo/bar.txt). If a path to a folder is passed,
             the file is saved to that folder using the original filename
             from the headers of the file or from the URL. If a path to
             a file is passed, the file will be saved to that path using
             the given filename, ignoring the original filename. If nothing
             is passed, the file will be saved to the current working
             directory with the original filename.

    Returns
    -------
    Relative path of the saved file.

    Notes
    -----
    This function has been slightly adapted from:
    https://stackoverflow.com/a/53153505/7144368
    """
    try:
        with requests.get(url, stream=True) as r:

            r.raise_for_status()

            # Take filename from headers if possible
            cd = r.headers.get("Content-Disposition")
            if cd:
                fn = cgi.parse_header(cd)[1]["filename"]
            else:
                fn = url.split("/")[-1]

            # Define output path in case it is a directory or it is not given
            if not save_to:
                save_to = os.path.join(".", fn)
            else:
                if os.path.isdir(save_to):
                    save_to = os.path.join(save_to, fn)

            with open(save_to, "wb") as file:
                for chunk in r.iter_content(chunk_size=1024):
                    file.write(chunk)

            return save_to

    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error while downloading task. {err}")


def unzip_file(src: str, dst: str) -> None:
    """
    Unzips zip files.

    Parameters
    ----------
    src: source zipped file.
    dst: target directory.

    Returns
    -------
    None
    """
    ext = os.path.splitext(src)[1]

    if ext == '.zip':
        with zipfile.ZipFile(src, 'r') as zip_ref:
            zip_ref.extractall(dst)
    else:
        raise NotImplementedError
