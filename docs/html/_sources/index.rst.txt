----------------
**Lab tutorials**    
----------------

*Towards open and reproducible NeuroImaging*
#######################################################

The tutorials presented here are inspired on `The Good Research Code Handbook <https://goodresearch.dev>`_, by `Patrick Mineault <https://scholar.google.com/citations?user=gpQg9uQAAAAJ&hl=en>`_. as a Github repo based on `Sphinx <https://www.sphinx-doc.org/en/master/>`_, `Markdown <https://daringfireball.net/projects/markdown/>`. 


Before we begin, I wanted to share a story. Both as a primer for the tutorials and as an example of how to use [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText). You can consider the following as a sort of *Lorem ipsum*:

ℝecently, I encountered an article discussing the ongoing replication crisis in biology
:footcite:p:`Oza_2023`. The article highlights a persistent issue in scientific research: even when different teams analyze the same data using the same methods, replication often leads to different results :footcite:p:`Nezer_2020`. One key reason, the authors argue, is that scientists frequently approach problems with some degree of preconceived beliefs, which translates to applying a rigid "toolbox" of hypotheses to the challenges they encounter. While the need for collective consensus is clear, these beliefs do not necessarily generalize from team to team, leaving the public confronted with what appears as inconsistent decisions during statistical analysis. Ironically, sometimes these decisions, made with the best of intentions, spreads as software packages, and are then used by other researchers to test different hypothesis in their own data.

Coincidentally, as I worked to align my implementations with best practices, I stumbled upon another noteworthy piece in the now defunct Twitter. The `post <https://twitter.com/lakens/status/1718654122516156777>`_ provided the much needed, *so zu sagen*, plumber's perspective: 

	*Statisticians should be less like priests and more plumbers. I don't care what you personally believe is the right way to do things - if I have a specific problem, I want to know all possible solutions that might fix it, what their limitations are, and how much each would cost.*                     `Daniël Lackens <https://twitter.com/lakens>`_





.. note::

	This online resource is meant to be a *living document*. This means it may contain errors and corrections. New content will be added over time. Please check back regularly for the latest version.

.. image:: /figures/Misc/Eaton_1985.png
	  :width: 750
	  :align: center
	  :alt: Diagram of the Sufficiency and Necessity Principle found in an old moleskine. Likely seen in a conference some years ago by Haanne De Jaegher or Shaun Gallagher.
	  
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
