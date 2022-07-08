from osgeo import gdal 
import os, sys
import subprocess

in_path = "/media/student/data/docker-jupyter/Images/S1/"
input_filename = "s1_vv_small.tif"

out_path = "/media/student/data/docker-jupyter/Images/S1/decoup/"
output_filename = 'S1_VV_SMALL_'

dset = gdal.Open(in_path+input_filename) #importation de la matrice

size_X = dset.RasterXSize #taille du raster importer selon X
size_Y = dset.RasterYSize #selon Y

chunck_size = 10 #définition de la taille des chucnks qui dans le cas de base 10x10

print(size_X)
print(size_Y)

k=0

for i in range(0, size_X, chunck_size):
    for j in range(0, size_Y, chunck_size):
        k+=1
        com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(chunck_size) + ", " + str(chunck_size) + " " + str(in_path) + str(input_filename) + " " + str(out_path) + str(output_filename) + str(k) + ".tif"
        os.system(com_string)

print('fini')

