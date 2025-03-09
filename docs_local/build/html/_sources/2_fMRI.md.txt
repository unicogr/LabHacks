---
layout: default
title: "fMRI"
comments: true
---

# <span style="color:black">Surface-based fMRI</span>


An important step in using functional MRI (fMRI) is the design of stimuli to target specific cortical regions and functions. Computational neuroimaging of the human visual cortex often relies on standard retinotopic paradigms that reflect the structure of the visual cortex (*e.g.*, rotating wedges, expanding rings, drifting bars) {cite:p}`Wandell_2007`. Provided we have a good alignment between functional (*e.g.* T2) and anatomical (*e.g.* T1) MRI mages, these stimuli enable the mapping of receptive field properties at the population level. However, in order to achieve this, fMRI and MRI images must be preprocessed in non-trivial ways. There is no out-of-the box solution for this. For example, proposed solutions such as fMRIprep only work reliably after heavy customization. Else, systematic methodological error may inadvertently affect the subsequent analyses. To avoid mislead and confusion, here we illustrate the basic pre-processing steps that are part of many software packages, toolboxes and in-house pipelines customized for and by different neuroimaging labs. The final details will depend on the type of data we have at hand and what we ant to achieve. A completely open and transparent example wil help us achieve this.
  
In this tutorial, we will use a single subject from the *iCORTEX 7T-fMRI* dataset to illustrate the basic preprocessing steps typically performed to obtain a good functional-to-anatomical match.

### What we will learn? 


* We will **not** learn today how to use BIDS or run an out-of-the-box toolbox. Today's tutorial does not cover this. 

* To demystify the mystery around fMRI preprocessing by showing a simple, yet clear and transparent pipeline with one subject and one single run.

* Additionally, we will learn some basic shell script commands and python. 


> *For multiple runs, between-scan motion correction is needed. SBRef scans (not used here) or T1 copies matched to each run can improve co-registration by aligning functional-matched T1s to the original T1 used for segmentation. We’ll cover this in part two.*    

Still on the making is the follow up part of this tutorial: *pRF mapping using 7T-fMRI data*. 


Requirements:

* Linux. Here we use Ubuntu 22 or 24. 
* For the shell-script based part: `AFNI`, `Freesurfer`, `FSL` and `ANTS` (optional for now).
* For the python based part: `scipy`, `numpy`, `ipyvolume`, and -crucially, `neuropythy`.
* If you bring your own data, be sure to run *freesurfer's* `recon-all` on the anatomical volume. 




## <span style="color:lightblue">Questions? 🦉</span>



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



## **1st part**: Mapping fMRI data to a cortical surface reconstruction


Here I have documented the essential preprocessing steps for the functional retinotopy data. 


The folder tree for the data ued in this tutorial:



/home/... ... /fMRIdata/iCORTEX   
├── cg220008-2898_001  
│   ├── 000001_AAHScout  
│   ├── 000002_AAHScout-MPR  
│   ├── 000003_b1-map-xfl-sag-Amplitude  
│   ├── 000004_b1-map-xfl-sag-Phase  
│   ├── 000005_b1-map-xfl-sag-B1-Ampli-CP-mode  
│   ├── 000006_b1-map-xfl-sag-VR  
│   ├── 000007_b0-gre-field-mapping  
│   ├── 000008_b0-gre-field-mapping  
│   ├── 000009_TEST-SAR-BOLD-SBRef  
│   ├── 000010_TEST-SAR-BOLD  
│   ├── 00011_mbep2d-TR1-1pt6mm-PA-SBRef  
│   ├── 000012_mbep2d-TR1-1pt6mm-PA  
│   ├── 000013_mbep2d-TR1-1pt6mm-AP-REST1-SBRef  
│   ├── 000014_mbep2d-TR1-1pt6mm-AP-REST1  
│   ├── 000015_mbep2d-TR2-1pt2mm-PA-SBRef  
│   ├── 000016_mbep2d-TR2-1pt2mm-PA  
│   ├── 000017_mbep2d-TR2-1pt2mm-AP-RET1-SBRef   
│   ├── 000018_mbep2d-TR2-1pt2mm-AP-RET1    
│   ├── 000019_mbep2d-TR2-1pt2mm-PA-SBRef  
│   ├── 000020_mbep2d-TR2-1pt2mm-PA  
│   ├── 000021_mbep2d-TR2-1pt2mm-AP-RET2-SBone-size-fits-allRef  
│   ├── 000022_mbep2d-TR2-1pt2mm-AP-RET2  
│   ├── 000023_mbep2d-TR2-1pt2mm-PA-SBRef  
│   ├── 000024_mbep2d-TR2-1pt2mm-PA  
│   ├── 000025_mbep2d-TR2-1pt2mm-AP-RET3-SBRef  
│   ├── 000026_mbep2d-TR2-1pt2mm-AP-RET3  
│   ├── 000027_mbep2d-TR2-1pt2mm-PA-SBRef  
│   ├── 000028_mbep2d-TR2-1pt2mm-PA  
│   ├── 000029_mbep2d-TR2-1pt2mm-AP-RET4-SBRef  
│   ├── 000030_mbep2d-TR2-1pt2mm-AP-RET4  
│   ├── 000031_mbep2d-TR1-1pt6mm-PA-SBRef  
│   ├── 000032_mbep2d-TR1-1pt6mm-PA  
│   ├── 000033_mbep2d-TR1-1pt6mm-AP-REST2-SBRef  
│   ├── 000034_mbep2d-TR1-1pt6mm-AP-REST2  
│   ├── 000035_t1-mp2rage-sag-iso0.75mm-INV1  
│   ├── 000036_t1-mp2rage-sag-iso0.75mm-INV1-PHS  
│   ├── 000037_t1-mp2rage-sag-iso0.75mm-INV2  
│   ├── 000038_t1-mp2rage-sag-iso0.75mm-INV2-PHS  
│   ├── 000039_t1-mp2rage-sag-iso0.75mm-T1-Images  
│   ├── 000040_t1-mp2rage-sag-iso0.75mm-UNI-DEN  
│   ├── 000041_t1-mp2rage-sag-iso0.75mm-UNI-Images  
│   ├── 000042_mbep2d-TR2-1pt2mm-PA-SBRef  
│   ├── 000043_mbep2d-TR2-1pt2mm-PA  
│   ├── 000044_mbep2d-TR2-1pt2mm-AP-CATV-SBRef  
│   ├── 000045_mbep2d-TR2-1pt2mm-AP-CATV  
│   ├── 000046_mbep2d-TR2-1pt2mm-AP-CATV-SBRef-split-1  
│   └── nifti  
├── pRF_log_images  
└── sub-00  
    ├── anat  
    ├── func  
    └── retinotopy  


### Set environment

First we create an environment with unset variables (so when we run it again things do no get scrambled). Here we "summon" our favorite neuroimaging software packages and define paths:


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
  
### Define file names and paths

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


### Get **nifti** files
And convert the `dicom` files within these folders to `nifti`:

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

### Apply slice timing correction

```shell
# Slice time correct the NIfTI files using 3dTshift
for index in $(seq 1 ${#moving_images[@]}); do
    moving_nifti="${pth}/moving_images_${index}.nii.gz"
    static_nifti="${pth}/static_images_${index}.nii.gz"

    if [ -f "${moving_nifti}" ]; then
        3dTshift -verbose -TR 2 -tpattern altplus -ignore 0 -tzero 0 -Fourier -prefix "${pth}/tshift_moving_images_${index}.nii.gz" "${moving_nifti}"
    fi

 
done

# Print completion message
echo "Slice time correction completed for all images."


```

### Apply motion correction


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

### Distortion correction

Now is time for distortion correction. Note that the fieldmap is computed using the original data, and the results applied to the slice-timing and motion corrected data. For illustration purposes, here we use `fsl` here but `AFNI` or `ANTS` may in some cases be preferable. 

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

### Cortical surface reconstruction
<details>
  <summary><span style="color:#3382FF">Wondering how to run `recon-all` ?</span></summary>  


The anatomical volume used in this tutorial was obtained as follows:

```shell
    export FREESURFER_HOME=/home/nicolas/Programas/freesurfer-linux-ubuntu22_amd64-7.4.0/freesurfer
    source $FREESURFER_HOME/SetUpFreeSurfer.sh
    export PATH=/home/nicolas/Programas/ants-2.5.4/bin:$PATH

    #### Divide UNI by T1 
    fslmaths ${subj}_uni.nii.gz -div ${subj}_t1.nii.gz ${subj}_unit1_div.nii.gz -odt float

    #### Check UNI by T1 division to find baseline noise empirically
    #fsleyes ${subj}_unit1_div.nii.gz

    #### Binarize INV2 (keep non-baseline values)
    fslmaths ${subj}_inv2.nii.gz -thr 150 ${subj}_inv2_bin.nii.gz -odt float

    #### Mask UNI by T1 division results with binarized INV2
    fslmaths  ${subj}_unit1_div.nii.gz -mas ${subj}_inv2_bin.nii.gz  ${subj}_t1_tmp.nii.gz -odt float

    #### Check masked UNI by T1 division to find outlier values
    #fsleyes ${subj}_t1_tmp.nii.gz

    #### Threshold UNI by T1 division to remove outliers
    fslmaths ${subj}_t1_tmp.nii.gz -uthr 5 ${subj}_t1_thr.nii.gz -odt float

    #### Correct T1 inhomogeneity (N4 algorithm) using ANTs
    N4BiasFieldCorrection -i ${subj}_t1_thr.nii.gz -o ${subj}_t1_corrected_N4.nii.gz -v -s 4 -c [50x50x50x50] -b [200] -t [0.15] -d 3

    #### Normalize between 0-256 using Freesurfer's mri_normalize
    mri_normalize -g 1 -mprage ${subj}_t1_corrected_N4.nii.gz ${subj}_t1_norm.nii.gz

    #### Check normalized T1
    fsleyes ${subj}_t1_corrected.nii.gz ${subj}_t1_norm.nii.gz

    #### Remove skull from corrected T1 using FSL (the -f 0.1 and -g 0.1 parameters are somewhat arbitrary and can be adjusted)
    bet ${subj}_t1_norm.nii.gz ${subj}_t1_brain.nii.gz -f 0 -g 0 -R -S -v

    # Remove redundant files, keep original inputs + t1_norm + t1_brain
    rm ${subj}_unit1_div.nii.gz ${subj}_inv2_bin.nii.gz ${subj}_t1_tmp.nii.gz ${subj}_t1_thr.nii.gz 

    #### Try recon-all with isotropic voxel size
    flirt -in ${subj}_t1_brain.nii.gz -ref ${subj}_t1_brain.nii.gz -applyisoxfm 1.0 -nosearch -out ${subj}_t1_brain_iso.nii.gz 

    recon-all -i ${subj}_t1_brain_iso.nii.gz -subjid ${subj}_iso -all
    recon-all -skullstrip -no-wsgcaatlas -s ${subj}_iso
    recon-all -autorecon2 -autorecon3 -s ${subj}_iso
    recon-all -i ${subj}_t1_brain_iso.nii.gz -subjid ${subj}_iso -make -no-isrunning
```
</details>



### Alignment
  
Now we can align (*co-register*) corrected data to the subject's anatomical image using "boundary based registration", provided we have run `freesurfer` successfully on a 1*mm* iso-volumetric resampled anatomical data of the subject:


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



```python
from nilearn import image, surface, plotting, signal

anat_pth = '/home/nicolas/Documents/Paris/UNICOG/Analyses/fMRIdata/iCORTEX/sub-00/anat/'
func_pth = '/home/nicolas/Documents/Paris/UNICOG/Analyses/fMRIdata/iCORTEX/sub-00/func/'

T1 = image.load_img(anat_pth + 'sub-00_t1_norm.nii.gz')
T2 = image.load_img(func_pth + 'registered_moving_images_1_iso_Tmean.nii.gz')
print(f'Dimensions of meanFunc: {T2}')

plotting.plot_stat_map(T2,bg_img=T1,title='T2 to T1 alignment',display_mode='ortho',cut_coords=(0,0,0),draw_cross=False)


```

|![](/figures/alignment.png){height="400px" align=center}|
|:--:|
|**Example alignment**.|


### Fine-tune alignment 

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

### Visual inspection

Let us have a look at the registered data for a single run using `freeview`:

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

|![](/figures/Freeview.png){height="600px" align=center}|
|:--:|
|**Freeview**. We can clearly see the modulation of the signal by the drifting bar used in the visual field mapping stimuli. We are going to use this later in order to compute pRF maps.|


### Summary I

So far all semi-automatic! Next steps:

* Fine-tuning of the functional-to-anaotmical volume alignment/co-registration (*e.g.* using `antsRegistration`).
* Compute pRFs using an occipital mask.
* Refactoring this to preprocess more subjects and organize the inputs and outputs results in **BIDS** format.


### Project times series to cortical surface

```shell
# Define the FreeSurfer subject directory
export SUBJECTS_DIR=$FREESURFER_HOME/subjects

# Define the paths for the input and output files
corrected_moving_image=${pth}/registered_moving_images_1_iso.nii.gz
lh_output_surface=${pth}/lh.corrected_moving_images_1_iso.mgh
rh_output_surface=${pth}/rh.corrected_moving_images_1_iso.mgh
registration_matrix=${pth}/registration_matrix_1.dat
nvoxfile=${pth}/nvoxfile_1.dat

# Find the brain.mgz file for the current subject
brain_mgz=${SUBJECTS_DIR}/${subj}/mri/orig.mgz

# Project the volumetric data onto the left hemisphere surface
mri_vol2surf --mov ${corrected_moving_image} \
  --projfrac 0.1 \
  --interp nearest \
  --hemi lh \
  --out ${lh_output_surface} \
  --surf white \
  --nvox ${nvoxfile} \
  --reg ${registration_matrix} 

# Project the volumetric data onto the right hemisphere surface
mri_vol2surf --mov ${corrected_moving_image} \
  --projfrac 0.1 \
  --interp nearest \
  --hemi rh \
  --out ${rh_output_surface} \
  --surf white \
  --nvox ${nvoxfile} \
  --reg ${registration_matrix} 

# Print completion message
echo "Projection of volumetric data onto the surface completed for corrected_moving_images_1.nii.gz."


```


### Get to Jupyter  

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

### Get V1 coordinats fom the *fsaverage* registration of the subjects

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

### Map functional data to a cortical mesh

Use `neuropythy` projection method to get the flat patch indices in the original surface:


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

### Plotting the temporal signal to noise ratio (t-SNR) on the cortical mesh

Load co-registered and surface projected time series and compute t-SNR:

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



|![](/figures/tSNR_V1.png){height="400px" align=center}|
|:--:|
|**Temporal SNR in V1**.|



### Obtaining BOLD percentage signal change

Load co-registered and surface projected time series and compute t-SNR:

```python
# Load the .mgh files
# Define the path to the functional image
pth = '/home/nicolas/Documents/Paris/UNICOG/Analyses/fMRIdata/iCORTEX/sub-00/func/'


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
lh_tsnr_ = np.std(lh_time_series[lh_cortex_index,:], axis=1)
rh_tsnr_ = np.std(rh_time_series[rh_cortex_index,:], axis=1)


print(lh_tsnr_.shape)


# Subtract the mean of each time series (channel) from the time series data
print('lh_time_series shape: ', lh_time_series.shape)
lh_tSeries = lh_time_series - np.mean(lh_time_series, axis=1, keepdims=True)
rh_tSeries = rh_time_series - np.mean(rh_time_series, axis=1, keepdims=True)

# Subtract global mean from each time series
lh_tSeries = lh_time_series - np.mean(lh_time_series.flatten(), keepdims=True)
rh_tSeries = rh_time_series - np.mean(rh_time_series.flatten(), keepdims=True)
print('demeaned time series shape: ', lh_tSeries.shape)

# Extract V1 time series for the left hemisphere
V1_ix = lh_v1_weight > 0.5
print(V1_ix.shape)
V1_ts_lh = lh_tSeries[lh_cortex_index[V1_ix],:]
print(V1_ts_lh.shape)

# Extract V1 time series for the right hemisphere
V1_ix = rh_v1_weight > 0.5
print(V1_ix.shape)
V1_ts_rh = rh_tSeries[rh_cortex_index[V1_ix],:]
print(V1_ts_rh.shape)

# Remove trends and convert to percent signal change
detrend     = True
standardize = 'psc'


print('V1_ts_lh shape: ', V1_ts_lh.shape)   



#V1_ts_lh = V1_ts_lh - 
#V1_ts_rh = V1_ts_rh - np.mean(V1_ts_rh, axis=1)

low_pass    = 0.08      
high_pass   = 0.02     
TR          = 2      
confounds   = None      

V1_ts_lh  = signal.clean(V1_ts_lh.T, confounds=confounds, detrend=detrend, standardize=standardize, 
                           filter='butterworth', low_pass=low_pass, high_pass=high_pass, tr=TR)

V1_ts_rh  = signal.clean(V1_ts_rh.T, confounds=confounds, detrend=detrend, standardize=standardize, 
                           filter='butterworth', low_pass=low_pass, high_pass=high_pass, tr=TR)


# Zscore
V1_ts_lh = stats.zscore(V1_ts_lh, axis=0)
V1_ts_rh = stats.zscore(V1_ts_rh, axis=0)


# Plot the time series
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Plot the left hemisphere time series
plt.sca(axs[0])
plt.imshow(V1_ts_lh[:,1:100].T, cmap='Spectral_r', aspect='auto')
plt.ylabel('site', fontsize=10)
plt.xlabel('TR', fontsize=10)
plt.colorbar()

# Plot the right hemisphere time series
plt.sca(axs[1])
plt.imshow(V1_ts_rh[:,1:100].T, cmap='Spectral_r', aspect='auto')
plt.xlabel('TR', fontsize=10)
plt.colorbar()

plt.show()

```




Remember, this is work in progress! 



### Summary II


The neuroimaging python package **Neuropythy** is very versatile but a little cumbersome to learn. See here for its [documentation](https://nben.net/docs/neuropythy/html/genindex.html), and [here](https://nben.net/Retinotopy-Tutorial/) for a nice retinotopy tutorial, and [here](https://nben.net/MRI-Geometry/) for details on MRI Data Representation and Geometry.

### What's next?

**Next**: using [prfpy](https://github.com/VU-Cog-Sci/prfpy) to compute population receptive field maps.


