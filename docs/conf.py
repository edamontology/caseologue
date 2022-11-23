# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EDAM Continuous Interagtion custom tool'
copyright = '2022, Lucie Lamothe, Alban Gaignard, Hervé Ménager, Matúš Kalaš'
author = 'Lucie Lamothe, Alban Gaignard, Matúš Kalaš, Hervé Ménager'

import os
import sys
sys.path.insert(0, os.path.abspath('../caseologue_python'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc','sphinx.ext.coverage','sphinx.ext.viewcode','sphinx.ext.autosummary',
 # The Napoleon extension allows for nicer argument formatting.
    'sphinx.ext.napoleon'
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary

language = 'python'
source_suffix = '.rst'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
