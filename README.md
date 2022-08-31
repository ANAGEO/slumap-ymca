# Welcome to the Read me of my jupyter on Docker
## This Git contains :
### Jupyter notebooks

- Preprocessing_Ymodel.ipynb : Notebook use to merge all the Sentinel-1/2 images and to clip it according to the grid and the validation/training patches.
- YMCA-kfold.ipynb : Model based on the given model of Rowel Atienza. It has been modified to reduce the overfitting and to work with the data. The pre-processing code has been modified to work with a kfolding.
- k-fold_processing.ipynb : A Jupyter notebook uses to create the kfold list.

### Python modules in MODULE

- stackage.py : A python homemade function that is used to create an array of raster data based on a list of path.
- chunkage.py : Python homemade function that warp an image from a vectorized grid.
- CircleMaker.py : Module uses to plot a pie plot to inspect the partition of test and validation patches.

## Other folders :

- CLUSTER : will desappear.
- CSV : corresponds to the outputs of previous models and run of the Ymodel.
- SRC : Python modules imported from https://github.com/tgrippa/Partimap.
- checkpoint : Checkpoints that contain the weight of each run of the model.
- ogr : will desappear.
- OutputCSV : corresponds to the outputs of the Ymodel-kfold.

## Background of the repository : 

This repository has been created in the frame of my intership at ANAGEO. Progressively, I will add more Python projects linked to the goal of my intership.

## Contact :

email : julien.govoorts@ulb.be

Name : Julien Govoorts
