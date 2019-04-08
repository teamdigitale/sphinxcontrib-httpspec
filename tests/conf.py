import os
import sys

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx import addnodes

sys.path.append(os.path.abspath("."))

extensions = ["sphinxcontrib.httpspec"]

html_theme = "classic"


# templates_path = ['_templates']
source_suffix = [".rst"]

project = "Sphinx <Tests>"
copyright = "2010-2016, Georg Brandl & Team"
# If this is changed, remember to update the versionchanges!
version = "0.6"
release = "0.6alpha1"
today_fmt = "%B %d, %Y"
exclude_patterns = ["_build", "**/excluded.*"]
keep_warnings = True
pygments_style = "sphinx"
show_authors = True
numfig = True


html_last_updated_fmt = "%b %d, %Y"


# modify tags from conf.py
