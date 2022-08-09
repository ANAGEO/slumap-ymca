import h5py

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np

from cv2 import cvtColor, COLOR_BGR2RGB

from osgeo import gdal
import numpy as np

from stackage import stackage

def normalise_01(image_data):
    stack = image_data
    image_data -= np.min(stack, axis=0)
    image_data /= (np.max(stack, axis=0) - np.min(stack, axis=0))
    return image_data

	
def Norma_Xpercentile(image_data, prct:int = 2, BGR2RGB=True):
	'''
	Function that perform x percent histogram equalization of RGB images display
	'''

	a = np.ndarray(image_data.shape, dtype='float32')  
	a[:,:,0] = (image_data[:,:,0] - np.nanpercentile(image_data[:,:,0],prct))/(np.nanpercentile(image_data[:,:,0],100-prct) - np.nanpercentile(image_data[:,:,0],prct))
	a[:,:,1] = (image_data[:,:,1] - np.nanpercentile(image_data[:,:,1],prct))/(np.nanpercentile(image_data[:,:,1],100-prct) - np.nanpercentile(image_data[:,:,1],prct))
	a[:,:,2] = (image_data[:,:,2] - np.nanpercentile(image_data[:,:,2],prct))/(np.nanpercentile(image_data[:,:,2],100-prct) - np.nanpercentile(image_data[:,:,2],prct))
	if BGR2RGB: 
		a = cvtColor(a, COLOR_BGR2RGB)
	return a



def assimilation(patch_id_train, patch_id_test, patch_lulc_test,path_raster):
    train_path = [None] * 10
    test_path = [None] * 10

    patch_id_train_re = patch_id_train.reshape(1,patch_id_train.size)
    patch_id_train_list = patch_id_train_re.tolist()[0]
    patch_id_test_re = patch_id_test.reshape(1,patch_id_test.size)
    patch_id_test_list = patch_id_test_re.tolist()[0]
    
    train_path = [None] * len(patch_id_train)
    test_path = [None] * len(patch_id_test)
    
    for path in path_raster : #récupération des id des images
        image = path.split(b'/')[-1]
        image_id = int(image.split(b'_')[-2])
        if image_id in patch_id_train_list :
            index = patch_id_train_list.index(int(image_id))
            train_path[index] = path
        elif image_id in patch_id_test_list :
            index = patch_id_test_list.index(int(image_id))
            test_path[index] = path

    #stack = stackage(train_path)

    stack_train = stackage(train_path)
    #stack = stackage(test_path)
    stack_test = stackage(test_path)

    
    plt.rcParams["figure.facecolor"] = 'w'
    plt.figure(figsize=(15, 15))
    for i in range(3):
        rd_img = np.random.randint(1,300)
        ax = plt.subplot(1, 3, i + 1)
        plt.imshow(Norma_Xpercentile(stack_test[rd_img,:,:,:]))
        plt.axis("off")
        plt.title("Random indx: %s\nID: %s\nlulc: %0.3f" %(rd_img,patch_id_test[rd_img],patch_lulc_test[rd_img]))
        print(stack_test[rd_img,0,0,:])
        print(test_path[rd_img])
        print(patch_id_test[rd_img])
    #plt.subplots_adjust(hspace=0.001)
    plt.tight_layout() 
    
    stack_train = normalise_01(stack_train)
    stack_test = normalise_01(stack_test)


    return stack_train, stack_test