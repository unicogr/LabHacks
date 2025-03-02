---
layout: default
title: "Results"
comments: true
---

# <span style="color:black"> Results </span>


## Example pipeline: pRF maping using 7T-fMRI data


	> This is a work in progress!  


Here the preprocessing for the functional retinotopy data. First we create an environment with unset variables (so when we run it again things do no get scrambled). Here we "summon" our favorite neuroimaging software packages and define paths:


```shell
#!/bin/bash
FSLDIR=/home/nicolas/Programas/fsl 
. ${FSLDIR}/etc/fslconf/fsl.sh
PATH=${FSLDIR}/bin:${PATH}
export FSLDIR PATH


# Data folders
export FREESURFER_HOME=/home/nicolas/Programas/freesurfer-linux-ubuntu22_amd64-7.4.0/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export PATH=/home/nicolas/Programas/ants-2.5.4/bin:$PATH


# Clear all variables 
unset current_dir
unset data_folder
unset pth
unset subj_id
unset subj
unset ret_folders
unset moving_images
unset static_images
unset sorted_folders


# Define the current working directory
current_dir=$(pwd)

# Define the paths based on the current working directory
export data_folder=/home/nicolas/Documents/Paris/UNICOG/Analyses/fMRIdata/iCORTEX
export pth=${data_folder}/sub-00/func

# Define the subject ID and subject folder
export subj_id=cg220008-2898_001
export subj=sub-00

# Change to the subject's data directory
cd ${data_folder}/${subj_id}

```
  
  
Next, we find the files with RET1, RET2, RET* in their name, excluding those with SBRef:


```shell
# Find all folders with the string RET1, RET2, RET* in their name, excluding those with SBRef
ret_folders=$(find . -type d -name "*AP-RET*" ! -name "*SBRef*")

# Declare variable for moving_images and static_images
declare -A moving_images
declare -A static_images

# Populate the variable and indices using IFS (Internal Field Separator)
IFS=$'\n' sorted_folders=($(sort <<<"${ret_folders[*]}"))
unset IFS

# Initialize the counter
counter=1

for folder in "${sorted_folders[@]}"; do
    moving_images["${counter}"]="${folder}"

    # Extract the first six digits from the folder name
    folder_name=$(basename "${folder}")
    folder_index=$(echo "${folder_name}" | awk -F'_' '{print $1}')
    
    # Subtract 2 from the first six digits to get the static index
    static_index=$(printf "%06d" $((10#${folder_index} - 2)))

    # Find the corresponding folder with the static_index
    static_folder=$(find . -type d -name "${static_index}*")
    
    # Save the names of the folders in the variable
    if [ -n "${static_folder}" ]; then
        static_images["${counter}"]="${static_folder}"
    fi

    echo "Index for static image: ${static_index}"
    echo "Index for moving image: ${folder_index}"

    counter=$((counter + 1))
done

for index in $(seq 1 ${#moving_images[@]}); do
    moving_image=${moving_images[${index}]}
    static_image=${static_images[${index}]}

    echo "Name for moving image: ${moving_image}"
    echo "Name for static image: ${static_image}"
done


```


And convert the 'dicom' files within these folders to 'nifti':

```shell

# Run dcm2niix_afni for moving_images and static_images in ascending order
for index in $(seq 1 ${#moving_images[@]}); do
    moving_image=${moving_images[${index}]}
    static_image=${static_images[${index}]}

    # Run dcm2niix_afni for moving_image
    dcm2niix_afni -o ${pth} -z y -f "moving_images_${index}" ${data_folder}/${subj_id}/${moving_image}

    # Run dcm2niix_afni for static_image
    if [ -n "${static_image}" ]; then
        dcm2niix_afni -o ${pth} -z y -f "static_images_${index}" ${data_folder}/${subj_id}/${static_image}
    fi
done

# Print completion message
echo "dcm2niix_afni processing and renaming completed for all images."


```

Apply slice timing correction:

```shell
# Slice time correct the NIfTI files using 3dTshift
for index in $(seq 1 ${#moving_images[@]}); do
    moving_nifti="${pth}/moving_images_${index}.nii.gz"
    static_nifti="${pth}/static_images_${index}.nii.gz"

    if [ -f "${moving_nifti}" ]; then
        3dTshift -verbose -TR 2 -tpattern altplus -ignore 0 -tzero 0 -Fourier -prefix "${pth}/tshift_moving_images_${index}.nii.gz" "${moving_nifti}"
    fi

    if [ -f "${static_nifti}" ]; then
        3dTshift -verbose -TR 2 -tpattern altplus -ignore 0 -tzero 0 -Fourier -prefix "${pth}/tshift_static_images_${index}.nii.gz" "${static_nifti}"
    fi
done

# Print completion message
echo "Slice time correction completed for all images."


```

Then motion correction:


```shell
# Motion correct the output of moving_images using 3dvolreg
for index in $(seq 1 ${#moving_images[@]}); do
    tshift_moving_nifti="${pth}/tshift_moving_images_${index}.nii.gz"

    if [ -f "${tshift_moving_nifti}" ]; then
        3dvolreg -verbose -prefix "${pth}/volreg_moving_images_${index}.nii.gz" "${tshift_moving_nifti}"
    fi
done

# Print completion message
echo "Motion correction completed for moving images."

```

Now is time for distortion correction. Note that the filedmap is computed using the original data, and the results applied to the slice-timing and motion corrected data. For illustration pruposes, here we use fsl here but AFNI or ANTS may in some cases be preferable. 

```shell
## Compute warps and apply distortion correction for each run
# Create the acquisition parameters file
cat <<EOT > ${pth}/acqparams.txt
0 -1 0 0.05
0 1 0 0.05
EOT

for index in $(seq 1 ${#moving_images[@]}); do   
 
    # Combine AP and PA images into a single 4D file
    fslroi ${pth}/moving_images_${index}.nii.gz ${pth}/AP_image.nii.gz 0 1
    fslroi ${pth}/static_images_${index}.nii.gz ${pth}/PA_image.nii.gz 0 1
    fslmerge -t ${pth}/combined_AP_PA.nii.gz ${pth}/AP_image.nii.gz ${pth}/PA_image.nii.gz

    # Run topup
    topup --imain=${pth}/combined_AP_PA.nii.gz --datain=${pth}/acqparams.txt --config=b02b0.cnf --out=${pth}/topup_results --iout=${pth}/hifi_b0.nii.gz --fout=${pth}/fieldmap.nii.gz

    # Apply the distortion correction to the volreg moving images
    moving_image="${pth}/volreg_moving_images_${index}.nii.gz"
    corrected_moving_image="${pth}/corrected_moving_images_${index}.nii.gz"
    applytopup --imain=${moving_image} --datain=${pth}/acqparams.txt --inindex=1 --topup=${pth}/topup_results --out=${corrected_moving_image} --method=jac

    # Clean up topup results
    rm ${pth}/AP_image.nii.gz ${pth}/PA_image.nii.gz ${pth}/combined_AP_PA*
    rm ${pth}/hifi_b0*
    rm ${pth}/fieldmap.nii.gz
    rm ${pth}/topup_results*
    
    echo "Distortion correction completed for moving image ${index}."

done

# Print completion message
#rm ${pth}/acqparams.txt
echo "Distortion correction completed for all moving images."

```

Now we can align corrected data to the subject's anatomical image using "boundary based registration", provided we have run freesurfer successfully on a 1mm iso-volumetric resampled anatomical data of the subject:


```shell

# Align corrected data to the subject's anatomical image

# Define the FreeSurfer subject directory
export SUBJECTS_DIR=$FREESURFER_HOME/subjects
export subj=sub-00_iso
export pth=${data_folder}/sub-00/func

# Perform affine registration using FreeSurfer's bbregister for all corrected_moving_images_*
for index in $(seq 1 ${#moving_images[@]}); do
    corrected_moving_image=${pth}/corrected_moving_images_${index}.nii.gz
    registered_image=${pth}/registered_moving_images_${index}_iso.nii.gz
    registration_matrix=${pth}/registration_matrix_${index}.dat

    # Find the brain.mgz file for the current subject
    brain_mgz=${SUBJECTS_DIR}/${subj}/mri/brain.mgz

    # Run bbregister for affine registration
    bbregister --s ${subj} --mov ${corrected_moving_image} --reg ${registration_matrix} --init-header --init-fsl --t2 --bold

    # Apply the registration to the functional image
    mri_vol2vol --mov ${corrected_moving_image} --targ ${brain_mgz} --reg ${registration_matrix} --o ${registered_image} --no-resample

    echo "Affine registration completed for corrected moving image ${index}."
done

# Print completion message
echo "Affine registration completed for all corrected moving images."


```

Finally, for now, we check the results visually and apply manual corrections if needed:

```shell

# Use tkregister2 to verify the registration
for index in $(seq 1 ${#moving_images[@]}); do
    corrected_moving_image=${pth}/corrected_moving_images_${index}.nii.gz
    registration_matrix=${pth}/registration_matrix_${index}.dat
    brain_mgz=${SUBJECTS_DIR}/${subj}/mri/brain.mgz

    tkregister2 --mov ${corrected_moving_image} --targ ${brain_mgz} --reg ${registration_matrix} --surf

    echo "Verification with tkregister2 completed for corrected moving image ${index}."
done

# Print completion message
echo "Verification with tkregister2 completed for all corrected moving images." 


```

Let us have a look at the registered data for a single run using **freeview*:

```shell
#!/bin/bash


# Data folders
export FREESURFER_HOME=/home/nicolas/Programas/freesurfer-linux-ubuntu22_amd64-7.4.0/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export PATH=/home/nicolas/Programas/ants-2.5.4/bin:$PATH

export subj=sub-00_iso
export data_folder=/home/nicolas/Documents/Paris/UNICOG/Analyses/fMRIdata/iCORTEX
export pth=${data_folder}/sub-00/func
export nifti=lh.corrected_moving_images_1_iso.mgh

export nifti=registered_moving_images_1_iso.nii.gz
freeview -f $SUBJECTS_DIR/${subj}/surf/lh.white -viewport 3d \
         -v ${pth}/${nifti}  -viewport 3d

```

|![](/figures/freeview.png){height="600px" align=center}|
|:--:|
|**Freeview**.|



So far all semi-automatic! Next steps:

* Fine tune coregsitration of anatomical to functional using 'antsRegistration'.
* Compute pRFs using an occipital mask.
* Refactoring this to preprocess more subjects.
* Organize the results in BIDS format.


Now we switch to python. The following has been adapted from excellent Noah Benson's [tutorial](https://github.com/noahbenson/neuropythy-tutorials/blob/master/tutorials/plotting-2D.ipynb):

```python
import os, sys, six # six provides python 2/3 compatibility
import numpy as np
import scipy as sp

# The neuropythy library is a swiss-army-knife for handling MRI data, especially
# anatomical/structural data such as that produced by FreeSurfer or the HCP.
# https://github.com/noahbenson/neuropythy
import neuropythy as ny

import matplotlib as mpl
import matplotlib.pyplot as plt
import ipyvolume as ipv


fs_pth = '/home/nicolas/Programas/freesurfer-linux-ubuntu22_amd64-7.4.0/freesurfer/subjects/'
subject_id = 'sub-00_iso'
sub = ny.freesurfer_subject([fs_pth + subject_id])
```

Get V1 coordinats fom the fsaverage registration of the subjects

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


```

Use neuropythy projection method to get the flat patch indices in the original surface:


```python
method = 'orthographic' # or: equirectangular, sinusoidal, mercator
radius = np.pi/2

# Now, we make the projections:
map_projs = {}
for h in ['lh', 'rh']: 
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

Plot flat patches and medial wall: 

```python
# We'll make two axes, one for each hemisphere.
(fig, (left_ax, right_ax)) = plt.subplots(1,2, figsize=(4,2), dpi=72*4)
# Make sure there isn't a bunch of extra space around them.
fig.subplots_adjust(0,0,1,1,0,0)

ny.cortex_plot(flatmaps['lh'], axes=left_ax)
ny.cortex_plot(flatmaps['rh'], axes=right_ax)

left_ax.axis('off')
right_ax.axis('off');

(fig, (left_ax, right_ax)) = plt.subplots(1,2, figsize=(4,2), dpi=72*4)
fig.subplots_adjust(0,0,1,1,0,0)


lh_cortex_label = flatmaps['lh'].prop('cortex_label')
rh_cortex_label = flatmaps['rh'].prop('cortex_label')


ny.cortex_plot(flatmaps['lh'], axes=left_ax,
               color=lh_cortex_label.astype('float'),
               cmap='inferno')
ny.cortex_plot(flatmaps['rh'], axes=right_ax,
               color=rh_cortex_label.astype('float'),
               cmap='inferno')

left_ax.axis('off')
right_ax.axis('off');   
```


Load co-registered and surface projected time series and compute t-SNR

```python
import nibabel as nib
import numpy as np

# Load the .mgh files
# Define the path to the functional image
pth = '/home/nicolas/Documents/Paris/UNICOG/Analyses/fMRIdata/iCORTEX/sub-00/func/'

lh_surfBOLD = 'lh.corrected_moving_images_1_iso.mgh'
rh_surfBOLD = 'rh.corrected_moving_images_1_iso.mgh'

# Load the projected time series
lh_time_series_path = os.path.join(pth, 'lh.corrected_moving_images_1_iso.mgh')
rh_time_series_path = os.path.join(pth, 'rh.corrected_moving_images_1_iso.mgh')

lh_time_series = np.squeeze(nib.load(lh_time_series_path ).get_fdata())
rh_time_series = np.squeeze(nib.load(rh_time_series_path).get_fdata())

print(lh_time_series.shape)

flatmaps = {h: mp(sub.hemis[h]) for (h,mp) in map_projs.items()}

lh_cortex_index = flatmaps['lh'].prop('index')
rh_cortex_index = flatmaps['rh'].prop('index')



# Calculate the temporal-SNR (temporal standard deviation of the time series)
lh_tsnr = np.std(lh_time_series[lh_cortex_index,:], axis=1)
rh_tsnr = np.std(rh_time_series[rh_cortex_index,:], axis=1)


print(lh_tsnr.shape)


ny.cortex_plot(flatmaps['lh'], axes=left_ax,
               color=lh_tsnr,
               alpha='V1_weight')


ny.cortex_plot(flatmaps['rh'], axes=right_ax,
               color=rh_tsnr,
               alpha='V1_weight')

left_ax.axis('off')
right_ax.axis('off');
```

Some preliminary figures:

|![](/figures/tSNR_V1.png){height="600px" align=center}|
|:--:|
|**Temporal SNR in V1**.|


|![](/figures/tSNR_outsideV1.png){height="600px" align=center}|
|:--:|
|**Temporal SNR outside V1**.|


Remember, this is work in progress! 






The neuroimaging python package **Neuropythy** is very versatile but a little cumbersome to learn. See here for its [documentation](https://nben.net/docs/neuropythy/html/genindex.html), and [here](https://nben.net/Retinotopy-Tutorial/) for a nice retinotopy tutorial, and [here](https://nben.net/MRI-Geometry/) for details on MRI Data Representation and Geometry.

**Next**: using [prfpy](https://github.com/VU-Cog-Sci/prfpy) to compute population receptive field maps.


## <span style="color:lightblue">Discussion📜</span>



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
