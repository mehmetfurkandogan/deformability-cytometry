# This script performs cell segmentation on a video file.
# The input video file is a TIFF stack. Data should be converted to a TIFF stack before running this script.
# The output video file is a TIFF stack with the same number of frames as the input video file.
# The output video file contains the segmented cells.
# The segmentation is performed using the Cellpose library.
######################################################################## IMPORT LIBRARIES
from halo import Halo
spinner = Halo(text='Importing libraries... ', text_color= 'magenta', color='magenta', spinner='dots')
spinner.start()
import cv2
import matplotlib.pyplot as plt
import numpy as np
from cellpose import models
from cellpose.io import imread
from cellpose import plot
import time
from tqdm import tqdm
import tifffile
spinner.stop()
######################################################################## FUNCTION DEFINITIONS
def segment_cells(input_movie_path, output_movie_path):
    # Choose a model (either 'cyto' for cytoplasm segmentation or 'nuclei' for nuclei segmentation)
    model = models.Cellpose(gpu=True, model_type='cyto')  # Adjust parameters as needed

    # Read the input TIFF stack
    tiff_stack = tifffile.imread(input_movie_path)

    # Get TIFF stack properties
    num_frames, height, width = tiff_stack.shape

    # Create TIFF stack for output
    output_stack = np.zeros_like(tiff_stack, dtype=np.uint8)
    
    spinner = Halo(text='Saving...'+output_movie_path, spinner='dots')

    # Loop through each frame
    for i, frame in tqdm(enumerate(tiff_stack),total=num_frames):
        # Perform cell segmentation
        masks, flows, styles, diams = model.eval(frame, diameter=60)
        # Scale the mask for visibility
        max_value = np.max(masks)
        if max_value == 0:
            continue
        scaled_frame = (masks.astype(np.float64) * 255/max_value).astype(np.uint8)

        # Store the segmented frame in the output stack
        output_stack[i] = scaled_frame

        # Save the output TIFF stack periodically to check progress
        saving_period = 100
        if i%saving_period == 0:
            spinner.start()
            tifffile.imwrite(output_movie_path, output_stack)
            spinner.stop()


    # Save the output TIFF stack
    spinner.start()
    tifffile.imwrite(output_movie_path, output_stack)
    spinner.stop()

######################################################################## MAIN


input_video_path = 'Data\PartC\CellB_GFP.tif'
output_video_path = 'Results\PartC\CellB_GFP_segmented.tif'

start_time = time.time()
segment_cells(input_video_path, output_video_path)
elapsed_time = time.time() - start_time

hour = int(elapsed_time/3600)
minute = int((elapsed_time - hour*3600)/60)
second = int(elapsed_time - hour*3600 - minute*60)
print('Elapsed time:',hour,'h',minute,'m',second,'s')
