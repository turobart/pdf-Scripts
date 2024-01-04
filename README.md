# pdf-Scripts
Python scripts for working with .pdf files.
---
findCitations.py
---
Script for finding occurances of citations in pdf file in square bracket format. Supports single ([1]), two ([1,2]) and more than two ([1-3]) citations. Default style is bold non-italic brackets and numbers.
Script returns list of occurances of all citations in format: 'Ref [1] on pages:	1, 3, 10, \r' in txt file. Some pages can be set to be ignored.
Script uses [pyMuPDF](https://github.com/pymupdf/PyMuPDF) module for operation.


AddToolTips.py
---
Script for adding tooltips for abbreviations in .pdf. It also sets labels of pages and sets properties of .pdf file.
Abbreviations and tooltips text are provided in separate .txt files, see example abbrevs.txt and full_names.txt files.
Tooltips are in form of an invisible button placed on top of an abbreviation.
Text detection is done by [pyMuPDF](https://github.com/pymupdf/PyMuPDF) module.


simple_operations.py
---
Scripts for merging pdfs and adding bookmarks to pdfs.
Script uses [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) module for operation.
