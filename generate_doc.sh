#!/bin/bash
# Shell script to generate documentation from the sources

#Delete the generated rst files if any
rm docs/source/customers.*
rm docs/source/modules.rst

#Generate new ones based on the source code
sphinx-apidoc -o docs/source customers

#Build the HTML output in build/
cd docs
make clean
make html
