---
layout: default
title: "fMRI"
comments: true
---

# <span style="color:black">Surface-based fMRI</span>


An important step in using functional MRI (fMRI) is the design of stimuli to target specific cortical regions and functions. Computational neuroimaging of the human visual cortex often relies on standard retinotopic paradigms that reflect the structure of the visual cortex (*e.g.*, rotating wedges, expanding rings, drifting bars) {cite:p}`Wandell_2007`. Provided we have a good alignment between functional (*e.g.* T2) and anatomical (*e.g.* T1) MRI mages, these stimuli enable the mapping of receptive field properties at the population level. However, in order to achieve this, fMRI and MRI images must be preprocessed in non-trivial ways {cite:p}`Polimeni_2018`. There is no out-of-the box solution for this. For example, proposed solutions such as fMRIprep only work reliably after heavy customization. Else, systematic methodological error may inadvertently affect the subsequent analyses. To avoid mislead and confusion, here we illustrate the basic pre-processing steps that are part of many software packages, toolboxes and in-house pipelines customized for and by different neuroimaging labs. The final details will depend on the type of data we have at hand and what we ant to achieve. A completely open and transparent example helps in achieving this.
  
In this tutorial, we will use a single subject from the *iCORTEX 7T-fMRI* dataset to illustrate the basic preprocessing steps typically performed to obtain a good functional-to-anatomical match.

 > **What we will learn?** 


* We will **not** learn today how to use BIDS or run an out-of-the-box toolbox. Today's tutorial does not cover this. 

* To demystify the mystery around fMRI preprocessing by showing a simple, yet clear and transparent pipeline with one subject and one single run. For multiple runs, between-scan motion correction is needed. T1 copies matched to each run can improve co-registration by aligning functional-matched T1s to the original T1 used for segmentation. We’ll cover this in part two.

* Additionally, we will learn some basic shell script commands and python. 

* Here we do not fully cover manual edition of the segmentation and registration. Manual improvements of these two steps can greatly improve the results. 

* We intentionally leave some gaps so the user can experience the challenge of figuring out solutions too. Figuring out solution oneself is an important drive in learning.


 >   **Requirements:**

* Linux. Here we use Ubuntu 22 or 24. 
* For the shell-script based part: `AFNI`, `Freesurfer`, `FSL` and `ANTS` (optional for now).
* For the python based part: `pyenv`, `scipy`, `numpy`, `ipyvolume`, and -crucially, `neuropythy`.
* If you bring your own data, be sure to run *freesurfer's* `recon-all` on the anatomical volume. 




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



## **1st part**: Preprocessing of MRI and fMRI data at 7T


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

There many options, here we apply within-scan rigid-body {cite:p}`Nestares_2000` using `AFNI`. 

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

|![](/figures/Freeview.png){width="800px" align=center}|
|:--:|
|**Freeview**. We can clearly see the modulation of the signal by the drifting bar used in the visual field mapping stimuli. We are going to use this later in order to compute pRF maps.|


### Summary I

So far all semi-automatic! Next steps:

* Fine-tuning of the functional-to-anaotmical volume alignment/co-registration (*e.g.* using `antsRegistration`).
* Compute pRFs using an occipital mask.
* Refactoring this to preprocess more subjects and organize the inputs and outputs results in **BIDS** format.


## **2nd part**:  Mapping fMRI data to a cortical surface reconstruction

Here we project the fMRI data to the cortical manifold reconstruction obtaind in freesurfer. Ideally, we want to include only gray matter voxels.  To better achieve this goal we 

 


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

# Input path for label and output names for mask
label_dir=${SUBJECTS_DIR}/${subj}/label
output_mask=${pth}/cortex_mask.nii.gz
masked_func=${pth}/cortex_masked_func.nii.gz


# Convert cortex label to volume for left hemisphere
mri_label2vol \
  --label ${label_dir}/lh.cortex.label \
  --temp ${corrected_moving_image} \
  --reg ${registration_matrix}  \
  --subject ${subj} \
  --hemi lh \
  --o ${pth}/lh_cortex_mask.nii.gz \
  --fill-ribbon

# Convert cortex label to volume for right hemisphere
mri_label2vol \
  --label ${label_dir}/rh.cortex.label \
  --temp ${corrected_moving_image} \
  --reg ${registration_matrix}  \
  --subject ${subj} \
  --hemi rh \
  --o ${pth}/rh_cortex_mask.nii.gz \
  --fill-ribbon

# Combine left and right hemisphere masks
fslmaths ${pth}/lh_cortex_mask.nii.gz -add ${pth}/rh_cortex_mask.nii.gz -bin ${output_mask}

# Apply mask to functional image
fslmaths ${corrected_moving_image} -mas ${output_mask} ${masked_func}

echo "Finished masking functional data with cortex label"
```

Once we have masked the gray matter, we can project it to the the cortical manifold.


```shell
# Project the volumetric data onto the left hemisphere surface
mri_vol2surf --mov ${pth}/cortex_masked_func.nii.gz \
  --projfrac 0.25 \
  --interp trilinear \
  --hemi lh \
  --out ${lh_output_surface} \
  --surf white \
  --nvox ${nvoxfile} \
  --reg ${registration_matrix} \
  --mask ${label_dir}/lh.cortex.label


# Project the volumetric data onto the right hemisphere surface
mri_vol2surf --mov ${pth}/cortex_masked_func.nii.gz \
  --projfrac 0.25 \
  --interp trilinear \
  --hemi rh \
  --out ${lh_output_surface} \
  --surf white \
  --mask ${label_dir}/rh.cortex.label \
  --nvox ${nvoxfile} \
  --reg ${registration_matrix} 
  

# Print completion message
echo "Projection of volumetric data onto the surface"

```

We can also add the flag `--cortex` to mask the outputs, but this misses the fact that the interpolation may have taken non-gray matter voxels as input. One can also define a mask: `--mask ${label_dir}/lh.cortex.label`.

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


fs_pth = '/home/... .../freesurfer-linux-ubuntu22_amd64-7.4.0/freesurfer/subjects/'
subject_id = 'sub-00_iso'
sub = ny.freesurfer_subject([fs_pth + subject_id])
```

### Get V1 coordinates from the *fsaverage* registration of the subjects

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


### Plotting the temporal signal to noise ratio (t-SNR) onto the cortical mesh

Load co-registered and surface projected time series and compute t-SNR:

```python
import nibabel as nib
import numpy as np

# Load the .mgh files
# Define the path to the functional image
pth = '/home/... .../fMRIdata/iCORTEX/sub-00/func/'


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



|![](/figures/tSNR_V1.png){width="800px" align=center}|
|:--:|
|**Temporal SNR (tSNR) in V1**. The tSNR is temporal average of the raw fMRI recording of each individual site, not the bold signal. It highlights low intensitiy recordings ,outliers (*e.g.* draining veins), stable signal, non gray matter, etc.|



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



low_pass    = 0.08      
high_pass   = 0.02     
TR          = 2      
confounds   = None      

V1_ts_lh  = signal.clean(V1_ts_lh.T, confounds=confounds, detrend=detrend, standardize=standardize, 
                           filter='butterworth', low_pass=low_pass, high_pass=high_pass, tr=TR)

V1_ts_rh  = signal.clean(V1_ts_rh.T, confounds=confounds, detrend=detrend, standardize=standardize, 
                           filter='butterworth', low_pass=low_pass, high_pass=high_pass, tr=TR)



# Plot the time series
fig, ax = plt.subplots(1,2, figsize=(12,8), dpi=300, facecolor="w")
aspect = 1.5

# Zscore
V1_ts_lh = stats.zscore(V1_ts_lh, axis=0)
V1_ts_rh = stats.zscore(V1_ts_rh, axis=0)

# Plot the left hemisphere time series
im_1 = ax[0].imshow(V1_ts_lh[:,150:200].T, cmap='bwr', aspect=aspect)
ax[0].set_ylabel('site', fontsize=10)
ax[0].set_xlabel('TR (2 sec)', fontsize=10)
cbar = plt.colorbar(im_1,cax = fig.add_axes([0.23, 0.25, 0.15, 0.044 ]),extend='both',orientation='horizontal')     
cbar.ax.tick_params(labelsize=8)
cbar.set_label('BOLD (%)',fontsize=12)

# Plot the right hemisphere time series
im_2 =ax[1].imshow(V1_ts_rh[:,50:100].T, cmap='bwr', aspect=aspect)
ax[1].set_xlabel('TR (2 sec)', fontsize=10)
cbar = plt.colorbar(im_2,cax = fig.add_axes([0.64, 0.25, 0.15, 0.044 ]),extend='both',orientation='horizontal')     
cbar.ax.tick_params(labelsize=8)
cbar.set_label('BOLD (%)',fontsize=12)



# Save the time series
np.save(save_path + 'V1_ts_lh.npy', V1_ts_lh)
np.save(save_path + 'V1_ts_rh.npy', V1_ts_rh)

```


|![](/figures/bold.png){width="900px" align=center}|
|:--:|
|**BOLD signals**. Blood oxygen level dependent signals are typically estimated as follows. First, by subtracting the mean of each channel (centering at zero, and optionally, the global mean too. Second, detrending a (**e.g.** using a discrete cosine transform with basis two, etc), filtering (**e.g.** 0.01 *Hz* and 0.1 *Hz*, depending on the protocol) and removing confounds (optional). Third, obtaining the percentage signal change, and again, z-scoring along space or time if needed. All these steps are to be customized according to the user's needs and can eventually lead to confusion. **Never take preprocessing for granted!**. Here we plot the first 100 sites (vertices) for each hemisphere for illustration. Se the traveling waves? Yeah, these are evoked by the drifting bar. We are now ready to compute some pRFs! The python implementation, [prfpy](https://github.com/VU-Cog-Sci/prfpy), is non-trivial (as everything in life 😅 ?), significant work is needed to adjust (based on empirical priors that are not always obvious) the parameters needed for the grid and iterative search based optimization -crucial for finding the best fitting models.|
 

Remember, this is work in progress! 



### Summary II


The neuroimaging python package **Neuropythy** is very versatile but a little cumbersome. See here for its [documentation](https://nben.net/docs/neuropythy/html/genindex.html), and [here](https://nben.net/Retinotopy-Tutorial/) for a nice retinotopy tutorial, and [here](https://nben.net/MRI-Geometry/) for details on MRI Data Representation and Geometry.

### What's next?

**Next**: using [prfpy](https://github.com/VU-Cog-Sci/prfpy) to compute population receptive field maps.

## **3rd part**:  pRF mapping


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

|![](/figures/pRF_maps_lh.png){width="900px" align=center}![](/figures/pRF_maps_rh.png){width="900px" align=center}|
|:--:|
|**Cortical site (vertex) selectivity to visual field position estimated using pRF modeling**. Data for a single subject and run.|


And remember...  this is work in progress!
