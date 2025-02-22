---
layout: default
title: "Intro"
comments: true
---



# <span style="color:black">Proposals</span>

<hr style="border: 1px solid black; width:100%;"></hr>


## The Human Visual Cortex through Computational NeuroImaging

An important step in using functional MRI is the design of stimuli to target specific cortical regions and functions. Computational neuroimaging of the human visual cortex often relies on standard retinotopic paradigms that reflect the structure of the visual cortex (*e.g.*, rotating wedges, expanding rings, drifting bars) {cite:p}`Wandell_2007, Schira_2010`. These types of stimuli enable the mapping of retinotopic cortical areas using methods such as population receptive field (pRF) modeling. Here we build upon a recently developed framework {cite:p}`Aquino_2014a` that predicts the BOLD response for a given stimulus. In short, the framework works as follows. First, retinal contrast responses are calculated for a given input. Second, the retinal responses are mapped onto a cortical surface by using a model of retinotopic mapping from the visual field to V1 {cite:p}`Benson_2018`. Third, the neuronal responses on cortex are approximated using a mean field model {cite:p}`Robinson_2016, Pang_2016`, and we use feed-forward projections from V1 to V2, and V3 that include realistic receptive field sizes {cite:p}`Harvey_2011`. Fourth, the hemodynamic response is modeled using the recently proposed spatiotemporal hemodynamic response function (st-HRF) {cite:p}`Drysdale_2010`, {cite:p}`Aquino_2014b` that takes into account hemodynamic propagation across cortical tissue. Fifth, the BOLD signal response is calculated from the estimated hemodynamics {cite:p}`Obata_2004`.




## <span style="color:lightblue">Feedback✍️</span>

```{disqus}
```


