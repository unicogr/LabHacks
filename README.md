# ResearchLog, minimal working example

See here, for the Github page: https://nicogravel.github.io/UNICOG_ResearchLog

This tutorial is a collaborative effort with [Christophe Pallier](https://github.com/chrplr). Please see [here](https://github.com/chrplr/mynotebook) for a boiled down (or "*distilled*") version. 



<details>
  <summary><span style="color:#3382FF"> 1.- Set up research project codebook folder using Python, Sphinx and Github</span></summary>  

  First, we want to create a project folder that will contain the research code (Matlab, Python, Jupyter notebooks, etc), the data, the results and the documentation:

  ```
  ├── docs
    └──.nojekyll
    └──index.html
  ├── docs_local
    └── source
    └── _static
    └── _templates
    └── figures
    └── myContent.md
    └── index.rst
    └── references.bib
  ├── results
  └── .gitignore
  └── requirements.txt
  └── README.md
  ```


Inside docs/index.html we add:

  ```html
  <meta http-equiv="refresh" content="0; url=./html/index.html" />
  ```
The folder `docs/html` will be copied from `docs_local/build/html` once we build the docs, as explained below. Meanwhile, the folder `docs_local` is added to `.gitignore`.

</details>

<br>

<details>
  <summary><span style="color:#3382FF"> 2.- Set up pyenv environment (first install pyenv)</span></summary>  

  We can then create a python environment locally and install Sphinx:

  ```shell
  pyenv install 3.8.19
  pyenv virtualenv 3.8.19 Sphinx
  pyenv activate Sphinx
  pip install -r requirements.txt
  ```

</details>


<br>
  
<details>
  <summary><span style="color:#3382FF"> 3.- Initialize or fork Github project</span></summary>  


  ```
  echo "# ResearchLog" >> README.md
  git init
  git add README.md
  git commit -m "1st commit"
  git branch -M main
  git remote add origin https://github.com/.../ResearchLog.git
  git push -u origin main
  ```

</details>

<br>
  
<details>
  <summary><span style="color:#3382FF"> 4.- Create a Python package</span></summary>  

  Create a `pyproject.toml` file in the root of your project: 
  
  ```shell
  cd ResearchLog
  touch pyproject.toml
  ```
  
  and add the following to `pyproject.toml`:

  ```toml
  [build-system]
  requires = ["setuptools", "wheel"]
  build-backend = "setuptools.build_meta"

  [project]
  name = "myCodeIsYourCode"
  version = "0.0.0"  # You can specify the version here
  description = "A short description of your project"
  readme = "README.md"
  requires-python = ">=3.8"


  [tool.setuptools.packages.find]
  where = ["."]

  ```
    
  Create myCodeIsYourCode directory an add empty `__init__.py` file to it, together with a python file that prints "hello world" to your package:
  
  ```shell
  mkdir myCodeIsYourCode
  cd myCodeIsYourCode
  touch __init__.py
  echo "print('hello world')" > helloworld.py
  ```

  Go to the root directory and install your package from the root directory:

  ```shell
  cd ..
  pip install -e .
  sphinx-apidoc -f -o docs_local/source myCodeIsYourCode
  ```

Try it:  

  ```shell
  python
  ```
  Then in python:

  ```python
  >>> import myCodeIsYourCode.helloworld
  hello world
  >>> exit()
  ```

</details>

<br>

<details>
  <summary><span style="color:#3382FF"> 5.- Generate project and code documentation using Sphinx</span></summary>  

  The folder `docs_local` will be used to generate the [sphinx](https://www.sphinx-doc.org/en/master/index.html) documentation. Then, we will copy the `build/html` to `docs`.

  ```shell
  cd /home/.../ResearchLog/docs_local/
  make clean; make html
  rsync -a --delete /home/.../ResearchLog/docs_local/build/html /home/.../ResearchLog/docs/
  ```

Edit `myCodeIsYourCode.rst`: add *:noindex:* to the end of the file, as follows:

```rst
Module contents
---------------

.. automodule:: myCodeIsYourCode
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:
```
 
Now enjoy building up your python package!

</details>
  
<br>
  
<details>
  <summary><span style="color:#3382FF"> 5.- Work: edit, make and commit</span></summary>  


  After these steps one wants to *make* the documentation locally. To build the documentation automatically, edit then the document `modules.rst` –if necessary, and do *make clean* followed by *make html*.

  ```shell
  cd docs_local
  make clean
  make html
  ```

  After adding new code and document everything, working on docstrings, etc, do not forget to commit the changes to Github and update both the documentation and the package. For example, if you write new python functions, do:

  ```shell
  pip install -e .
  sphinx-apidoc -f -o docs_local/source myCodeIsYourCode
  git add .
  git commit -m "replace setup.py for pyproject.toml, updates in docstrings, etc"
  git push -u origin main'
  ```

</details>
  
<br>