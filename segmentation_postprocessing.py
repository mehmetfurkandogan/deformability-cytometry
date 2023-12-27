# This script is used to postprocess the segmentation results and calculate the deformation metrics.
######################################################################## IMPORT LIBRARIES
from halo import Halo
spinner = Halo(text='Importing libraries... ', text_color= 'magenta', color='magenta', spinner='dots')
spinner.start()
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import tifffile
import csv
spinner.stop()
######################################################################## FUNCTION DEFINITIONS
def postprocess(input_movie_path,output_csv_file):
    # Intializing
    # Read the input TIFF stack
    tiff_stack = tifffile.imread(input_movie_path)
    # Get TIFF stack properties
    num_frames, height, width = tiff_stack.shape
    # Initialize the CSV file
    with open(output_csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['Frame Index', 'Area (microns^2)',
                             'Centroid X (microns)', 'Centroid Y (microns)',
                             'Width (microns)', 'Height (microns)',
                             'Aspect Ratio', 'Solidity'])
    # Initialize counters
    zero_cell_counter = 0
    one_cell_counter = 0
    multiple_cell_counter = 0
    wrong_contour_counter = 0
    # constants
    pixel_size = 10 # microns

    # Loop through each frame
    for i, frame in tqdm(enumerate(tiff_stack),total=num_frames):
        unique_values = np.unique(frame)
        if len(unique_values)==1:
            zero_cell_counter+=1
            continue
        elif len(unique_values)==2:
            # Count the number of elements with value 1
            one_cell_counter+=1
            # Calculate the area of the cell
            cell_area = np.sum(frame == 1)*pixel_size*pixel_size
            # Find the area and the centroid of the cell
            M = cv2.moments(frame)
            cell_area = M['m00']*pixel_size*pixel_size
            cell_centroid_x = int(M['m10']/M['m00'])
            cell_centroid_y = int(M['m01']/M['m00'])
            # Calculate deformation metrics
            contours, _ = cv2.findContours(frame.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                # Aspect ratio
                x,y,w,h = cv2.boundingRect(cnt)
                aspect_ratio = float(w)/h
                # Solidity
                area = cv2.contourArea(cnt)
                if area == 0:
                    wrong_contour_counter+=1
                    continue
                hull = cv2.convexHull(cnt)
                hull_area = cv2.contourArea(hull)
                solidity = float(area)/hull_area
            # save in csv file
            with open(output_csv_file, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([i,cell_area,cell_centroid_x*pixel_size,cell_centroid_y*pixel_size,
                                    w*pixel_size,h*pixel_size,
                                    round(aspect_ratio,4),round(solidity,4)])
        else:
            multiple_cell_counter+=1
            continue
    # Print the statistics
    print('Frames with none or multiple cells are ignored.')
    print('Number of frames with 1 cell (%): ', "{:.2f}".format(one_cell_counter/num_frames*100))
    print('Number of frames with 0 cell (%): ', "{:.2f}".format(zero_cell_counter/num_frames*100))
    print('Number of frames with multiple cells (%): ', "{:.2f}".format(multiple_cell_counter/num_frames*100))
    print('Number of frames with wrong contour (%): ', "{:.2f}\n".format(wrong_contour_counter/num_frames*100))

######################################################################## MAIN
    
# List of all input and output paths
input_video_names = ['CellA_GFP',
                     'CellA_ShME480',
                     'CellB_GFP',
                     'CellB_ME480']
# Prepare the input video paths using the list above
input_video_paths = []
output_csv_files = []
for input_video_name in input_video_names:
    input_video_paths.append('Results\PartC\\'+input_video_name+'_segmented.tif')
    output_csv_files.append('Results\PartC\\'+input_video_name+'.csv')

# Run the postprocessing function for each video
for i in range(len(input_video_paths)):
    print('Processing',input_video_names[i])
    postprocess(input_video_paths[i],output_csv_files[i])