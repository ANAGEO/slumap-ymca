from osgeo import gdal
from osgeo import ogr
import os, sys
import geopandas
import json

def extract_coord(output_poly): #fonction pour extraire les coordonnées géographiques à partir d'un fichier json
    
    extract_json = json.loads(output_poly)
    coordinates = extract_json['coordinates']
    xmin = coordinates[0][0][0][0]
    xmax = coordinates[0][0][1][0]
    ymin = coordinates[0][0][0][1]
    ymax = coordinates[0][0][2][1]
    
    return xmin,xmax,ymin,ymax
    

#in_path = "/media/student/data1/docker-jupyter/Images/S1/"
#in_path_vect = "/media/student/data1/julien/sample/"
#raster_filename = "S1_VV_SMALL_"

#vector_filename = "sample_small.gpkg"

#format_file = ".tif"

vector = ogr.Open('Images/smaller/sample/sample_grid.gpkg') #ouverture de la fichier gkpg
layer = vector.GetLayer() #extraction des couches dans le gkpg dans ce cas-ci il n'y en a qu'une seule (sinon spécifier)
print(layer.GetExtent()) #affiche de l'emprise de la couche vectorielle

for feat in layer: #une boucle sur les polygones dans la couche vectorielle
    polygone = feat.GetGeometryRef().ExportToJson() #extraire les données géométriques et exporter en format JSON
    print(extract_coord(polygone)) #extraction des coordonnées des polygones
    poly_id = feat.GetField("id") #extraire le id de l'object
    lulc = feat.GetField("lulc") #extraire le lulc (si slum ou pas slum) de l'object

    print(str(poly_id))
    print(lulc)
    
#raster = gdal.Open(in_path+raster_filename+str(1)+format_file) #importation de la matrice

#vect = "ogrinfo /media/student/data1/julien/smaller/sample/sample_small.gpkg -al -fid 1"
