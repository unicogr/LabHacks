---
layout: default
title: "VFM"
comments: true
---

# [**TUTORIAL:**](https://nicogravel.github.io/researchLog_template/html/2_fMRI.html) <span style="color:lightblue">pRF mapping </span>


In this tutorial, we will learn how to use [prfpy](https://github.com/VU-Cog-Sci/prfpy) to compute population receptive field maps using 7T-fMRI.


 > **Goals** 


* Align repeated runs of a visual field mapping fMRI acquisition.  

* Set up the right search [grids](https://prfpy.readthedocs.io/en/latest/model.html) for pRF parameter optimization.

* Run pRF modelling using parallelization.

* Plot the pRF maps on a flattened cortical reconstruction and as interactive an 3D surface.

We will use the *iCORTEX 7T-fMRI* dataset. We will be performing the following steps:

    1. Define the FreeSurfer subject and load the flatmaps
    2. Load surface-matched T2 data and project it to the flatmaps
    3. Preprocess BOLD time series and compute the average for each hemisphere
    4. Load stimuli images and define design matrix
    4. Set pRF model parameters (grid fit, iterative fit)
    5. Fit pRF models to the averaged BOLD time series data
    6. Save the pRF parameters

 

|![](/figures/pRF/sub-01_iso_averaged_lh_pRF_maps_with_colorbars.png){width="1200px" align=center}|
|:--:|
|**Retinotopic maps in early visual cortex for a single hemisphere**. Population receptive field (pRF) parameters (eccentricity, polar angle, size) were estimated for BOLD data interpolated to the cortical surface. circular region of interest (ROI) was defined on the cortical surface, centered on FreeSurfer’s probabilistic V1 label. The resulting pRF estimates revealed eccentricity representations (left) and polar angle organization (right). Data shown for a single subject (BOLD data were averaged across four runs).|





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
%matplotlib inline
from IPython.display import clear_output

import os, sys, six # six provides python 2/3 compatibility
import numpy as np
import scipy as sp
import scipy.stats as stats
import pickle
import nibabel as nib
import matplotlib.pyplot as plt
from nilearn import plotting, signal
import neuropythy as ny  # Import neuropythy


# The neuropythy library is a swiss-army-knife for handling MRI data, especially
# anatomical/structural data such as that produced by FreeSurfer or the HCP.
# https://github.com/noahbenson/neuropythy
import neuropythy as ny
import matplotlib as mpl
import ipyvolume as ipv

from nilearn import image, surface, plotting, signal



import math 
from PIL import Image
from prfpy.stimulus import PRFStimulus2D
from prfpy.model import Iso2DGaussianModel
from prfpy.fit import Iso2DGaussianFitter

fs_pth = '/home/ng281432/Documents/Programas/freesurfer/8.0.0/subjects/'
subject_id = 'sub-00_iso'
sub = ny.freesurfer_subject([fs_pth + subject_id])

anat_pth = '/home/ng281432/Documents/data/iCORTEX/sub-00/anat/'
T1 = image.load_img(os.path.join(anat_pth, 'sub-00_t1_norm.nii.gz'))

save_path = '/home/ng281432/Documents/data/iCORTEX/sub-00/pRF_results/'


# Set paths
func_pth = '/home/ng281432/Documents/data/iCORTEX/sub-00/retinotopy/'

pRF_images_path ='/home/ng281432/Documents/data/iCORTEX/pRF_log_images/'


# # Loop through runs 1 to 4
# for run in range(1, 5):
#     print(f"Processing run: {run}")

#     # Load the functional image for the current run
#     func_img_path = os.path.join('/home/ng281432/Documents/data/iCORTEX/sub-00/retinotopy/', f'coreg_motioncomp_{run}.nii.gz')
#     try:
#         T2_img = image.load_img(func_img_path)
#         T2_data = T2_img.get_fdata()  # Get the data as a NumPy array

#         # Calculate the mean across the time dimension (axis=3)
#         T2_mean_data = np.mean(T2_data, axis=3)

#         # Create a new NIfTI image from the mean data
#         T2_mean_img = image.new_img_like(T2_img, T2_mean_data)

#     except FileNotFoundError:
#         print(f"Error: Functional image not found for run {run} at {func_img_path}")
#         continue  # Skip to the next run

#     # Generate the plot
#     display = plotting.plot_stat_map(T2_mean_img, bg_img=T1, title=f'T2 to T1 alignment - Run {run}',
#                                    display_mode='ortho', cut_coords=(0, 0, 0),
#                                    draw_cross=False)
    
#     # Save the plot
#     plot_filename = f'{subject_id}_run{run}_T2_T1_alignment.png'
#     display.savefig(os.path.join(save_path, plot_filename), dpi=300)
#     display.close()  # Close the figure to free memory
#     print(f"T2-T1 alignment plot saved to {os.path.join(save_path, plot_filename)}")
    
```

### Get V1 coordinates fom the fsaverage registration of the subject

We did this in step  2.3.14. No we jujst load these:

```python
fsaverage = ny.freesurfer_subject('fsaverage')

v1_centers = {}
for h in ['lh', 'rh']:
    # Get the Cortex object for this hemisphere.
    cortex = fsaverage.hemis[h]
    # We're dealing with the cortical sphere, so get that surface.
    sphere = cortex.registrations['native']
    # Grab the V1_weight property and the coordinates.
    v1_weight = sphere.prop('V1_weight')
    coords = sphere.coordinates
    # Now, we can take a weighted average of the coordinates in V1.
    v1_center = np.sum(coords * v1_weight[None,:], axis=1)
    v1_center /= np.sum(v1_weight)
    # Save this in the v1_centers dict.
    v1_centers[h] = v1_center

# See what got saved:
v1_centers

v1_rights = {}
for h in ['lh', 'rh']:
    # Once again, we get the Cortex object for this hemisphere and the
    # spherical surface.
    cortex = fsaverage.hemis[h]
    sphere = cortex.registrations['native']
    # Now, we want the cortex_label property, which is True for points not
    # on the medial wall and False for points on the medial wall.
    weight = sphere.prop('cortex_label')
    # We want to find the point at the middle of the medial wall, so we
    # want to invert this property (True values indicate the medial wall).
    weight = ~weight
    # Now we take the weighted average again (however, since these weight
    # values are all True or False (1 or 0), we can just average the
    # points that are included.
    mwall_center = np.mean(coords[:, weight], axis=1)
    # If this is the RH, we invert this coordinate
    v1_rights[h] = -mwall_center if h == 'rh' else mwall_center

# See what got saved.
v1_rights

method = 'orthographic' # or: equirectangular, sinusoidal, mercator
radius = np.pi/2 

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

## Load surface-matched T2 data and project it to the flatmaps

```python
# Load FreeSurfer subject
sub = ny.freesurfer_subject([fs_pth + subject_id])

# Define flatmaps (assuming map_projs is defined elsewhere in your notebook)
# Example:
# method = 'orthographic'
# radius = np.pi/2
# map_projs = {}
# for h in ['lh', 'rh']:
#     mp = ny.map_projection(chirality=h, method=method, radius=radius)
#     map_projs[h] = mp
# flatmaps = {h: mp(sub.hemis[h]) for (h,mp) in map_projs.items()}

# Set signal cleaning parameters
detrend = True
standardize = 'psc'  # Percent signal change
low_pass = 0.12
high_pass = 0.02
TR = 2
confounds = None

# Loop through runs and hemispheres
for run in range(1, 5):
    for hemi in ['lh', 'rh']:
        print(f"Processing run: {run}, hemisphere: {hemi}")

        # Load the projected time series
        time_series_path = os.path.join(func_pth, f'{hemi}.tseries_run{run}.mgh')
        try:
            time_series = np.squeeze(nib.load(time_series_path).get_fdata())
        except FileNotFoundError:
            print(f"Error: Time series not found for run {run}, hemisphere {hemi} at {time_series_path}")
            continue  # Skip to the next iteration

        print(f"Time series in hemisphere: {time_series.shape}")

        # Get cortex indices using flatmaps
        cortex_index = flatmaps[hemi].prop('index')
        time_series_cortex = time_series[cortex_index, :]

        print(f"Time series in ROI: {time_series_cortex.shape}")

        # Clean the time series data
        time_series_cleaned = signal.clean(time_series_cortex.T,
                                            confounds=confounds,
                                            detrend=detrend,
                                            standardize=standardize,
                                            filter='butterworth',
                                            low_pass=low_pass,
                                            high_pass=high_pass,
                                            tr=TR).T

        # Z-score the cleaned time series
        time_series_zscored = stats.zscore(time_series_cleaned, axis=1)

        # # Save the cleaned and z-scored time series as .npy file
        # output_npy_path = os.path.join(func_pth, f'{hemi}_run_{run}_cleaned_zscored.npy')
        # np.save(output_npy_path, time_series_zscored)
        # print(f"Cleaned and z-scored time series saved to {output_npy_path}")

        # Plot the time series (first 100 vertices)
        # num_vertices = min(time_series_zscored.shape[0], 100)  # Limit to 100 vertices or less
        # plt.figure(figsize=(10, 5))  # Adjust figure size as needed
        # plt.imshow(time_series_zscored[:num_vertices, :], aspect='auto', cmap='bwr')  # Plot as heatmap
        # plt.xlabel('Time Points')
        # plt.ylabel('Vertices')
        # plt.title(f'Normalized BOLD Time Series - Run {run}, {hemi}, First {num_vertices} Vertices')
        # plt.colorbar(label='Normalized BOLD Signal (Z-score)')  # Add a colorbar
        # plt.tight_layout()
        # plt.show()
```


## Preprocess BOLD time series and compute the average for each hemisphere

```python
# First, load and average time series data for each hemisphere
for hemi in ['lh', 'rh']:
    time_series_list = []
    
    # Load data from all runs
    for run in range(1, 5):
        time_series_path = os.path.join(func_pth, f'{hemi}_run_{run}_cleaned_zscored.npy')
        try:
            time_series = np.load(time_series_path)
            time_series = np.nan_to_num(time_series, nan=0.0)  # Replace NaNs with zeros
            time_series_list.append(time_series)
            print(f"Loaded time series from {time_series_path}, shape: {time_series.shape}")
        except FileNotFoundError:
            print(f"Could not find file: {time_series_path}")
    
    # Average the time series if we have any data
    if time_series_list:
        avg_time_series = np.mean(time_series_list, axis=0)
        print(f"Created averaged time series for {hemi} with shape {avg_time_series.shape}")
        
        # Save the averaged time series
        avg_output_path = os.path.join(func_pth, f'{hemi}_averaged_cleaned_zscored.npy')
        np.save(avg_output_path, avg_time_series)
        print(f"Saved averaged time series to {avg_output_path}")
    else:
        print(f"No data found for hemisphere {hemi}")

```


###  Load stimuli images and define design matrix
```python
# screen pRF stimulus parameters
screen_height_cm   = 32 #39.29 #69.84 #12.65
screen_size_cm     = screen_height_cm/2 
screen_distance_cm = 199 #5.0

# calculate max stim ecc
max_ecc = math.atan(screen_size_cm/screen_distance_cm)

print('Min ecc in rad: ', max_ecc)
max_ecc_deg        = round(math.degrees(max_ecc))
print('Max ecc in deg: ', max_ecc_deg)
max_ecc_deg

prf_stim = PRFStimulus2D(screen_size_cm=screen_size_cm,
                         screen_distance_cm=screen_distance_cm,
                         design_matrix=design_matrix,
                         TR=2)

# Set pRF fitting parameters
n_procs = 8
normalize_RFs = True
ecc_grid = np.linspace(0.1, 5, 10)
polar_grid = np.linspace(-np.pi, np.pi, 24)
size_grid = np.linspace(0.1, 4, 10)
verbose = True
n_batches = 20
fixed_grid_baseline = 0
gauss_grid_bounds = [(0, 1)]
rsq_threshold = 0.001
gauss_bounds = [(-17.5, 17.5), (-17.5, 17.5), (0.2, 7), (0, 1), (0, 0)]
gauss_bounds += [(0, 10), (0, 0)]

```

### Load the averaged time series data

```python
    
    lh_avg_path = os.path.join(func_pth, 'lh_averaged_cleaned_zscored.npy')
    rh_avg_path = os.path.join(func_pth, 'rh_averaged_cleaned_zscored.npy')

    try:
        lh_time_series = np.load(lh_avg_path)
        print(f"Loaded LH averaged time series, shape: {lh_time_series.shape}")
    except FileNotFoundError:
        print(f"Error: Could not find {lh_avg_path}")
        lh_time_series = None

    try:
        rh_time_series = np.load(rh_avg_path)
        print(f"Loaded RH averaged time series, shape: {rh_time_series.shape}")
    except FileNotFoundError:
        print(f"Error: Could not find {rh_avg_path}")
        rh_time_series = None

    print(f"Loaded LH time series: {lh_time_series.shape}, RH time series: {rh_time_series.shape}") 
```



### Set pRF model parameters (grid fit, iterative fit)


We first set the grid search. Setting a biophysically meaningful and computationally feasible grid for the optimisation of the pRF position and size parameters, as well as boundaries for only positive pRF is crucial, as it will allow converging fast and accurately to the best solution (by grid search based *least squares minimisation*). Importantly, `n_procs` is crucial, in my personal computer I can use up to 8 workers. In a high performance cluster more can be used. The more workers, the faster. 

```python
# Initialize the pRF model and fitter
gg = Iso2DGaussianModel(stimulus=prf_stim, normalize_RFs=normalize_RFs)
gf = Iso2DGaussianFitter(data=lh_time_series, model=gg, n_jobs=n_procs)

# Grid fit
gf.grid_fit(ecc_grid=ecc_grid,
            polar_grid=polar_grid,
            size_grid=size_grid,
            verbose=verbose,
            n_batches=n_batches,
            grid_bounds=gauss_grid_bounds,
            fixed_grid_baseline=fixed_grid_baseline)

# Iterative fit
gf.iterative_fit(rsq_threshold=rsq_threshold,
                    verbose=verbose, bounds=gauss_bounds)

# Extract pRF parameters
x = gf.iterative_search_params[:, 0]
y = gf.iterative_search_params[:, 1]
sigma = gf.iterative_search_params[:, 2]
total_rsq = gf.iterative_search_params[:, -1]

# Calculate polar angle and eccentricity
polar = np.angle(x + 1j*y)
ecc = np.abs(x + 1j*y)

# Print parameter info
print('Polar shape: ', polar.shape)
print('Max ecc: ', np.max(ecc))
print('Max polar: ', np.max(polar))
print('Max sigma: ', np.max(sigma))
print('Max rsq: ', np.max(total_rsq))

```

Once the grid search has been defined we can continue with the iterative search, we must set the `rsq_threshold` to a small but not *too* small number. This is important. Too small, and we will get stuck on a local minima and never converge (it will take longer to compute and the solution will be wrong).

### Fit pRF models to the averaged BOLD time series data

```python
# Loop through runs and hemispheres
for run in range(1, 5):
    for hemi in ['lh', 'rh']:
        print(f"Processing pRF mapping: run {run}, hemisphere {hemi}")

        # Load the cleaned and z-scored time series data
        time_series_path = os.path.join(func_pth, f'{hemi}_run_{run}_cleaned_zscored.npy')
        try:
            time_series = np.load(time_series_path)
            print(f"Loaded time series from {time_series_path}")
            print(f"Time series shape: {time_series.shape}")

            # Replace NaN values with zeros
            time_series = np.nan_to_num(time_series, nan=0.0)

        except FileNotFoundError:
            print(f"Error: Time series not found at {time_series_path}")
            continue

        # Initialize the pRF model and fitter
        gg = Iso2DGaussianModel(stimulus=prf_stim, normalize_RFs=normalize_RFs)
        gf = Iso2DGaussianFitter(data=time_series, model=gg, n_jobs=n_procs)

        # Grid fit
        gf.grid_fit(ecc_grid=ecc_grid,
                    polar_grid=polar_grid,
                    size_grid=size_grid,
                    verbose=verbose,
                    n_batches=n_batches,
                    grid_bounds=gauss_grid_bounds,
                    fixed_grid_baseline=fixed_grid_baseline)

        # Iterative fit
        gf.iterative_fit(rsq_threshold=rsq_threshold,
                         verbose=verbose, bounds=gauss_bounds)

        # Extract pRF parameters
        x = gf.iterative_search_params[:, 0]
        y = gf.iterative_search_params[:, 1]
        sigma = gf.iterative_search_params[:, 2]
        total_rsq = gf.iterative_search_params[:, -1]

        # Calculate polar angle and eccentricity
        polar = np.angle(x + 1j*y)
        ecc = np.abs(x + 1j*y)

        # Print parameter info
        print('Polar shape: ', polar.shape)
        print('Max ecc: ', np.max(ecc))
        print('Max polar: ', np.max(polar))
        print('Max sigma: ', np.max(sigma))
        print('Max rsq: ', np.max(total_rsq))

        # Save pRF parameters
        save_path = '/home/ng281432/Documents/data/iCORTEX/sub-00/pRF_results/'
        pRF_params = {'x': x, 'y': y, 'sigma': sigma, 'total_rsq': total_rsq}
        output_pRF_path = os.path.join(save_path, f'pRF_params_run_{run}_{hemi}.npy')
        np.save(output_pRF_path, pRF_params)
        print(f"pRF parameters saved to {output_pRF_path}")

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
  


### Save pRF parameters

```python
# Save pRF parameters
save_path = '/home/ng281432/Documents/data/iCORTEX/sub-00/pRF_results/'
pRF_params = {'x': x, 'y': y, 'sigma': sigma, 'total_rsq': total_rsq}
output_pRF_path = os.path.join(save_path, f'pRF_params_run_{run}_{hemi}.npy')
np.save(output_pRF_path, pRF_params)
print(f"pRF parameters saved to {output_pRF_path}")
```


### Load pRF mapping results

```python
## Plot pRF maps on inflated surfaces
from nilearn import plotting, surface

# Set hemispheres to process
hemispheres = ['lh', 'rh']


hemi = hemispheres[1]
run=1

# Get the inflated surfaces from the FreeSurfer subject
inflated_mesh = os.path.join(fs_pth, subject_id, 'surf', f'{hemi}.inflated')
sulc_map = os.path.join(fs_pth, subject_id, 'surf', f'{hemi}.sulc')

# Load pRF parameters for the current hemisphere
#pRF_params_path = os.path.join(save_path, f'pRF_params_run_{run}_{hemi}.npy')
pRF_params_path = os.path.join(save_path, f'pRF_params_averaged_{hemi}.npy')
pRF_params = np.load(pRF_params_path, allow_pickle=True).item()

# Extract parameters
x = pRF_params['x']
y = pRF_params['y']
sigma = pRF_params['sigma']
total_rsq = pRF_params['total_rsq']

# Calculate derived measures
ecc = np.abs(x + 1j*y)
polar = np.angle(x + 1j*y)

```

### Define meaingful pRF colormaps

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def get_eccentricity_palette():
    """
    Returns a color palette with 20 colors transitioning from green to red to green to blue to green.
    
    Returns:
        dict: Dictionary containing different formats of the color palette
    """
    # Original RGB values (0-255)
    rgb_values = [
        [255, 40, 0], # Red

        [255, 130, 0], # Orange-red

        [255, 210, 0], # Orange-yellow

        [255, 255, 0], # Yellow

        [115, 255, 0], # Yellow-green

        [31, 255, 0], # Green

        [0, 255, 207], # Turquoise

        [0, 231, 255], # Cyan

        [20, 140, 255], # Light blue

        [40, 60, 255] # Blue

        # [0, 231, 255], # Cyan (repeated)

        # [0, 147, 255], # Sky blue

        # [0, 63, 255], # Royal blue

        # [7, 0, 255], # Blue

        # [91, 0, 255], # Indigo

        # [175, 0, 255], # Purple

        # [247, 0, 255], # Magenta

        # [255, 0, 179], # Pink

        # [255, 0, 95], # Hot pink

        # [255, 0, 11] # Red
    ]
    
    # Normalize to 0-1 range for matplotlib
    norm_values = [[r/255, g/255, b/255] for r, g, b in rgb_values]
    
    # Create hex values for other libraries
    hex_values = [mcolors.rgb2hex(rgb) for rgb in norm_values]
    
    # Create named colors with format for easy access
    named_colors = {f"color{i+1}": hex_values[i] for i in range(len(hex_values))}
    
    return {
        "rgb_0_255": rgb_values,         # Original RGB (0-255)
        "rgb_0_1": norm_values,          # Normalized RGB (0-1)
        "hex": hex_values,               # Hex color codes
        "named": named_colors,           # Named colors
        "matplotlib_cmap": mcolors.LinearSegmentedColormap.from_list("custom_cmap", norm_values)  # Matplotlib colormap
    }



def get_polar_palette():
    """
    Returns a color palette with 20 colors transitioning from green to red to green to blue to green.
    
    Returns:
        dict: Dictionary containing different formats of the color palette
    """
    # Original RGB values (0-255)
    rgb_values = [
        [106, 189, 69],   # Color1
        [203, 219, 42],   # Color2
        [254, 205, 8],    # Color3
        [242, 104, 34],   # Color4
        [237, 32, 36],    # Color5
        [237, 32, 36],    # Color6
        [242, 104, 34],   # Color7
        [254, 205, 8],    # Color8
        [203, 219, 42],   # Color9
        [106, 189, 69],   # Color10
        [106, 189, 69],   # Color11
        [110, 205, 221],  # Color12
        [50, 178, 219],   # Color13
        [62, 105, 179],   # Color14
        [57, 84, 165],    # Color15
        [57, 84, 165],    # Color16
        [62, 105, 179],   # Color17
        [50, 178, 219],   # Color18
        [110, 205, 221],  # Color19
        [106, 189, 69]    # Color20
    ]
    
    # Normalize to 0-1 range for matplotlib
    norm_values = [[r/255, g/255, b/255] for r, g, b in rgb_values]
    
    # Create hex values for other libraries
    hex_values = [mcolors.rgb2hex(rgb) for rgb in norm_values]
    
    # Create named colors with format for easy access
    named_colors = {f"color{i+1}": hex_values[i] for i in range(len(hex_values))}
    
    return {
        "rgb_0_255": rgb_values,         # Original RGB (0-255)
        "rgb_0_1": norm_values,          # Normalized RGB (0-1)
        "hex": hex_values,               # Hex color codes
        "named": named_colors,           # Named colors
        "matplotlib_cmap": mcolors.LinearSegmentedColormap.from_list("custom_cmap", norm_values)  # Matplotlib colormap
    }


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import os

# Set subject ID and path for saving the figures
subject_id = 'sub-00_iso'
save_path = '/home/ng281432/Documents/data/iCORTEX/sub-00/pRF_results/'

# Get color palettes
colors_ecc = get_eccentricity_palette()
colors_polar = get_polar_palette()

# # Plot eccentricity palette as concentric rings
# fig_ecc, ax_ecc = plt.subplots(figsize=(6, 6))
# ax_ecc.set_aspect('equal')
# ax_ecc.set_xlim(-1.1, 1.1)
# ax_ecc.set_ylim(-1.1, 1.1)
# ax_ecc.set_axis_off()

# # Create concentric rings from inner to outer
# num_ecc_colors = len(colors_ecc["hex"])
# for i, color in enumerate(colors_ecc["hex"]):
#     inner_radius = i / num_ecc_colors
#     outer_radius = (i + 1) / num_ecc_colors
    
#     # Create a ring (using a wedge with a 360-degree arc)
#     ring = Wedge((0, 0), outer_radius, 0, 360, width=outer_radius-inner_radius, color=color)
#     ax_ecc.add_patch(ring)

# # # Create concentric rings with logarithmic spacing
# # num_ecc_colors = len(colors_ecc["hex"])
# # # Define logarithmic spacing - add a small value to avoid log(0)
# # log_space = np.logspace(np.log10(0.05), np.log10(1.0), num_ecc_colors + 1)
# # # Normalize to ensure the outer radius is exactly 1.0
# # log_space = log_space / log_space[-1]

# # for i, color in enumerate(colors_ecc["hex"]):
# #     inner_radius = log_space[i]
# #     outer_radius = log_space[i + 1]
    
# #     # Create a ring (using a wedge with a 360-degree arc)
# #     ring = Wedge((0, 0), outer_radius, 0, 360, width=outer_radius-inner_radius, color=color)
# #     ax_ecc.add_patch(ring)

# plt.title("Eccentricity")
# plt.tight_layout()

# # Save eccentricity colormap
# ecc_filename = f"{subject_id}_eccentricity_colormap.png"
# fig_ecc.savefig(os.path.join(save_path, ecc_filename), dpi=300)
# #plt.close(fig_ecc)

# # Plot polar angle palette as circle sectors
# fig_polar, ax_polar = plt.subplots(figsize=(6, 6), subplot_kw={'polar': True})
# # Set orientation: zero at left (West), clockwise direction
# ax_polar.set_theta_zero_location("W")
# ax_polar.set_theta_direction(-1)
# ax_polar.set_axis_off()

# # Create sectors around the circle
# num_polar_colors = len(colors_polar["hex"])
# theta = np.linspace(0, 2*np.pi, num_polar_colors, endpoint=False)
# width = 2*np.pi / num_polar_colors
# bars = ax_polar.bar(theta, [1]*num_polar_colors, width=width, bottom=0, 
#                     color=colors_polar["hex"], align="edge")

# plt.title("Polar Angle")
# plt.tight_layout()

# # Save polar angle colormap
# polar_filename = f"{subject_id}_polar_angle_colormap.png"
# fig_polar.savefig(os.path.join(save_path, polar_filename), dpi=300)
# #plt.close(fig_polar)

# print(f"Saved eccentricity colormap to: {os.path.join(save_path, ecc_filename)}")
# print(f"Saved polar angle colormap to: {os.path.join(save_path, polar_filename)}")
```

### Plot pRF parameter histograms

```python

# Get the parameters from the iterative fit
x=pRF_params['x']
y=pRF_params['y']
sigma=pRF_params['sigma']
total_rsq = pRF_params['total_rsq']

# Calculate polar angle and eccentricity maps
polar = np.angle(x + 1j*y)
ecc = np.abs(x + 1j*y)

# Examining the shape of the output
print('Polar shape: ', polar.shape)
print('Max ecc: ', np.max(ecc))
print('Max polar: ', np.max(polar))
print('Max sigma: ', np.max(sigma))
print('Max rsq: ', np.max(total_rsq)) 

# Plot the time series
fig_hist, ax = plt.subplots(1,4, figsize=(24,4), dpi=300, facecolor="w")

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

# Save histogram plot
hist_filename = f"{subject_id}_rh_pRF_histograms.png"
hist_filepath = os.path.join(save_path, hist_filename)
fig_hist.savefig(hist_filepath, dpi=300, bbox_inches='tight')
plt.close(fig_hist)  # Close the figure to free memory
print(f"Histograms saved to: {hist_filepath}")

```

|![](/figures/pRF/sub-01_pRF_params_hist.png){width="900px" align=center}|
|:--:|
|**Distribution of pRF parameters**.|


### Plot the pRF maps on the flattened spherical cortical representation



```python
## Plot pRF maps
(fig, (left_ax, right_ax)) = plt.subplots(1,2, figsize=(4,2), dpi=72*4)

ny.cortex_plot(flatmaps['rh'], axes=left_ax,
                color=ecc,  # Use log-transformed eccentricity
                cmap=colors_ecc['matplotlib_cmap'], #'turbo_r',
                mask=total_rsq > 0.1,
                vmin=np.min(ecc), vmax=np.max(ecc)/8)  # Adjust vmin and vmax to log scale


ny.cortex_plot(flatmaps['rh'], axes=right_ax,
                color=polar, #np.degrees(polar),
                mask=total_rsq > 0.1,
                cmap=colors_polar['matplotlib_cmap'])

# Add inset axes for the colorbars
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import Wedge

# Inset for eccentricity colorbar
ecc_inset = inset_axes(left_ax, width="30%", height="30%", loc="upper right")
ecc_inset.set_aspect('equal')
ecc_inset.set_xlim(-1.5, 1.5)
ecc_inset.set_ylim(-1.5, 1.5)
ecc_inset.set_axis_off()


# Create concentric rings from inner to outer
num_ecc_colors = len(colors_ecc["hex"])
for i, color in enumerate(colors_ecc["hex"]):
    inner_radius = i / num_ecc_colors
    outer_radius = (i + 1) / num_ecc_colors
    
    # Create a ring (using a wedge with a 360-degree arc)
    ring = Wedge((0, 0), outer_radius, 0, 360, width=outer_radius-inner_radius, color=color)
    ecc_inset.add_patch(ring)

# # Create concentric rings with logarithmic spacing
# num_ecc_colors = len(colors_ecc["hex"])
# log_space = np.logspace(np.log10(0.05), np.log10(1.0), num_ecc_colors + 1)
# log_space = log_space / log_space[-1]

# for i, color in enumerate(colors_ecc["hex"]):
#     inner_radius = log_space[i]
#     outer_radius = log_space[i + 1]
#     ring = Wedge((0, 0), outer_radius, 0, 360, width=outer_radius-inner_radius, color=color)
#     ecc_inset.add_patch(ring)

# Inset for polar angle colorbar using matplotlib's pie function
polar_inset = inset_axes(right_ax, width="30%", height="30%", loc="upper right")
polar_inset.set_aspect('equal')
polar_inset.set_axis_off()

# Use pie chart for the polar angle colorbar
num_polar_colors = len(colors_polar["hex"])
patches, texts = polar_inset.pie([1]*num_polar_colors, colors=colors_polar["hex"], 
                               startangle=180, counterclock=False)  # Start at left, go clockwise

left_ax.axis('off')
right_ax.axis('off')

# Save the plot with a descriptive filename
plot_filename = f"{subject_id}_run_{run}_{hemi}_pRF_maps_with_colorbars.png"
plot_filename = f"{subject_id}_averaged_{hemi}_pRF_maps_with_colorbars.png"
plot_filepath = os.path.join(save_path, plot_filename)
fig.savefig(plot_filepath, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {plot_filepath}")
```

### Plot the pRF maps on inflated surfaces

```python
## Plot pRF maps on inflated surfaces
from nilearn import plotting, surface

# Set hemispheres to process
hemispheres = ['lh', 'rh']


hemi = hemispheres[1]
run=1

# Get the inflated surfaces from the FreeSurfer subject
inflated_mesh = os.path.join(fs_pth, subject_id, 'surf', f'{hemi}.inflated')
sulc_map = os.path.join(fs_pth, subject_id, 'surf', f'{hemi}.sulc')

# Load pRF parameters for the current hemisphere
#pRF_params_path = os.path.join(save_path, f'pRF_params_run_{run}_{hemi}.npy')
pRF_params_path = os.path.join(save_path, f'pRF_params_averaged_{hemi}.npy')
pRF_params = np.load(pRF_params_path, allow_pickle=True).item()

# Extract parameters
x = pRF_params['x']
y = pRF_params['y']
sigma = pRF_params['sigma']
total_rsq = pRF_params['total_rsq']

# Calculate derived measures
ecc = np.abs(x + 1j*y)
polar = np.angle(x + 1j*y)

time_series_path = os.path.join(func_pth, f'{hemi}.tseries_run{run}.mgh')
time_series = np.squeeze(nib.load(time_series_path).get_fdata())
print(time_series.shape)
n_vertices = time_series.shape[0]
print(f"{hemi} has {n_vertices} vertices")
# Initialize arrays with zeros
ecc_surf = np.zeros(n_vertices)
polar_surf = np.zeros(n_vertices)

# Map data to appropriate vertices (using flatmap index)
cortex_index = flatmaps[hemi].prop('index')
ecc_surf[cortex_index] = ecc 
polar_surf[cortex_index] = polar

# Apply mask to show only significant voxels
mask = total_rsq > 0.1
ecc_surf[cortex_index[~mask]] = 0
polar_surf[cortex_index[~mask]] = 0


# view = plotting.view_surf(inflated_mesh, ecc_surf, threshold=0.5,
#                           bg_map=sulc_surf_fn)
# view

# Eccentricity map
view_ecc = plotting.view_surf(
    inflated_mesh, 
    ecc_surf, 
    threshold=0.1,  # Only show values > 0.1
    bg_map=sulc_map,
    cmap=colors_ecc['matplotlib_cmap'], # Good for eccentricity
    symmetric_cmap=False,
    vmax=np.percentile(ecc[mask], 95)  # Use 95th percentile to avoid outliers
)
view_ecc

# Polar angle map
view_polar = plotting.view_surf(
    inflated_mesh, 
    polar_surf, 
    threshold=0.1,
    bg_map=sulc_map,
    cmap=colors_polar['matplotlib_cmap'],  # Circular colormap good for angles
    symmetric_cmap=True
)
view_polar

```

### Save HTML for the 3D visualization

```python
# Save visualizations as HTML (interactive) and PNG (static image)
html_ecc_path = os.path.join(save_path, f'{subject_id}_{hemi}_eccentricity_3D.html')
html_polar_path = os.path.join(save_path, f'{subject_id}_{hemi}_polar_3D.html')
print(f"Saved 3D visualizations for {hemi} to {save_path}")
view_ecc.save_as_html(html_ecc_path)
view_polar.save_as_html(html_polar_path)
```

Interactive 3D visualization a population receptive field (pRF) eccentricity and polar angle map depicted on an inflated cortical surface representation for the left hemisphere:


<figure>
    <iframe src="https://rawcdn.githack.com/nicogravel/researchLog_template/fd3cc222bb62b3bacf5a2d855a4adaf5748cbc62/docs_local/source/figures/pRF/lh_eccentricity_3D.html" width="100%" height="500px" frameborder="0"></iframe>
    <figcaption><strong>pRF eccentricity.</strong> Population receptive field mapping of the left hemisphere visual cortex. Colorbar represent the eccentricity preferences across the cortical surface (colorbar units are in degree of visual angle from the fixation point).</figcaption>
</figure>

<figure>
    <iframe src="https://rawcdn.githack.com/nicogravel/researchLog_template/fd3cc222bb62b3bacf5a2d855a4adaf5748cbc62/docs_local/source/figures/pRF/lh_polar_3D.html" width="100%" height="500px" frameborder="0"></iframe>
    <figcaption><strong>pRF polar angle.</strong> Population receptive field mapping of the left hemisphere visual cortex. Colorbar represent polar angle preferences across the cortical surface (colorbar units are in radians).</figcaption>
</figure>


As a proof of concept, we managed to compute retinotopic maps using one subject and one run using prfpy (a python package for pRF mapping). After some adjustments we will have an accurate, minimalistic and completely transparent and clear pipeline to work data in individual native space level.


