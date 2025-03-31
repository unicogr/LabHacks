𝙻𝚊𝚋 𝚑𝚊𝚌𝚔𝚜 
#########


Here you will find a collection of tutorials and code snippets to help you get started with your own research log and high field fMRI analyses. 
  
The goal is to provide a simple and clear way to document your research process, from data collection to analysis and visualization.
  
The tutorials are designed to be easy to follow and adaptable to your own needs. They are based on open source software and best practices in research reproducibility [#handbook]_. The tutorials are written in a way that allows you to easily copy and paste the code into your own projects, and they include links to additional resources for further reading.
  
The tutorials are organized into three main sections:
  
1. **Sphinx**: This section provides a guide to setting up a personalized research log using `Sphinx <https://www.sphinx-doc.org/en/master/>`_, a documentation generator that makes it easy to create and maintain documentation for your projects. As a bonus, it comes with an example on how to set up a python project and document its code and functions using `docstring <https://en.wikipedia.org/wiki/Docstring>`_, `Markdown <https://daringfireball.net/projects/markdown/>`_ and `reStructuredText <https://en.wikipedia.org/wiki/ReStructuredText>`_. 
  
2. **fMRI**: This section provides a guide to preprocessing fMRI data using `FreeSurfer <https://surfer.nmr.mgh.harvard.edu/>`_, `AFNI <https://afni.nimh.nih.gov/>`_, `FSL <https://fsl.fmrib.ox.ac.uk/fsl/docs/#/>`_, `NeuroPythy <https://github.com/noahbenson/neuropythy/wiki>`_ , `Nilearn <https://nilearn.github.io/stable/index.html>`_, as well as other open source software packages.
  
3. **pRF**: This section provides a guide to computing population receptive fields using the `prfpy <https://prfpy.readthedocs.io/en/latest/>`_ package, a simple and clear python package for visual field mapping.

4. **References**: This section provides a list of references cited in the tutorials, as well as additional resources for further reading.
  


.. raw:: html

	<figure>
		<iframe src="https://rawcdn.githack.com/nicogravel/researchLog_template/fd3cc222bb62b3bacf5a2d855a4adaf5748cbc62/docs_local/source/figures/pRF/lh_polar_3D.html" width="100%" height="500px" frameborder="0"></iframe>
        <figcaption><strong>Figure 1:</strong> Population receptive field mapping of the left hemisphere visual cortex. Colorbar represent polar angle preferences across the cortical surface (colorbar units are in radians).</figcaption>
	</figure>


	
Philosophy
==========
	
ℝecently, I encountered an article discussing the ongoing replication crisis in biology
:footcite:p:`Oza_2023`. The article highlights a known issue in scientific research :footcite:p:`Nezer_2020`: even when different teams analyze the same data using the same methods, replication often leads to different results. The article made me think of overconfident chefs - they don’t just follow recipes, but sneak in their favorite ingredients into every dish before we even taste it. One key reason I pondered, is that scientists frequently approach problems with some degree of preconceived beliefs, which translates to applying a rigid "toolbox" of hypotheses to the challenges they encounter. While the need for collective consensus is clear, these beliefs do not necessarily generalize from team to team, leaving the public confronted with what appears as inconsistent decisions during statistical analysis. Ironically, sometimes these decisions, made with the best of intentions, spread as software packages, and are then used by other researchers to test different hypothesis in their own data. Coincidentally, as I worked to align my scientific software implementations with best practices, I stumbled upon another noteworthy piece in the now defunct Twitter. The `post <https://twitter.com/lakens/status/1718654122516156777>`_ provided the much needed, *so zu sagen*, plumber's perspective: 

	*Statisticians should be less like priests and more plumbers. I don't care what you personally believe is the right way to do things - if I have a specific problem, I want to know all possible solutions that might fix it, what their limitations are, and how much each would cost.*                     `Daniël Lackens <https://twitter.com/lakens>`_



.. note::

	This online resource is meant to be a *living document*. This means it may contain errors and corrections. New content will be added over time. Please check back regularly for the latest version.


This project builds on resources from the community [#handbook]_.




**********
Comments
**********

.. raw :: html

    <div class="giscus-container">
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
    </div>
    
    	    
**********
Content
**********
.. toctree::
      :maxdepth: 2
      :numbered:          

      1_Sphinx
      2_fMRI
      3_VFM
      References

      

   
**************
Python package
**************

.. toctree::
    :maxdepth: 1
    :caption: Codebook:

    modules

Indices
=======

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

 
      
**********
References
**********

.. footbibliography::

.. [#handbook] The tutorials presented here are inspired by `The Good Research Code Handbook <https://goodresearch.dev>`_, by `Patrick Mineault <https://scholar.google.com/citations?user=gpQg9uQAAAAJ&hl=en>`_. 

