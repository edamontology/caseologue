
.. _installation:

Installation
=============

As of this version, this tool is not available as a pyhton of conda package. To use this tool on your owl file you will need to clone the public GitHub repository: 
::
   git clone git@github.com:edamontology/edam-validation.git

Move to the xxxx directory and run :
:: 
   EDAM_PATH=<_path to test data_> python3  XXXXX.py  

By default the scrip will run all tests. You can filter the tests on error level using these options:
::
  -e, --error      runs all error tests
  -E, --essential  runs all essential tests
  -c, --curation   runs all curation tests

Repartition of tests can be seen in the source code `here <file:///home/llamothe/work/edam-validation/caseologue/doc/_build/html/_modules/caseologue.html#suite>`_.

* **Error**: test insuring this semantic and sintactic consistency of the ontology, that are mandatory to pass for a pull request to be merged on the GitHub repository. 
* **Essential**: error test that can be applicable to other side of the EDAM ontology such as EDAM geo of EDAM bioimaging. ???
* **Curation**: unmandatory tests, ran by maintainers, that, if failed, do not compromise the integrity or the logical structure of the ontology. The error level is also a staging area for tests that should be error or essential but still raise errors needing to be fixed. 

..
   .. list-table:: Title
      :widths: 20 50
      :header-rows: 1

      * - Error level
      - Description
      * - Error
      - test insuring this semantic and sintactic consistency of the ontology, that are mandatory to pass for a pull request to be merged on the GitHub repository.
      * - Essential
      - error test that can be applicable to other side of the EDAM ontology such as EDAM geo of EDAM bioimaging. ???
      * - Curation
      - unmandatory tests, ran by maintainers, that, if failed, do not compromise the integrity or the logical structure of the ontology. The error level is also a staging area for tests that should be error or essential but still raise errors needing to be fixed. 


