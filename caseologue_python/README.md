# caseologue
caseologue is a CI python tool for the EDAM Ontology, grouping a set of tests (mostly using SPARQL queries) to validate the ontology. 

## Run Caséologue

Clone the repository, navigate to the `caseologue_python` folder, and install requirements:
```
pip install -r requirements.txt
```

In the following, replace the edampath and use your python. (On Windows you might need to replace `python3` with `python`.)
```
EDAM_PATH=../../edamontology/EDAM_dev.owl python3 caseologue.py 
```

Options:\
  -e, --error      runs all error tests\
  -E, --essential  runs all essential tests\
  -c, --curation   runs all curation tests


> Documentation using docstring for each tests: TO COMPLETE

_____________________________________

## How to add a test to caseologue

1)  **Query file**
  
  The query file is written in SPARQL and should (as much as possible) return the problematic concept URI, their label, the faulting property. 
  
  Add the query file to the ./caseologue_pyhton/queries directory. The name of the file is the name of the test. Words should be separated with "_". The name will be consistent across all caseologue. Extension should be ".rq"

2) **Test data**

  The test data is a small owl code reusing existing EDAM concept and adding specific errors to test the added query. Use other example as template (for the name spaces).
  
  Add the test data file to the ./caseologue_pyhton/queries directory. The name of the file should be the same as the query file it is testing + "_test_data". Extension should be ".owl"

3) **Add the test in caseologue python script**

      3.1. Add the test function. Copy the commented template at the end of the caseologue.py file. 
      
      3.2. Everything with "XXXXX" should be changed according to the added test: function name,  documentation with link to the query file once on github, called query file, error level of test, name (should be the same as the query file), debug message. Warning: the name of the function should be "test_"+name of the test

      3.3. Update the suite() function at the top of the script. According to the error level you chose you will add after the "if curation/error/essential == True" line, a "suite.addTest(EdamQueryTest("XXXXtest_function_nameXXX"))" line. Warning: the test function name should be the same as the one defined in the function you defined just before. 


4) **Add test to test_caseologue**

  In the main function of test_caseologue.py, add a call of the "test_caseologue" function with the name of your newly added test and the number of expected error from your test data.

5) **Run the test**

    First run it with its test data, see README.md in the ./caseologue_python/queries folder. Then test it with the whole EDAM, see README in the ./caseologue_python folder.
