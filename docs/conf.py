#!/usr/bin/env python3

"""
conf
====

Generation of documentation.
"""

from os.path import abspath
from sys import path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List, Tuple, Union

path.insert(0, abspath("./../src"))

# pylint: disable=wrong-import-position, unused-import, import-error,
import sausage_links  # noqa: E402, F401

# pylint: disable=invalid-name, redefined-builtin

extensions: "List[str]" = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

source_suffix: str = ".rst"
master_doc: str = "index"

autodoc_default_options: "Dict[str, Union[bool, str]]" = {
    "private-members": True,
    "special-members": "__init__, __repr__, __str__, __call__",
    "show-inheritance": True,
    "members": True,
    "exclude-members": "__weakref__",
}

intersphinx_mapping: "Dict[str, Tuple[str, None]]" = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
todo_include_todos: bool = True

project: str = "sausage_links"
author: str = "Aleksandr F. Mikhaylov (ChelAxe) <chelaxe@gmail.com>"
copyright: str = "D.F.H. ChelAxe 2005"
version: str = sausage_links.__version__
release: str = sausage_links.__version__
language: str = "en"
show_authors: bool = True

html_theme: str = "alabaster"
html_show_sourcelink: bool = False
html_show_copyright: bool = False
html_experimental_html5_writer: bool = True
html_theme_options: "Dict[str, Union[str, bool]]" = {
    "logo": "images/logo.png",
    "description": "Sausage Links",
    "fixed_sidebar": True,
    "sidebar_collapse": True,
    "show_powered_by": False,
    "show_relbars": True,
}

html_static_path: "List[str]" = ["_static"]
html_css_files: "List[str]" = ["css/style.min.css"]
html_js_files: "List[str]" = ["js/script.min.js"]
html_favicon: str = "_static/favicon.ico"
mathjax_path: str = "js/MathJax/MathJax.js"

latex_paper_size: str = "a4"
latex_logo: str = "_static/images/logo.png"
latex_font_size: str = "14pt"
latex_documents: "List[Tuple[str, str, str, str, str]]" = [
    (
        "index",
        "sausage_links.tex",
        "sausage_links",
        "Aleksandr F. Mikhaylov (ChelAxe) <chelaxe@gmail.com>",
        "howto",
    )
]
