----------------
**Lab tutorials**    
----------------

*Towards open and reproducible NeuroImaging*
#######################################################
  
*************************************************************************************************************************************************************************
**Goals:** Learn how to create a research (*and code*) handbook, preprocess fMRI data, map cortical responses using custom techniques and visualize results.
*************************************************************************************************************************************************************************
  
The tutorials presented here are inspired on `The Good Research Code Handbook <https://goodresearch.dev>`_, by `Patrick Mineault <https://scholar.google.com/citations?user=gpQg9uQAAAAJ&hl=en>`_. as a Github repo based on `Sphinx <https://www.sphinx-doc.org/en/master/>`_, `Markdown <https://daringfireball.net/projects/markdown/>`_ and  I serve them`reStructuredText <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>`_ (rendered using `Github pages <https://jekyllrb.com/docs/github-pages/>`_). 

Before we begin, I wanted to share a story. Both as a primer for the tutorials and as an example of how to use [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText). You can consider the following as a very personal *Lorem ipsum*:

.. raw:: html
	
	<span style="font-family: 'Old English Text MT', fantasy; font-size: 2em;">R</span>ecently, I encountered an article discussing the ongoing replication crisis in biology
:footcite:p:`Oza_2023`. Why so often, the article stressed, results obtained by different teams using the same data (and following the same inquiries) are difficult to replicate :footcite:p:`Nezer_2020`. According to the article, scientists tend to integrate their beliefs into their hypothesis-making machinery (*i.e.* in the form of a *toolbox*) to every problem they stumble upon in the field. While the need for collective consensus is clear, potentially diverging decisions taken during a statistical assessment may bring forth confusion rather than clarity. With all its good intentions, excess trust in a method should not lead us into the realm of extreme scientific belief or `scientificism/scientism <https://www.merriam-webster.com/dictionary/scientism>`_ (i.e. *the urge to trust on the temporary answers our good ol' metric provide rather than the underlying problem that inspired them in first place*). Coincidentally, while trying to reach consensus in my own work, I stumbled upon another noteworthy piece in the now defunct Twitter. The `post <https://twitter.com/lakens/status/1718654122516156777>`_ provided the much needed, *so zu sagen*, plumber's perspective: 

	*Statisticians should be less like priests and more plumbers. I don't care what you personally believe is the right way to do things - if I have a specific problem, I want to know all possible solutions that might fix it, what their limitations are, and how much each would cost.*                     `Daniël Lackens <https://twitter.com/lakens>`_


.. note::

	This online resource is meant to be a *living document*. This means it may contain errors and corrections. New content will be added over time. Please check back regularly for the latest version.
  <span style="font-family: 'Old English Text MT', fantasy; font-size: 2em;">R</span>ecently, I encountered an article discussing the ongoing replication crisis in biology :footcite:p:`Oza_2023`. Why so often, the article stressed, results obtained by different teams using the same data (and following the same inquiries) are difficult to replicate :footcite:p:`Nezer_2020`. According to the article, scientists tend to integrate their beliefs into their hypothesis-making machinery (*i.e.* in the form of
  
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
