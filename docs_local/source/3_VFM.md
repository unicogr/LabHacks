---
layout: default
title: "VFM"
comments: true
---

# <span style="color:black">pRF mapping</span>


In this tutorial, we will learn how to use [prfpy](https://github.com/VU-Cog-Sci/prfpy) to compute population receptive field maps using 7T-fMRI.

We will use the *iCORTEX 7T-fMRI* dataset to illustrate how to apply slice timing correction, motion compensation within and between runs, distortion correction, and co-registration with the freesurfer anatomy. 

 > **What we will lear to:** 


* Align repeated runs of a visual field mapping fMRI acquisition.  

* Set up the right search grids for pRF parameter optimization.

* Run pRF modelling using parallelization.

* Plot the pRF maps on a flattened cortical reconstruction and as interactive an 3D surface.


<figure>
    <iframe src="https://rawcdn.githack.com/nicogravel/researchLog_template/fd3cc222bb62b3bacf5a2d855a4adaf5748cbc62/docs_local/source/figures/pRF/lh_eccentricity_3D.html" width="100%" height="500px" frameborder="0"></iframe>
</figure>

<figure>
    <iframe src="https://rawcdn.githack.com/nicogravel/researchLog_template/fd3cc222bb62b3bacf5a2d855a4adaf5748cbc62/docs_local/source/figures/pRF/lh_polar_3D.html" width="100%" height="500px" frameborder="0"></iframe>
</figure>



### <span style="color:lightblue">Questions? 🦉</span>



<script src="https://giscus.app/client.js"
        data-repo="nicogravel/researchLog_template"
        data-repo-id="R_kgDON90EnA"
        data-category="Giscus!"
        data-category-id="DIC_kwDON90EnM4CnVS9"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="gruvbox"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>




## **1st part**:  pRF mapping


### We use and `neuropythy` and `prfpy` to compute pRF parameters for a flattened cortical reconstruction on  single subject and using a single run 

```python
import os, sys, six # six provides python 2/3 compatibility
import numpy as np
import scipy as sp
import scipy.stats as stats
import pickle


# The neuropythy library is a swiss-army-knife for handling MRI data, especially
# anatomical/structural data such as that produced by FreeSurfer or the HCP.
# https://github.com/noahbenson/neuropythy
import neuropythy as ny

import matplotlib as mpl
import matplotlib.pyplot as plt
import ipyvolume as ipv

from nilearn import image, surface, plotting, signal

import nibabel as nib
import numpy as np

import math 
from PIL import Image
from prfpy.stimulus import PRFStimulus2D
from prfpy.model import Iso2DGaussianModel
from prfpy.fit import Iso2DGaussianFitter


# Load the time series
load_path = '/home/nicolas/Documents/Paris/UNICOG/Analyses/fMRIdata/iCORTEX/sub-00/retinotopy/'
V1_ts_lh = np.load(load_path + 'V1_ts_lh.npy')
V1_ts_rh = np.load(load_path + 'V1_ts_rh.npy')


fs_pth = '/home/nicolas/Programas/freesurfer-linux-ubuntu22_amd64-7.4.0/freesurfer/subjects/'
subject_id = 'sub-00_iso'
sub = ny.freesurfer_subject([fs_pth + subject_id])
```

### Get V1 coordinates fom the fsaverage registration of the subject

We did this in step  2.3.14. No we jujst load these:

```python
# Load the time series
load_path = '/home/... ... fMRIdata/iCORTEX/sub-00/retinotopy/'
v1_centers = np.load(load_path + 'v1_centers.npy', allow_pickle=True).item()
v1_rights = np.load(load_path + 'v1_rights.npy', allow_pickle=True).item()


method = 'orthographic' # or: equirectangular, sinusoidal, mercator
radius = np.pi/4 #np.pi/2

# Now, we make the projections:
map_projs = {}
for h in ['lh', 'rh']: 
#for h in [0, 1]:     
    mp = ny.map_projection(chirality=h,
                           center=v1_centers[h],
                           center_right=v1_rights[h],
                           method=method,
                           radius=radius,
                           registration='native')
    map_projs[h] = mp

# See what this created.
map_projs

flatmaps = {h: mp(sub.hemis[h]) for (h,mp) in map_projs.items()}
flatmaps

lh_cortex_label = flatmaps['lh'].prop('index')
rh_cortex_label = flatmaps['rh'].prop('index')
lh_cortex_label
```


### We run pRF mapping !

We use the output from section 2.3.17.


### Prepare stimulus
```python
pRF_images_path ='/home/... .../iCORTEX/pRF_log_images/'

# Initialize an empty list to store the data
data_list = []

# Loop through the files in the folder
for frame in range(150):
    # Load the .png file
    file_path = os.path.join(pRF_images_path,'run5_' + str(frame) + '.png')
    image = Image.open(file_path)
    data = np.array(image)
    data_list.append(data)

# Stack the data along the third dimension to create the design matrix
design_matrix = np.stack(data_list, axis=-1)

print(f'Design matrix shape: {design_matrix.shape}')


%matplotlib inline
from IPython.display import clear_output

plt.figure()
for i in range(np.shape(design_matrix)[2]):
    plt.imshow(design_matrix[:,:,i],cmap='gist_gray')
    plt.title('Frame %d' % (i+1))
    plt.show()
    clear_output(wait=True)



# screen size parameters
screen_height_cm   = 39.29 #69.84 #12.65
screen_size_cm     = screen_height_cm/2 
screen_distance_cm = 200 #5.0

# calculate max stim ecc
max_ecc = math.atan(screen_size_cm/screen_distance_cm)
#max_ecc = math.atan(screen_height_cm/screen_distance_cm)/np.pi*2; # in degrees

print('Max ecc in rad: ', max_ecc)
max_ecc_deg        = round(math.degrees(max_ecc))
print('Max ecc in deg: ', max_ecc_deg)
max_ecc_deg

prf_stim = PRFStimulus2D(screen_size_cm=screen_size_cm,
                             screen_distance_cm=screen_distance_cm,
                             design_matrix=design_matrix,
                             TR=2)
```


### Compute pRFs!


We first set the grid search. Setting a biophysically meaningful and computationally feasible grid for the optimisation (*least square minimisation*) is crucial, as it will allow converging fast and accurately to the best solution. Importantly, `n_procs` is crucial, in my personal computer I can use up to 8 workers. In a high performance cluster more can be used. The more workers, the faster. 

```python
normalize_RFs=True


print('Data shape: ', V1_ts_lh.shape)
data = V1_ts_lh.T
print('Data shape: ', data.shape)

# pRF type
n_procs = 8
gg = Iso2DGaussianModel(stimulus=prf_stim,normalize_RFs=normalize_RFs)
gf = Iso2DGaussianFitter(data=data, model=gg, n_jobs=n_procs)

# Gid fit
ecc_grid=np.linspace(0.1,7,10)
polar_grid=np.linspace(-np.pi,np.pi,24)
size_grid=np.linspace(0.1,10,10)
max_ecc_size  = round(max_ecc_deg,2)
verbose = True        
n_batches = 20

#IMPORTANT: fixing bold baseline to 0 (recommended), and only allowing positive prfs
#fixed_grid_baseline=0
gauss_grid_bounds=[(0,1)] # bound on prf amplitudes (only positive)


gf.grid_fit(ecc_grid=ecc_grid,
            polar_grid=polar_grid,
            size_grid=size_grid,
            verbose=verbose,
            n_batches=n_batches,
            grid_bounds=gauss_grid_bounds)
            #fixed_grid_baseline=fixed_grid_baseline, 

```

Once the grid search has been defined we can continue with the iterative search, we must set the `rsq_threshold` to a small but not *too* small number. This is important. Too small, and we will get stuck on a local minima and never converge (it will take longer to compute and the solution will be wrong).


```shell
# Iterative fit
# 
rsq_threshold=0.0005
verbose=True
gauss_bounds = [(-17.5, 17.5),  # x
                (-17.5, 17.5),  # y
                (0.5, 15),  # prf size
                (0, 1),  # prf amplitude
                (0, 0)]  # bold baseline
gauss_bounds += [(0,10),(0,0)] #hrf bounds. if want it fixed to some value, specify e.g. (4,4) (0,0)




#iterative fit acts as a wrapper of optimize.minimize and passes all the arguments
gf.iterative_fit(rsq_threshold=rsq_threshold, 
                 verbose=verbose, bounds=gauss_bounds)

```

 > Output:

[Parallel(n_jobs=8)]: Using backend LokyBackend with 8 concurrent workers.   
[Parallel(n_jobs=8)]: Done  34 tasks      | elapsed:    8.7s  
[Parallel(n_jobs=8)]: Done 184 tasks      | elapsed:   36.7s  
[Parallel(n_jobs=8)]: Done 434 tasks      | elapsed:  1.5min  
[Parallel(n_jobs=8)]: Done 784 tasks      | elapsed:  2.5min  
[Parallel(n_jobs=8)]: Done 1234 tasks      | elapsed:  4.1min  
[Parallel(n_jobs=8)]: Done 1784 tasks      | elapsed:  6.3min    
[Parallel(n_jobs=8)]: Done 2434 tasks      | elapsed:  9.2min  
[Parallel(n_jobs=8)]: Done 3184 tasks      | elapsed: 12.4min  
[Parallel(n_jobs=8)]: Done 4034 tasks      | elapsed: 16.2min  
[Parallel(n_jobs=8)]: Done 4984 tasks      | elapsed: 20.1min  
[Parallel(n_jobs=8)]: Done 6034 tasks      | elapsed: 24.6min  
[Parallel(n_jobs=8)]: Done 7184 tasks      | elapsed: 29.7min  
[Parallel(n_jobs=8)]: Done 8434 tasks      | elapsed: 34.8min  
[Parallel(n_jobs=8)]: Done 9784 tasks      | elapsed: 39.6min  
[Parallel(n_jobs=8)]: Done 11234 tasks      | elapsed: 44.8min  
[Parallel(n_jobs=8)]: Done 12784 tasks      | elapsed: 50.6min  
[Parallel(n_jobs=8)]: Done 14434 tasks      | elapsed: 56.6min  
[Parallel(n_jobs=8)]: Done 16184 tasks      | elapsed: 63.5min  
[Parallel(n_jobs=8)]: Done 17447 out of 17447 | elapsed: 68.6min finished  
  

### Plot pRF parameter histograms

```python
# Save the pRF parameters

# Get the parameters from the iterative fit
x=gf.iterative_search_params[:,0]
y=gf.iterative_search_params[:,1]
sigma=gf.iterative_search_params[:,2]
total_rsq = gf.iterative_search_params[:,-1]

# Calculate polar angle and eccentricity maps
polar = np.angle(x + 1j*y)
ecc = np.abs(x + 1j*y)

# Examining the shape of the output
print('Polar shape: ', polar.shape)
print('Max ecc: ', np.max(ecc))
print('Max polar: ', np.max(polar))
print('Max sigma: ', np.max(sigma))
print('Max rsq: ', np.max(total_rsq)) 

# Save the pRF parameters
f = open(pRF_params, 'wb')
pickle.dump(gf, f)
f.close()

pRF_params = { 'x': x, 'y': y, 'sigma': sigma, 'total_rsq': total_rsq}   


save_path = '/home/... .../fMRIdata/iCORTEX/sub-00/retinotopy/'
np.save(save_path + 'pRF_params_lh.npy', pRF_params)


# Plot the time series
fig, ax = plt.subplots(1,4, figsize=(24,4), dpi=300, facecolor="w")

# Plot the left hemisphere time series
bins = 50
ax[0].hist(ecc, bins=bins, edgecolor='black')
ax[0].set_ylabel('Frequency', fontsize=10)
ax[0].set_xlabel('Eccentricity', fontsize=10)
ax[0].set_xlim([0, 7])  # Adjust the limits as needed
ax[1].hist(polar, bins=bins, edgecolor='black')
ax[1].set_ylabel('Frequency', fontsize=10)
ax[1].set_xlabel('Polar angle', fontsize=10)
ax[2].hist(sigma, bins=bins, edgecolor='black')
ax[2].set_ylabel('Frequency', fontsize=10)
ax[2].set_xlabel('Sigma', fontsize=10)
ax[2].set_xlim([0, 5])  # Adjust the limits as needed
ax[3].hist(total_rsq, bins=bins, edgecolor='black')
ax[3].set_ylabel('Frequency', fontsize=10)
ax[3].set_xlabel('VE', fontsize=10)
ax[3].set_xlim([0, 0.6])  # Adjust the limits as needed

```


|![](/figures/pRF_params_hist.png){width="900px" align=center}|
|:--:|
|**Distribution of pRF parameters**.|




### Plot pRF maps on the flattened cortical surface

```python

# Plot
(fig, (left_ax, right_ax)) = plt.subplots(1,2, figsize=(4,2), dpi=72*4)

ny.cortex_plot(flatmaps['lh'], axes=left_ax,
                color=ecc,
                cmap='RdBu',
                mask=total_rsq > 0.1,
                vmin=0.2, vmax=6)


ny.cortex_plot(flatmaps['lh'], axes=right_ax,
                color=np.degrees(polar),
                mask=total_rsq > 0.1,
                cmap='polar_angle_lh')

left_ax.axis('off')
right_ax.axis('off')
```


As a proof of concept, we managed to compute retinotopic maps using one subject and one run using prfpy (a python package for pRF mapping). After some adjustments we will have an accurate, minimalistic and completely transparent and clear pipeline to work at the surface level using more subjects and runs, and in different experiments.


Here some preliminary results, as proof of concept. 

|![](/figures/pRF/pRF_maps_avg_lh.png){width="900px" align=center}|
|:--:|
|**Cortical site (vertex) selectivity to visual field position estimated using pRF modeling**. Data for a single subject and run.|

