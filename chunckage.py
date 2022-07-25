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


def chunckage(folder_raster,filename_raster,format_rast,folder_vector, filename_vector, output_name, lulc_yes):
    
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
            poly_id = int(feat.GetField("id")) #extraire le id de l'object
            #print(poly_id)
            
            if lulc_yes == 1 : 
                lulc = int(feat.GetField("lulc")) #extraire le lulc (si slum ou pas slum) de l'object
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