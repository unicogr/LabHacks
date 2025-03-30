𝙻𝚊𝚋 𝚑𝚊𝚌𝚔𝚜 
#########


ℝecently, I encountered an article discussing the ongoing replication crisis in biology
:footcite:p:`Oza_2023`. The article highlights a known issue in scientific research :footcite:p:`Nezer_2020`: even when different teams analyze the same data using the same methods, replication often leads to different results. The article made me think of overconfident chefs - they don’t just follow recipes, but sneak in their favorite ingredients into every dish before we even taste it. One key reason I pondered, is that scientists frequently approach problems with some degree of preconceived beliefs, which translates to applying a rigid "toolbox" of hypotheses to the challenges they encounter. While the need for collective consensus is clear, these beliefs do not necessarily generalize from team to team, leaving the public confronted with what appears as inconsistent decisions during statistical analysis. Ironically, sometimes these decisions, made with the best of intentions, spread as software packages, and are then used by other researchers to test different hypothesis in their own data. Coincidentally, as I worked to align my scientific software implementations with best practices, I stumbled upon another noteworthy piece in the now defunct Twitter. The `post <https://twitter.com/lakens/status/1718654122516156777>`_ provided the much needed, *so zu sagen*, plumber's perspective: 

	*Statisticians should be less like priests and more plumbers. I don't care what you personally believe is the right way to do things - if I have a specific problem, I want to know all possible solutions that might fix it, what their limitations are, and how much each would cost.*                     `Daniël Lackens <https://twitter.com/lakens>`_



The tutorials presented here are inspired on `The Good Research Code Handbook <https://goodresearch.dev>`_, by `Patrick Mineault <https://scholar.google.com/citations?user=gpQg9uQAAAAJ&hl=en>`_. Everything needed to reproduce this pages in a Github repo based on `Sphinx <https://www.sphinx-doc.org/en/master/>`_, `Markdown <https://daringfireball.net/projects/markdown/>`_ and `reStructuredText <https://en.wikipedia.org/wiki/ReStructuredText>`_. The first tutorial is a guide to produce a personalised *research log* that can be easily `adapted <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>`_ to one's individual needs. As a bonus, it comes with an example on how to set up a python project and document its code and functions using `docstring <https://en.wikipedia.org/wiki/Docstring>`_. The second tutorial is about how to implement a simple yet clear preprocessing pipeline for surface reconstruction of fMRI data. The third is still on the making and it will be a an extension of the second one, aiming to compute population receptive models using, again, simple yet clear open source packages.


.. note::

	This online resource is meant to be a *living document*. This means it may contain errors and corrections. New content will be added over time. Please check back regularly for the latest version.


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
