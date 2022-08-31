'''
This python module is build to create accuracy and loss plot from the multi-histories model save in a merging list HISTALL.

Inputs :
    - List with all the histories of the deep learning tensorflow model 

Name : Julien Govoorts
Contact : julien.govoorts@ulb.be/@gmail.com
This module is coming from : https://github.com/jgovoort/docker-jupyter

'''

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np

def plotandcsv_history_kfold(HISTALL, idx, vvvh) :
    
    if idx == 'ALL' :
        for i in range(len(HISTALL)) :
            plotandcsv_history_kfold(HISTALL, i, vvvh)
    else :
        
        if vvvh == 1 :
            IMAGENAME = ['VVVH_BNIR','VVVH_RNIR','VVVH_RGBNIR']
        elif vvvh == 0 : 
            IMAGENAME = ['BNIR','RNIR','RGBNIR']
        
        
        MINLOSS = []
        MAXLOSS = []
        MINVALLOSS = []
        MAXVALLOSS = []
        MINACC = []
        MAXACC = []
        MINVALACC = []
        MAXVALACC = []

        LENLIST  = []
        
        CSVLOSS = []
        CSVVALLOSS = []
        CSVACC = []
        CSVVALACC = []

        for history in HISTALL[idx] :
            LENLIST.append(len(history.history["loss"]))

        maxlen = max(LENLIST)
        
        # Create list with same length that the largest Kfold

        LOSS = [[] for _ in range(maxlen)]
        VALLOSS = [[] for _ in range(maxlen)]
        ACC = [[] for _ in range(maxlen)]
        VALACC = [[] for _ in range(maxlen)]
        
        # Append the value of loss and accuracy of each kfold for every epochs

        for history in HISTALL[idx] :
            
            lenlist = len(history.history["loss"])
            CSVLOSS.append(history.history["loss"])
            CSVVALLOSS.append(history.history["val_loss"])
            CSVACC.append(history.history["accuracy"])
            CSVVALACC.append(history.history["loss"])
            
            for j in range(lenlist) :
                LOSS[j].append(history.history["loss"][j])
                VALLOSS[j].append(history.history["val_loss"][j])
                ACC[j].append(history.history["accuracy"][j])
                VALACC[j].append(history.history["val_accuracy"][j])
                
        # Append the min and max value for loss and accuracy

        for j in range(maxlen) :
            MINLOSS.append(min(LOSS[j]))
            MAXLOSS.append(max(LOSS[j]))

            MINVALLOSS.append(min(VALLOSS[j]))
            MAXVALLOSS.append(max(VALLOSS[j]))

            MINACC.append(min(ACC[j]))
            MAXACC.append(max(ACC[j]))

            MINVALACC.append(min(VALACC[j]))
            MAXVALACC.append(max(VALACC[j]))

        xfit = list(range(0, maxlen))
        
        # Mean the loss of each epoch

        loss = list(map(np.mean, LOSS ))
        valloss = list(map(np.mean, VALLOSS ))
        
        # plotting

        f = plt.figure(figsize = (20,10))

        plt.plot(loss)
        plt.fill_between(xfit,MINLOSS, MAXLOSS, # Standard deviation of training loss
                         color='blue', alpha=0.2)
        plt.plot(valloss)
        plt.fill_between(xfit,MINVALLOSS, MAXVALLOSS, # Standard deviation of validation loss
                         color='orange', alpha=0.2)
        plt.xlabel('Epochs')
        plt.ylabel('Mean loss')
        plt.legend(['Mean : Training loss','Training loss standard deviation','Mean : Validation loss', 'Validation loss standard deviation'], title = "Legend")
        plt.title('Validation and training loss for the dataset '+str(IMAGENAME[idx]))
        plt.savefig('outputCSV/fig/LOSS_'+str(IMAGENAME[idx])+'.png')
        plt.show()
        

        f = plt.figure(figsize = (20,10))
        
        # Mean the accuracy of each epoch

        acc = list(map(np.mean, ACC ))
        valacc = list(map(np.mean, VALACC ))
        
        # plotting

        plt.plot(acc)
        plt.fill_between(xfit,MINACC, MAXACC, # Standard deviation of training accuracy
                         color='blue', alpha=0.2)
        plt.plot(valacc)
        plt.fill_between(xfit,MINVALACC, MAXVALACC, # Standard deviation of validation accuracy
                         color='orange', alpha=0.2)
        plt.xlabel('Epochs')
        plt.ylabel('Mean accuracy')
        plt.title('Validation and training accuracy for the dataset '+str(IMAGENAME[idx]))
        plt.legend(['Mean : Training accuracy','Training accuracy standard deviation','Mean : Validation accuracy', 'Validation accuracy standard deviation'], title = "Legend")
        plt.savefig('outputCSV/fig/ACC_'+str(IMAGENAME[idx])+'.png')
        plt.show()
        
