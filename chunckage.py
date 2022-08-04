'''
This module has been coded to warp raster images from a GeoPackage. It contains two functions : extract_coord() that extracts coordinates from the GeoPackage and chunkage() that warps the raster.

Inputs of chunckage()

folder_raster : Directory of the raster that must be warped AND the directory of the warped rasters --> MUST BE A STRING (e.g. "/home/libraries/")
filename_raster : Name of the raster that must be warped --> MUST BE A STRING (e.g. "raster")
format_rast : Format of the raster that must be warped  --> MUST BE A STRING (e.g. ".tif")

folder_vector : Directory of the vector that is used to warp the raster --> MUST BE A STRING (e.g. "/home/vector/")
filename_vector : Name of the vector with its extension that is used to warp the raster --> MUST BE A STRING AND MUST BE A GEOPACKAGE (.gpkg) (e.g. "vector.gpkg")

output_name : Part of the name of the output warped rasters --> MUST BE A STRING

id_field : Name of the field that contains the id of the object in the vectorfile --> MUST BE A STRING
lulc_field : Name of the field that contains the label of the object in the vectorfile --> MUST BE A STRING

lulc_yes : Take 0 --> The module DO NOT extract the values in the lulc_field
                        Example of a warped raster name :
                            (output_name)_(id_field)
                                   raster_1234.tif
           Take 1 --> The module extract the values in the lulc_field
                            (output_name)_(id_field)_(lulc_field)
                                   raster_1234_0.tif

Outputs of chunckage()

if lulc_yes == 0 :
    listvrt :  A list that contains the path of each raster
    patch_id :  A list that contains the id of each raster
    
if lulc_yes == 1 :
    The same output as lulc_yes == 0 more :
       patch_lulc :  A list that contains the label of each raster
       
       
This module as been created in the frame of an internship at ANAGEO Labs (Université Libre de Bruxelles) :
    https://cvchercheurs.ulb.ac.be/Site/unite/ULB568UK.php
    https://github.com/ANAGEO
    
Name : Julien Govoorts
Contact : julien.govoorts@ulb.be or gmail.com
This module is coming from : https://github.com/jgovoort/docker-jupyter

'''


from osgeo import gdal
from osgeo import ogr
import os, sys
import numpy as np
import json

def extract_coord(output_poly): #fonction pour extraire les coordonnées géographiques à partir d'un fichier json
    
    extract_json = json.loads(output_poly) #convertion de l'input dans le format json
    coordinates = extract_json['coordinates'] #extraction des coordonnées
    #extraction des coordonnées nécessaire selon la structure des données json
    xmin = coordinates[0][0][0][0]
    xmax = coordinates[0][0][1][0]
    ymin = coordinates[0][0][0][1]
    ymax = coordinates[0][0][2][1]
    
    return xmin,ymin,xmax,ymax


def chunckage(folder_raster,filename_raster,format_rast,folder_vector, filename_vector, output_name, id_field, lulc_field, lulc_yes):
    
    rast = gdal.Open(folder_raster+filename_raster+format_rast) #ouverture du raster

    vector = ogr.Open(folder_vector+filename_vector) #ouverture de la fichier gkpg

    layer = vector.GetLayer() #extraction des couches dans le gkpg dans ce cas-ci il n'y en a qu'une seule (sinon spécifier)

    print(layer.GetExtent()) #affiche de l'emprise de la couche vectorielle
   
    os.system('mkdir ./'+folder_raster+output_name+'_patch') #création automatique de la directory pour enregistrer les patchs
    
    #étape d'initialisation de la boucle
    patch_id = [] #création des matrices
    patch_lulc = []
    listvrt = []

    for feat in layer: #une boucle sur les polygones dans la couche vectorielle
            polygone = feat.GetGeometryRef().ExportToJson() #extraire les données géométriques et exporter en format JSON
            list_coord = extract_coord(polygone) #extraction des coordonnées des polygones
            #print(list_coord)
            poly_id = int(feat.GetField(id_field)) #extraire le id de l'object
            #print(poly_id)
            
            if lulc_yes == 1 : 
                lulc = int(feat.GetField(lulc_field)) #extraire le lulc (si slum ou pas slum) de l'object
                name_file= output_name+'_'+str(poly_id)+'_'+str(lulc)+'.tif' #création du nom du fichier de sortie
                patch_lulc.append(lulc) #enregistrement dans une liste si le patch est un slum ou pas
            elif lulc_yes == 0 :
                name_file= output_name+'_'+str(poly_id)+'.tif' #création du nom du fichier de sortie
            
            filename = folder_raster+output_name+'_patch/'+str(name_file)
            gdal.Warp(str(filename),rast, outputBounds = list_coord) #division en petite tuile correspondante aux polygone dans le shpfile
            listvrt.append(filename) #enregistremet dans une liste le chemin des patchs
            
            patch_id.append(poly_id) #enregistrement dans une liste l'id du patch
            

    if lulc_yes == 1 :         
        return listvrt, patch_id, patch_lulc
    elif lulc_yes == 0 : 
        return listvrt, patch_id