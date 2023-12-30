# This script is used to postprocess the segmentated video and calculate the deformation metrics.
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
def postprocess(input_video_name):
    raw_movie_path = 'Data\PartC\\'+input_video_name+'.tif'
    input_movie_path = 'Results\PartC\\'+input_video_name+'_segmented.tif'
    output_csv_file = 'Results\PartC\\'+input_video_name+'.csv'
    # Intializing
    # Read the input TIFF stack
    masks = tifffile.imread(input_movie_path)
    raws = tifffile.imread(raw_movie_path)
    # Get TIFF stack properties
    num_frames, height, width = masks.shape
    # Initialize the CSV file
    with open(output_csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['Frame Index', 'Area Convex (px^2)', 'Area Measured (px^2)', 'Area (microns^2)',
                             'Width (px)', 'Height (px)', 'Width (microns)', 'Height (microns)',
                             'Aspect Ratio', 'Porosity', 'Brightness', 'Deformation',
                             'Inertia Ratio', 'Principal Inertia Ratio'])
    # Initialize counters
    zero_cell_counter = 0
    one_cell_counter = 0
    multiple_cell_counter = 0
    wrong_contour_counter = 0
    # constants
    pixel_size = 10 # microns
    magnification = 30
    pixel_size = pixel_size/magnification

    # Loop through each frame
    for i, mask in tqdm(enumerate(masks),total=num_frames):
        # Raw frame
        raw_frame = raws[i]
        # Masked frame
        masked_frame = cv2.bitwise_and(raw_frame, raw_frame, mask=mask.astype('uint8'))
        # Total brightness of the frame
        mask_sum = np.sum(mask)
        if mask_sum != 0:
            bright_avg = np.sum(masked_frame) / (mask_sum / 255)
        else:
            bright_avg = 0

        # Find the unique values in the mask
        unique_values = np.unique(mask)
        if len(unique_values)==1:
            zero_cell_counter+=1
            continue
        elif len(unique_values)==2:
            # Count the number of elements with value 1
            one_cell_counter+=1
            # Find the contours
            contours, _ = cv2.findContours(mask.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                # Aspect ratio
                x,y,w,h = cv2.boundingRect(cnt)
                w_um, h_um = w*pixel_size, h*pixel_size
                aspect = float(w)/h
                # Measured area
                area_msd = cv2.contourArea(cnt)     # [px]
                area_um = area_msd*pixel_size*pixel_size # [um^2]
                if area_msd == 0:
                    wrong_contour_counter+=1
                    continue
                hull = cv2.convexHull(cnt)
                area_cvx = cv2.contourArea(hull)    # [px]
                solidity = float(area_msd)/area_cvx
                porosity = float(area_cvx)/area_msd
                # Circularity
                perimeter = cv2.arcLength(cnt,True)
                circularity = 2*np.sqrt(np.pi*area_msd)/perimeter
                # Deformation
                deformation  = 1 - circularity
                # Moments of inertia
                M = cv2.moments(hull)
                mu20 = M['mu20']
                mu02 = M['mu02']
                mu11 = M['mu11']

                # Inertia ratio
                Ix = mu20
                Iy = mu02
                inertia_ratio = Iy / Ix if Ix != 0 else 0

                # Principal moments of inertia
                I1 = 0.5 * (mu20 + mu02) + 0.5 * np.sqrt(4 * mu11**2 + (mu20 - mu02)**2)
                I2 = 0.5 * (mu20 + mu02) - 0.5 * np.sqrt(4 * mu11**2 + (mu20 - mu02)**2)

                # Principal inertia ratio
                principal_inertia_ratio = I2 / I1 if I1 != 0 else 0


            # save in csv file
            with open(output_csv_file, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([i,area_cvx,area_msd,round(area_um,4),
                                    w,h,round(w_um,4),round(h_um,4),
                                    round(aspect,4),round(porosity,4),
                                    round(bright_avg,4),round(deformation,4),
                                    round(inertia_ratio,4),round(principal_inertia_ratio,4)])
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
# Run the postprocessing function for each video
for input_video_name in input_video_names:
    print('Processing',input_video_name)
    postprocess(input_video_name)