# edam-custom
edam-custom is a CI python tool for the EDAM Ontology, grouping a set of tests (mostly using SPARQL queries) to validate the ontology. 

run edam-custom (replace the edampath):
```
EDAM_PATH=../../edamontology/EDAM_dev.owl python3 edam-custom.py 
```

Options:\
  -e, --error      runs all error tests\
  -E, --essential  runs all essential tests\
  -c, --curation   runs all curation tests


> Documentation using docstring for each tests: TO COMPLETE

Install requirements:
```
pip install -r requirements.txt
```