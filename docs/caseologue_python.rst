.. _tests:


Caseologue custom python script
=================================


This custom pyhton script **complement** the test performed by the ELK reasoner and our custom version of the robot report tool.
It alows us to test for **specific features** of the EDAM ontology (e.g. check for wikipedia links or for mandatory property)

Installation & Usage
---------------------

As of this version, this tool is not available as a pyhton of conda package. To use this tool on your owl file you will need to clone the public GitHub repository: 
::
   git clone git@github.com:edamontology/edam-validation.git

Move to the caseologue directory and run :
:: 
   EDAM_PATH=<path to test data> python3  caseologue.py --options  

By default the scrip will run all tests. You can filter the tests on error level using these options:
::
  -e, --error      runs all error tests
  -E, --essential  runs all essential tests
  -c, --curation   runs all curation tests

Repartition of tests can be seen in the source code `here <file:///home/llamothe/work/edam-validation/caseologue/doc/_build/html/_modules/caseologue.html#suite>`_.

Options
~~~~~~~~~~

* **Error**: tests insuring this semantic and sintactic consistency of the ontology, that are mandatory to pass for a pull request to be merged on the GitHub repository. 
* **Essential**: error tests that can be applicable to other side of the EDAM ontology such as EDAM geo of EDAM bioimaging.
* **Curation**: unmandatory tests, ran by maintainers, that, if failed, do not compromise the integrity or the logical structure of the ontology. The error level is also a staging area for tests that should be error or essential but still raise errors needing to be fixed. 

Tests documentation
------------------------

This pyhton script uses the unittest modules to test and report errors of the tested EDAM owl file. 

For (almost) each test described bellow, the script calls a custom `SPARQL <https://www.w3.org/TR/rdf-sparql-query/>`_ query, using the RDFlib library, and report the error in a comprehensive table. 


.. automodule:: caseologue
    :members:
    :no-private-members:
