# This file is used to visualize the deformability cytometry segmentation results
# Mehmet Furkan Doğan - December 2023
######################################################################## IMPORT LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter
######################################################################## MAIN
# List of all input and output paths
input_video_names = ['CellA_GFP',
                     'CellA_ShME480',
                     'CellB_GFP',
                     'CellB_ME480']
# Csv file paths
csv_files = [None]*len(input_video_names)
for i in range(len(input_video_names)):
    csv_files[i] = 'Results\PartC\\'+input_video_names[i]+'.csv'
# csv_file = 'Results\PartC\\'+input_video_names[0]+'.csv'

# Load your data into pandas DataFrames
CellA_GFP = pd.read_csv(csv_files[0])
CellA_ShME480 = pd.read_csv(csv_files[1])
CellB_GFP = pd.read_csv(csv_files[2])
CellB_ME480 = pd.read_csv(csv_files[3])

########################## FILTERING ##########################
# Filtering the data based on porosity
# Cells with porosity greater than 1.05 is filtered out
CellA_GFP = CellA_GFP[CellA_GFP['Porosity']<1.05]
CellA_ShME480 = CellA_ShME480[CellA_ShME480['Porosity']<1.05]
CellB_GFP = CellB_GFP[CellB_GFP['Porosity']<1.05]
CellB_ME480 = CellB_ME480[CellB_ME480['Porosity']<1.05]


########################## BRIGHNESS VS AREA ##########################
plt.scatter(CellA_GFP['Area (microns^2)'], CellA_GFP['Brightness'], label='CellA_GFP', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellA_ShME480['Area (microns^2)'], CellA_ShME480['Brightness'], label='CellA_ShME480', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellB_GFP['Area (microns^2)'], CellB_GFP['Brightness'], label='CellB_GFP', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellB_ME480['Area (microns^2)'], CellB_ME480['Brightness'], label='CellB_ME480', s=10, alpha=0.5, edgecolors='none')

plt.xlabel('Area [$\mu m^2$]')  # x-axis label
plt.ylabel('Brightness [a.u]')  # y-axis label
plt.legend()  # To show legend
# Save as eps
plt.savefig('Results\PartC\BrightnessVsArea.eps', format='eps')
# Save as pdf
plt.savefig('Results\PartC\BrightnessVsArea.pdf', format='pdf')
plt.show()

########################## DEFORMATION VS AREA ##########################
plt.scatter(CellA_GFP['Area (microns^2)'], CellA_GFP['Deformation'], label='CellA_GFP', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellA_ShME480['Area (microns^2)'], CellA_ShME480['Deformation'], label='CellA_ShME480', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellB_GFP['Area (microns^2)'], CellB_GFP['Deformation'], label='CellB_GFP', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellB_ME480['Area (microns^2)'], CellB_ME480['Deformation'], label='CellB_ME480', s=10, alpha=0.5, edgecolors='none')

plt.xlabel('Area [$\mu m^2$]')  # x-axis label
plt.ylabel('Deformation')  # y-axis label
plt.legend()  # To show legend
# Save as pdf
plt.savefig('Results\PartC\DeformationVsArea.pdf', format='pdf')
plt.show()

########################## POROSITY VS INERTIA RATIO ##########################
plt.scatter(CellA_GFP['Porosity'], CellA_GFP['Inertia Ratio'], label='CellA_GFP', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellA_ShME480['Porosity'], CellA_ShME480['Inertia Ratio'], label='CellA_ShME480', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellB_GFP['Porosity'], CellB_GFP['Inertia Ratio'], label='CellB_GFP', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellB_ME480['Porosity'], CellB_ME480['Inertia Ratio'], label='CellB_ME480', s=10, alpha=0.5, edgecolors='none')

plt.xlabel('Porosity')  # x-axis label
plt.ylabel('Inertia Ratio')  # y-axis label
plt.legend()  # To show legend
# Save as pdf
# plt.savefig('Results\PartC\PorosityVsInertiaRatio.pdf', format='pdf')
plt.show()

########################## ASPECT RATIO VS AREA ##########################
plt.scatter(CellA_GFP['Area (microns^2)'], CellA_GFP['Aspect Ratio'], label='CellA_GFP', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellA_ShME480['Area (microns^2)'], CellA_ShME480['Aspect Ratio'], label='CellA_ShME480', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellB_GFP['Area (microns^2)'], CellB_GFP['Aspect Ratio'], label='CellB_GFP', s=10, alpha=0.5, edgecolors='none')
plt.scatter(CellB_ME480['Area (microns^2)'], CellB_ME480['Aspect Ratio'], label='CellB_ME480', s=10, alpha=0.5, edgecolors='none')

plt.xlabel('Area [$\mu m^2$]')  # x-axis label
plt.ylabel('Aspect Ratio')  # y-axis label
plt.legend()  # To show legend
# Save as pdf
plt.savefig('Results\PartC\AspectRatioVsArea.pdf', format='pdf')
plt.show()

########################## DEFORMATION HISTOGRAM ##########################
plt.hist(CellA_GFP['Deformation'], bins=50, label='CellA_GFP', alpha=0.5, density=True)
plt.hist(CellA_ShME480['Deformation'], bins=50, label='CellA_ShME480', alpha=0.5, density=True)
plt.hist(CellB_GFP['Deformation'], bins=50, label='CellB_GFP', alpha=0.5, density=True)
plt.hist(CellB_ME480['Deformation'], bins=50, label='CellB_ME480', alpha=0.5, density=True)
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=100))
plt.xlim(0, 0.3)

plt.xlabel('Deformation')  # x-axis label
plt.ylabel('Frequency')  # y-axis label
plt.legend()  # To show legend
# Save as pdf
plt.savefig('Results\PartC\DeformationHistogram.pdf', format='pdf')
plt.show()
