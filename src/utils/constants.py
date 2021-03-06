# -----------------------------------------------------------------------
# Author: Marcelo Villa-Piñeros
#
# Purpose: Contains constants used by several scripts in the project.
# -----------------------------------------------------------------------
import os

# Earthdata's username and password. Either create the respective
# environment variables or change these two lines with your credentials.
EARTHDATA_USERNAME = os.environ.get("EARTHDATA_USERNAME")
EARTHDATA_PASSWORD = os.environ.get("EARTHDATA_PASSWORD")

# Dictionary with paths to save the files of an AppEEARS task. The number
# of elements in the dictionary has to be the same of tasks that are
# going to be submitted and each key should correspond to a task name.
SAVE_PATHS = {"MCD64A1": "data/nc/MODIS/MCD64A1"}

REGIONS = [
    {"name": "orinoquia", "path": "data/shp/regions/orinoquia.shp"},
    {"name": "flooded", "path": "data/shp/regions/flooded.shp"},
    {"name": "highland", "path": "data/shp/regions/highland.shp"},
    {"name": "dissected", "path": "data/shp/regions/dissected.shp"}
]

# Factor to multiply number of pixels with and compute an area measure.
# Each pixel is 500 x 500 meters and it can be then divided by another
# constant to obtain hectares, square kilometers or any other unit.
AREA_FACTOR = (500 * 500) / 10000

NODATA_VALUE = -9999

BURNED_AREA_THRESHOLD = 0.8

# Download link for Landsat's World Reference System-2 descending
# (daytime) grid.
WRS2_DESCENDING_GRID_URL = "https://prd-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/WRS2_descending_0.zip"

S3_LANDSAT8_SCENE_LIST_URL = "http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz"

# Landsat 8 acquisition date start and end in the year-month-day
# format.
L8_START_DATE = "2017-12-01"
L8_END_DATE = "2018-03-31"

L8_CLOUD_THRESHOLD = 10

L8_BANDS = ("B1", "B2", "B3", "B4", "B5", "B6", "B7")

L8_NODATA_VALUE = 0

FILTER_NEIGHBOURS = 9

AREA_THRESHOLD = 250000

ACCESSIBILITY_FEATURES = [
    {"name": "popc", "path": "data/shp/accessibility/popc.shp"},
    {"name": "rivers", "path": "data/shp/accessibility/rivers.shp"},
    {"name": "roads", "path": "data/shp/accessibility/roads.shp"}
]

DISTANCE_FACTOR = 0.5

DICTIONARY = {
    "popc": "cpob",
    "rivers": "rios",
    "roads": "vias",
    "comb": "comb",
    "orinoquia": "orinoquia",
    "flooded": "inundables",
    "highland": "altillanura",
    "dissected": "distectadas"
}

RECLASSIFY_MAP = {
    0: 255,
    1: 0,
    2: 1,
    3: 2,
    4: 4,
    5: 5,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 3,
    12: 1,
    13: 255
}

LANDCOVER_MAP = {
    0: "Other",
    1: "Forest",
    2: "Annual cropland",
    3: "Perennial cropland",
    4: "Savanna",
    5: "Grassland"
}

LANDCOVER_COLORS = {
    "Forest": "#01665e",
    "Cropland": "#dfc27d",
    "Savanna": "#f6e8c3",
    "Grassland": "#35978f",
    "Other": "#455a64"
}

LANDCOVER_PADDING = 2

LANDCOVER_PERIODS = [
    ("2000", "2005"),
    ("2005", "2010"),
    ("2010", "2016")
]

SANKEY_ALPHA = 0.6

MCD64A1_RESOLUTION = 0.004166666883983575
GRID_RESOLUTION = MCD64A1_RESOLUTION * 2 * 11
GRID_AREA_THRESHOLD = 0.8
SAMPLING_PROPORTION = 0.25
RANDOM_SEED = 42
