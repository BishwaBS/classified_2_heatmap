def classify_2_heatmap (classified_imgpath, class_of_interest, gridsize, eqn, eqn_type, percentc, savemappath):

    #importing required packages and modules
    import numpy as np
    import cv2
    import matplotlib.pyplot as plt
    from matplotlib.colors import from_levels_and_colors
    import sklearn
    from sklearn.preprocessing import MinMaxScaler
    import re
    import os
    
    #assigning variables to some of the the user-fed parameters
    n=int(gridsize)
    classid=class_of_interest

    if savemappath is not None:
        savemappath1=os.path.join(savemappath, "eqn_map.jpg")
        savemappath2 = os.path.join(savemappath, "percent_coverage.jpg")
        savemappath3 = os.path.join(savemappath, "combined.jpg")

    #loading the classified image in its original form
    img=cv2.imread(classified_imgpath, -1)
    a= img.shape[0]%n
    b= img.shape[1]%n

    #trimming the image to the dimension exactly divisible by n
    if a==0:
        x=img.shape[0]
    else:
        x=img.shape[0] - a

    if b==0:
        y=img.shape[1]
    else:
        y=img.shape[1] - b

    clip_img=img[0:x, 0:y]

    #calculating the number of grids in terms of nrows and ncols.
    nrows=int(clip_img.shape[0]/n)
    ncols=int(clip_img.shape[1]/n)

    #finding the column positions for the all the grids
    colidx=[]
    idx=0
    for t in range(ncols):
        idx=idx+n
        idx1 = idx - 1
        colidx.append(idx1)

    #finding the row positions for the all the grids
    rowidx=[]
    idx=0
    for t in range(nrows):
        # print(t)
        idx=idx+n
        idx1=idx-1
        rowidx.append(idx1)
    colidx.insert(0, 0)
    rowidx.insert(0, 0)

    #finding the frequency of the class of interest in each of the grids determined above
    freq=[]
    count = 0
    for i in range(len(rowidx)):
        for j in range(len(colidx)):
            count=0
            if i<len(rowidx)-1 and j<len(colidx)-1:
                for row in range(rowidx[i], rowidx[i+1]):
                    for col in range(colidx[j], colidx[j+1]):
                        # print(row)
                        if clip_img[row, col]==classid:
                            count+=1
            else:
                break
            freq.append(count)

    #Converting list of frequency to array and reshaping to the nrows and ncols
    freq_arr=np.array(freq)
    freq_arr=freq_arr.reshape((nrows, ncols))

    # Solving the equation fed by user where y would be the response variable user is looking
    # for and x would be the array of frequency obtained above
    if eqn is not None:
        if eqn_type =="simple_linear":
            text=eqn
            parts= re.findall(r"[0-9.]+|.", text)
            parts=list(filter(None, parts))
            parts=' '.join(parts).split()
            if len(parts)==8:
                m=float(parts[3])
                c=float(parts[7])
                m=-m
                if parts[6]=="-":
                    freq_arr1 = freq_arr * m - c
                    labeltext = "biomass(g) per grid"
                else:
                    freq_arr1 = freq_arr * m + c
                    labeltext = "biomass(g) per grid"
            else:
                m=float(parts[2])
                c=float(parts[6])
                if parts[5]=="-":
                    freq_arr1 = freq_arr * m - c
                    labeltext = "biomass(g) per grid"
                else:
                    freq_arr1 = freq_arr * m + c
                    labeltext = "biomass(g) per grid"

            if savemappath is not None:
                fig1, ax= plt.subplots(1,1)
                heatmap=ax.imshow(freq_arr1, cmap=plt.cm.Reds)
                cbar = fig1.colorbar(heatmap, ax=ax)
                cbar.set_label(labeltext)
                fig1.savefig(savemappath1)
                print("The map is saved successfully")

    #converting the array of frequency to the percentage cover if user assigns percentc=True.
    if percentc=="True":
        freq_arr2=freq_arr/ (n*n)*100
        labeltext1="% coverage per grid"
        fig2, ax = plt.subplots(1, 1)
        heatmap = ax.imshow(freq_arr2, cmap=plt.cm.Reds)
        cbar = fig2.colorbar(heatmap, ax=ax)
        cbar.set_label(labeltext1)
        fig2.savefig(savemappath2)
        print("The map is saved successfully")
    else:
        pass

    #plotting the maps together if conditions are met
    if eqn is not None and percentc=="True":
        fig3, ax = plt.subplots(2, 2, figsize=(15,15))
        ax[0,0].imshow(img)
        heatmap1 = ax[0,1].imshow(freq_arr, cmap=plt.cm.Reds)
        cbar = fig3.colorbar(heatmap1, ax=ax[0,1])
        cbar.set_label("# of pixels per grid ")
        heatmap2 = ax[1, 0].imshow(freq_arr2, cmap=plt.cm.Reds)
        cbar = fig3.colorbar(heatmap2, ax=ax[1,0])
        cbar.set_label(labeltext1)
        heatmap3 = ax[1,1].imshow(freq_arr1, cmap=plt.cm.Reds)
        cbar = fig3.colorbar(heatmap3, ax=ax[1,1])
        cbar.set_label(labeltext)
        fig3.savefig(savemappath3)
        print("The map is saved successfully")

    


#classify_2_heatmap ("..test\classified_image.jpg", 1, 10, "y=3.4*x+24" , "simple_linear", "True", "..test\output_folder")
