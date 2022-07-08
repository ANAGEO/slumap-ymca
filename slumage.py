from osgeo import gdal
from osgeo import ogr
import os, sys
import geopandas

in_path = "/media/student/data/docker-jupyter/Images/S1/decoup/"
in_path_vect = "/media/student/data/julien"
input_filename = "S1_VV_SMALL_"

format_file = ".tif"

raster = gdal.Open(in_path+input_filename+str(1)+format_file) #importation de la matrice


