---
layout: default
title: "Results"
comments: true
---

# <span style="color:black"> Results </span>

## Example figure: *From Visual Stimulus to BOLD* 


|![](/figures/barMap.png){height="400px"}![](/figures/stHRF_BOLD_sim_cortex.png){height="400px"}|
|:--:|
|**Figure #. Cortical BOLD response.** *Left*: [Drifting bar aperture used in population receptive field mapping](https://drive.google.com/file/d/14MRGpbjya8KwtLup8kAvR8EmKF5svNSr/view?usp=sharing). *Right*: [Cortical BOLD responses to the drifting bar stimuli depicted on a flattened cortical reconstruction for a single hemisphere](https://drive.google.com/file/d/17JkrsSYfcZkWn2gZsGGb1wURvY_gLqTL/view?usp=sharing) (using Freesurfer's *fsaverage*). Black traces indicate the borders between visual cortical maps V1, V2 and V3 within 0.1 and 6 degrees of visual eccentricity. Within each of these maps, nearby neurons respond to nearby locations in the visual image, with this property (receptive fields) extending along cortical hierarchy. Neuronal responses across cortical sites were approximated using a mean field approximation of retino-cortical inputs, resulting on stimuli-dependent estimates for the neuronal drive in V1, V2 and V3. These estimates are then translated to BOLD activity using an empirically established spatiotemporal hemodynamic response function (st-HRF).|


## Example pipeline: p-RF maping using 7T-fMRI data


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


# Clear all variables and dictionaries
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

# Declare dictionaries for moving_images and static_images
declare -A moving_images
declare -A static_images

# Populate the dictionaries and indices using IFS (Internal Field Separator)
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
    
    # Save the names of the folders in the dictionaries
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

Now we can align corrected data to the subject's anatomical image using "boundary based registration", provided we have run freesurfer succesfully on the anatomical data of the subject:


```shell

# Define the FreeSurfer subject directory
export SUBJECTS_DIR=$FREESURFER_HOME/subjects

# Perform affine registration using FreeSurfer's bbregister for all corrected_moving_images_*
for index in $(seq 1 ${#moving_images[@]}); do
    corrected_moving_image=${pth}/corrected_moving_images_${index}.nii.gz
    registered_image=${pth}/registered_moving_images_${index}.nii.gz
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

So far all semi-automatic! Next steps:

* Fine tune coregsitration of anatomical to functional using 'antsRegistration'.
* Compute pRFs using an occipital mask.
* Refactoring this to preprocess more subjects.
* Organize the results in BIDS format.



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
