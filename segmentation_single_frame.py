# This script reads a single frame from an AVI file and runs Cellpose on it.
# The segmentation results are visualized using Matplotlib.
# It is used to evaluate the performance of Cellpose on a single frame and to estimate the time needed to process the whole video.
# The input parameters such as the model type and the diameter of the cells can be adjusted as needed.
# Mehmet Furkan Doğan - December 2023
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
# Function that reads nth frame
def get_frame(input_video_path,n):
    # Open the video file
    cap = cv2.VideoCapture(input_video_path)
    # Read the nth frame
    for i in range(n):
        ret, frame = cap.read()
        if not ret:
            print(f"Error reading frame {n} from the video file.")
            exit()
    return frame
    # Release the video capture object
    cap.release()

######################################################################## MAIN

# Choose a model (either 'cyto' for cytoplasm segmentation or 'nuclei' for nuclei segmentation)
model = models.Cellpose(gpu=True, model_type='cyto')  # Adjust parameters as needed

video_path = 'Data\PartC\CellA_GFP.avi'
# Specify the frame number you want to read
frame_number = 12398
# get total number of frames from the video file
cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.release()
print('Total number of frames:',total_frames)

# Read the specified frame from the AVI file
img = get_frame(video_path, frame_number)

# Run Cellpose on the image
spinner.text = 'Evaluating... '
spinner.start()
start_time = time.time()
masks, flows, styles, diams = model.eval(img, diameter=75)
elapsed_time = time.time() - start_time
spinner.stop()
# Print the elapsed time for one frame and the estimated time for the whole video
print('Elapsed time for one frame (s): ',elapsed_time)
print('Estimated time for the whole video (s):',19231*elapsed_time)
print('Estimated time for the whole video (h):',19231*elapsed_time/3600)

# Print the number of cells detected in this frame
unique_values = np.unique(masks)
print('Number of cells in this frame:',len(unique_values)-1)

# Visualize the segmentation results
# Create a Matplotlib figure
fig = plt.figure('Segmentation Results',figsize=(12, 5))
# Segmentation results
plot.show_segmentation(fig,img, masks, flows[0], channels=[0, 0])
plt.show()