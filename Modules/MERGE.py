from osgeo import gdal, ogr

'''

This function automatically merge multiple rasters with a SINGLE band to a raster with multiple bands like RGB.
    Inputs :
        listRGBNIR : This input MUST be a list with the different SINGLE band raster that must be merged.
        output_dir : Is a string of the output directory. DO NOT FORGET to end the path with '/' Example : 'jgovoort/Images/S2/'
    Outputs :
        There is no output in Python. However, it will create a raster in GTiff format with all the merged bands in the indicate folder.
        
Contact : julien.govoorts@ulb.be

jgovoort

'''
def merge_RGBNIR(listRGBNIR,output_dir, output_name, format_name):
    gdal.BuildVRT("Images/RGBNIR.vrt",listRGBNIR, separate=True) #rassemble les 3 rasters à bande unique en un seul raster sous un format vrt
    output = output_dir+output_name+format_name
    gdal.Translate(output,"Images/RGBNIR.vrt", format='GTiff') #traduit le format vrt en format GTiff