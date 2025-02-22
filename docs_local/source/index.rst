----------------
**Tutorial I:**    
----------------

Documenting research with *Sphinx*
###################################
  
*************************************************************
**Goal:** keep track of progress during the research process.   
*************************************************************
  
This `tutorial <https://github.com/nicogravel/UNICOG_ResearchLog>`_ is an adaptation of `The Good Research Code Handbook <https://goodresearch.dev>`_, by `Patrick Mineault <https://scholar.google.com/citations?user=gpQg9uQAAAAJ&hl=en>`_. It is delivered as a Github repo based on `Sphinx <https://www.sphinx-doc.org/en/master/>`_, `Markdown <https://daringfireball.net/projects/markdown/>`_ and `reStructuredText <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>`_ (rendered using `Github pages <https://jekyllrb.com/docs/github-pages/>`_). Its purpose is to provide us with a scaffold for a personalised *research log* that can be easily adapted to one's individual needs.     
  
  
Before we begin, I wanted to share a couple of stories, both as a primer and as an example of how to use the resource, its functionalities, etc. 
    
Recently, I encountered an article discussing the ongoing replication crisis in biology :footcite:p:`Oza_2023`. Why so often, the article stressed, results obtained by different teams using the same data (and following the same inquiries) are difficult to replicate :footcite:p:`Nezer_2020`. According to the article, scientists tend to integrate their beliefs into their hypothesis-making machinery (*i.e.* in the form of a *toolbox*) to every problem they stumble upon in the field. While the need for collective consensus is clear, potentially diverging decisions taken during a statistical assessment may bring forth confusion rather than clarity. With all its good intentions, excess trust in a method should not lead us into the realm of extreme scientific belief or `scientificism/scientism <https://www.merriam-webster.com/dictionary/scientism>`_ (i.e. *the urge to trust on the temporary answers our good ol' metric provide rather than the underlying problem that inspired them in first place*). Coincidentally, while trying to reach consensus in my own work, I stumbled upon another noteworthy piece in the now defunct Twitter. The `post <https://twitter.com/lakens/status/1718654122516156777>`_ provided the much needed, *so zu sagen*, plumber's perspective: 

  *Statisticians should be less like priests and more plumbers. I don't care what you personally believe is the right way to do things - if I have a specific problem, I want to know all possible solutions that might fix it, what their limitations are, and how much each would cost.*                     `Daniël Lackens <https://twitter.com/lakens>`_


If reflecting on this wasn't already challenging, the so-called *Sufficiency and Necessity Principle* :footcite:p:`Eaton_1985` then came to mind. I remember having heard about it some years ago in a `conference <https://www.mind-and-brain.de/events/scientific-events-postdoctoral-program-2012-2018/an-enactive-approach-to-psychiatry-and-psychotherapy?no_cache=1&sword_list%5B0%5D=guendelman&cHash=ca4f193024e67e08bfc74b613468bd71>`_. Was it a talk  about the integration of causality in enactive approaches by `Shaun Gallagher <https://scholar.google.com/citations?user=B1gMcHkAAAAJ&hl=en>`_? or      the talk *Loving and knowing: Towards a humane science of subjectivity* by `Hanne De Jaegher <https://scholar.google.com/citations?user=lNV02IsAAAAJ&hl=en>`_? Can't remember exactly, but I wrote the damn diagram in my moleskine (see diagram below).
  
One of these "*principles*" often discussed in the context of practical inference of causality. The principle is based on the idea that if a certain variable is necessary for a certain outcome, then the absence of that variable will lead to the absence of the outcome. On the other hand, if a variable is sufficient for an outcome, then the presence of that variable will lead to the presence of the outcome, as shown in the following diagram: 

|
    
.. image:: /figures/Eaton_1985.png
      :width: 750
      :align: center 
        
  
Both anecdotes matter to us, as the process of experimental design and statistical inference that we engage in often involves the equivalent of  "deactivating" or "activating" a *region of interest* using various tools (*e.g.* perceptual/cognitive/behavioral tasks, pharmacological interventions, animal models, *etc...*) and recording modalities (*e.g.* electrophysiology, fMRI, *etc...*), measuring changes in behavior before and after manipulation, and then drawing causal links between variables. If deactivation leads to suppression of the desired outcome while activation induces that outcome, a causal link *may* be inferred. However, it's essential to consider potentially *hidden* variables that may influence this relationship  :footcite:p:`Gomez-Marin_2017`.  
        
For a simple and clear critique of the *Sufficiency and Necessity Principle* limitations, I recommend this recent article by `Grace Lindsay <https://scholar.google.com/citations?user=4kETHY4AAAAJ&hl=en>`_ on `The Transmitter: Claims of necessity and sufficiency are not well suited for the study of complex systems <https://doi.org/10.53053/IHMY3378>`_ or  `Causal Circuit Explanations of Behavior: Are Necessity and Sufficiency Necessary and Sufficient? <https://link.springer.com/chapter/10.1007/978-3-319-57363-2_11>`_ by `Alex Gomez-Marin <https://scholar.google.com/citations?user=JKt3ReoAAAAJ&hl=en>`_.

Do not take what is written here textual. To be clear, there is no endorsement here of the so-called *Sufficiency and Necessity Principle* or pointers to an assumed correlation-causality link. Moreover, this text is intentionally human-like and meant *to be* rather *mysteriös und rätselhaft*, instead of *crystal*-clear, as it is my own **non-chatGPT** *Lorem ipsum* (and English is not my mother tongue!) as well as an ongoing exercise in public/collaborative writing. From humans to humans. As such, it may/will contains errors and mutate from time to time. Finally, this online resource is meant to be a *living document* that will be updated regularly to keep track of my thoughts, ideas, and progress regarding scientific blogging and teaching. It is also a way to spread with the broader scientific community an enthusiasm to share and connect, to get feedback, and to learn from others.  
  
I hope you find the tutorial useful and interesting. If you have any comments or suggestions, please feel free to contact me. I would love to hear from you.
  

**********
Comments
**********
.. disqus::
  
    
**********
Content
**********
.. toctree::
      :maxdepth: 2
      :numbered:          

      1_intro
      2_okr
      3_results
      4_tutorials
      5_refs
      

   
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
