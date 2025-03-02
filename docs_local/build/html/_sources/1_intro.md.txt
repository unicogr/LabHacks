---
layout: default
title: "Intro"
comments: true
---



# <span style="color:black">Proposals</span>

<hr style="border: 1px solid black; width:100%;"></hr>


## The Human Visual Cortex through Computational NeuroImaging

An important step in using functional MRI is the design of stimuli to target specific cortical regions and functions. Computational neuroimaging of the human visual cortex often relies on standard retinotopic paradigms that reflect the structure of the visual cortex (*e.g.*, rotating wedges, expanding rings, drifting bars) {cite:p}`Wandell_2007, Schira_2010`. These types of stimuli enable the mapping of retinotopic cortical areas using methods such as population receptive field (pRF) modeling. Here we build upon a recently developed framework {cite:p}`Aquino_2014a` that predicts the BOLD response for a given stimulus. In short, the framework works as follows. First, retinal contrast responses are calculated for a given input. Second, the retinal responses are mapped onto a cortical surface by using a model of retinotopic mapping from the visual field to V1 {cite:p}`Benson_2018`. Third, the neuronal responses on cortex are approximated using a mean field model {cite:p}`Robinson_2016, Pang_2016`, and we use feed-forward projections from V1 to V2, and V3 that include realistic receptive field sizes {cite:p}`Harvey_2011`. Fourth, the hemodynamic response is modeled using the recently proposed spatiotemporal hemodynamic response function (st-HRF) {cite:p}`Drysdale_2010`, {cite:p}`Aquino_2014b` that takes into account hemodynamic propagation across cortical tissue. Fifth, the BOLD signal response is calculated from the estimated hemodynamics {cite:p}`Obata_2004`.


|![](/figures/barMap.png){height="400px"}![](/figures/stHRF_BOLD_sim_cortex.png){height="400px"}|
|:--:|
|**Figure #. From Visual Stimulus to BOLD.** *Left*: [Drifting bar aperture used in population receptive field mapping](https://drive.google.com/file/d/14MRGpbjya8KwtLup8kAvR8EmKF5svNSr/view?usp=sharing). *Right*: [Cortical BOLD responses to the drifting bar stimuli depicted on a flattened cortical reconstruction for a single hemisphere](https://drive.google.com/file/d/17JkrsSYfcZkWn2gZsGGb1wURvY_gLqTL/view?usp=sharing) (using Freesurfer's *fsaverage*). Black traces indicate the borders between visual cortical maps V1, V2 and V3 within 0.1 and 6 degrees of visual eccentricity. Within each of these maps, nearby neurons respond to nearby locations in the visual image, with this property (receptive fields) extending along cortical hierarchy. Neuronal responses across cortical sites were approximated using a mean field approximation of retino-cortical inputs, resulting on stimuli-dependent estimates for the neuronal drive in V1, V2 and V3. These estimates are then translated to BOLD activity using an empirically established spatiotemporal hemodynamic response function (st-HRF).|


## <span style="color:lightblue">Feedback ✍️</span>

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
