# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'researchLog'
copyright = ''
author = 'Nicolas Gravel'
release = ''

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
import os
import sys
import alabaster


templates_path = ['_templates']
exclude_patterns = []

extensions = [
    'myst_parser',
    'alabaster',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinxcontrib.bibtex',
    'sphinx.ext.autosectionlabel',
    'sphinx_disqus.disqus',
    'sphinx.ext.viewcode'
]
typehints_fully_qualified = False
disqus_shortname = ''


myst_enable_extensions = [
    "attrs_image",
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
] 

bibtex_bibfiles = ['references.bib']
bibtex_encoding = 'utf-8-sig'
bibtex_default_style = 'unsrt'
bibtex_reference_style = 'super'



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#html_theme_path = [alabaster.get_path()]
html_theme = 'alabaster' #'classic' # 'alabaster' #'bizstyle' #
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}


html_static_path = ['_static']
html_css_files = ['custom.css']

def setup(app):
    app.add_css_file('custom.css')

html_theme_options = {
    'logo': 'logo.png',
    'logo_text_align': 'left',
    'github_banner': False,
    'description': 'Research Log',
    'description_font_style': 'Caslon',
    'page_width': '100%',
    'body_max_width': 'auto',
    'sidebar_width': '20%',
    'show_relbars': True,
    'show_powered_by' : False,
    'fixed_sidebar': True

}

import mock

MOCK_MODULES = ['numpy', 'matplotlib', 'matplotlib.pyplot','statsmodels','statsmodels.api']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()


'''

# Switch from conda to pyenv (Python 3.8.19)

pyenv install 3.8.19
pyenv virtualenv 3.8.19 Sphinx
pyenv activate Sphinx
pip install -r requirements.txt



#which leads to this error:
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
myst-parser 3.0.1 requires sphinx<8,>=6, but you have sphinx 5.2.0 which is incompatible.
sphinxcontrib-bibtex 2.6.3 requires docutils!=0.18.*,!=0.19.*,>=0.8, but you have docutils 0.19 which is incompatible.

# To get rid of adds and use Giscus, follow the instructions in the following link:
https://www.patrickthurmond.com/blog/2023/12/11/commenting-is-available-now-thanks-to-giscus

# Snippets to build the html files, sync them to the docs folder and push the changes to the remote repository

# Activate sphinx environment
# conda activate sphinx
pyenv activate Sphinx

# Navigate to the directory containing the conf.py file
cd /home/nicolas/Documents/GitHubProjects/researchLog_template/docs_local/

# Build the html files
make clean; make html

# Sync the html files to the docs folder
rsync -a --delete /home/nicolas/Documents/GitHubProjects/researchLog_template/docs_local/build/html /home/nicolas/Documents/GitHubProjects/researchLog_template/docs/

# Navigate to the directory containing the conf.py file
cd  /home/nicolas/Documents/GitHubProjects/researchLog_template/

# Add, commit and push the changes
git add .
git commit -m "fixed refs"
git push -u origin main


'''
