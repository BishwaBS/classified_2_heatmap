# classified_2_heatmap
The python file consists of function that converts a classified image into heatmaps. The user would require to pass in the follwoing information:
1. input image path
2. class of interest for the heatmap (one may have multiple classes in classified images)
3. grid size as the number of pixels
4. simple linear equation such that x is number of the pixels corresponding to the class of interest at each grid. If the user doesn't have one, they can simply pass in None. 
5. Boolean information denoting if the user is interested in percent coverage; if interested, boolean should be passed as "True", else "False"
6. Output folder
